"""Expand capability selectors into source-backed evidence and oracle obligations."""

from __future__ import annotations

import json
from pathlib import Path

from sage_inventory.coverage import load_records, select
from sage_inventory.index import read_entities, read_modules
from sage_inventory.models import CapabilityStatus, IndexSummary


def build(index: Path, capabilities: Path) -> dict:
    """Return one source and oracle evidence row for every capability."""
    entities = read_entities(index)
    modules = {module.module: module for module in read_modules(index)}
    records, _ = load_records(capabilities)
    summary = IndexSummary.model_validate_json((index / "summary.json").read_text())
    rows = []
    unresolved = []
    broad_selectors = []

    for record in records:
        matched_by_selector = {
            selector: sorted(
                entity.id
                for entity in select(selector, entities)
                if entity.public
            )
            for selector in record.sage
        }
        selected_ids = sorted({entity_id for ids in matched_by_selector.values() for entity_id in ids})
        selected = {entity.id: entity for entity in entities if entity.id in selected_ids}
        source_entities = []
        for entity_id in selected_ids:
            entity = selected[entity_id]
            module = modules[entity.module]
            source_entities.append(
                {
                    "id": entity.id,
                    "module": entity.module,
                    "qualname": entity.qualname,
                    "source_path": module.path,
                    "source_line": entity.line,
                    "doctests": entity.doctests,
                    "algorithm": entity.algorithm,
                    "references": list(entity.references),
                    "backends": list(module.backends),
                }
            )
        source_doctests = sum(entity["doctests"] for entity in source_entities)
        empty_selectors = [selector for selector, ids in matched_by_selector.items() if not ids]
        broad_selectors.extend(
            {
                "capability": record.id,
                "selector": selector,
                "public_entities": len(ids),
            }
            for selector, ids in matched_by_selector.items()
            if "*" in selector
        )
        if record.status is CapabilityStatus.SOURCE_RECONCILED and (
            not source_entities or not record.tests or empty_selectors
        ):
            unresolved.append(record.id)
        rows.append(
            {
                "id": record.id,
                "status": record.status.value,
                "selectors": matched_by_selector,
                "empty_selectors": empty_selectors,
                "source_entities": source_entities,
                "source_doctests": source_doctests,
                "oracle_inputs": list(record.tests),
                "oracle_input_status": (
                    "source-doctest-backed" if source_doctests else "contract-input-backed"
                ),
                "catalogue": list(record.catalogue),
                "depends_on": list(record.depends_on),
            }
        )

    return {
        "revision": summary.revision.model_dump(),
        "source": {
            "index": str(index),
            "capabilities": str(capabilities),
        },
        "capabilities": len(rows),
        "unresolved": unresolved,
        "distinct_source_entities": len(
            {entity["id"] for row in rows for entity in row["source_entities"]}
        ),
        "broad_selectors": broad_selectors,
        "broad_selector_count": len(broad_selectors),
        "overlapping_entities": [
            {
                "entity": entity_id,
                "capabilities": owners,
            }
            for entity_id, owners in sorted(
                _owners(rows).items()
            )
            if len(owners) > 1
        ],
        "records": rows,
    }


def _owners(rows: list[dict]) -> dict[str, list[str]]:
    owners: dict[str, list[str]] = {}
    for row in rows:
        for entity in row["source_entities"]:
            owners.setdefault(entity["id"], []).append(row["id"])
    return owners


def write(index: Path, capabilities: Path, report: Path) -> dict:
    """Build and write the capability evidence report."""
    result = build(index, capabilities)
    report.write_text(json.dumps(result, indent=2) + "\n")
    return result
