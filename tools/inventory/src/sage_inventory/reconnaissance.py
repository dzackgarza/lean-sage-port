"""Build the exhaustive, entity-level reconnaissance ledger."""

from __future__ import annotations

import json
import tomllib
from collections import Counter, defaultdict
from pathlib import Path

from sage_inventory.categories import measure as measure_categories
from sage_inventory.coverage import load_category_entities, load_records, partition, select
from sage_inventory.index import read_entities, read_modules
from sage_inventory.models import CapabilityStatus, IndexSummary


def build(
    index: Path,
    domains: Path,
    capabilities: Path,
    categories: Path,
) -> dict:
    """Return a reproducible disposition ledger for every indexed public manual entity."""
    domain_rows = {
        row["id"]: row
        for row in tomllib.loads(domains.read_text())["section"]
    }
    entities = read_entities(index)
    modules = {module.module: module for module in read_modules(index)}
    capability_records, exclusion_records = load_records(capabilities)

    selected_capabilities: dict[str, list[str]] = defaultdict(list)
    selected_exclusions: dict[str, list[str]] = defaultdict(list)
    for record in capability_records:
        if record.status is not CapabilityStatus.SOURCE_RECONCILED:
            continue
        for selector in record.sage:
            for entity in select(selector, entities):
                if entity.public:
                    selected_capabilities[entity.id].append(record.id)
    for record in exclusion_records:
        for selector in record.sage:
            for entity in select(selector, entities):
                if entity.public:
                    selected_exclusions[entity.id].append(record.id)

    category_selectors = load_category_entities(categories)
    summary = IndexSummary.model_validate_json((index / "summary.json").read_text())
    rows: list[dict] = []
    section_counts: dict[str, Counter] = defaultdict(Counter)

    for entity in entities:
        placement = modules[entity.module].manual
        if not entity.public or placement is None:
            continue
        section = placement.section
        domain = domain_rows[section]
        if section == "categories":
            accounting = "category-record" if entity.id in category_selectors else "unaccounted"
            owners = ["lean-categories"]
        elif selected_capabilities.get(entity.id):
            accounting = "capability"
            owners = selected_capabilities[entity.id]
        elif selected_exclusions.get(entity.id):
            accounting = "exclusion"
            owners = selected_exclusions[entity.id]
        else:
            accounting = "unaccounted"
            owners = []

        row = {
            "id": entity.id,
            "section": section,
            "section_title": placement.section_title,
            "disposition": domain["disposition"],
            "role": "mathematical-candidate" if domain["disposition"] == "mathematical" else domain["disposition"],
            "accounting": accounting,
            "owners": owners,
            "module": entity.module,
            "qualname": entity.qualname,
            "kind": entity.kind.value,
            "source_line": entity.line,
            "doctests": entity.doctests,
            "algorithm": entity.algorithm,
            "references": list(entity.references),
            "backends": list(modules[entity.module].backends),
            "source_path": modules[entity.module].path,
        }
        rows.append(row)
        section_counts[section][accounting] += 1

    sections = [
        {
            "section": section,
            "title": domain_rows[section]["title"],
            "disposition": domain_rows[section]["disposition"],
            "entities": sum(counts.values()),
            **dict(sorted(counts.items())),
        }
        for section, counts in sorted(section_counts.items())
    ]
    category_report = measure_categories(index, categories)
    return {
        "revision": summary.revision.model_dump(),
        "source": {
            "domains": str(domains),
            "capabilities": str(capabilities),
            "categories": str(categories),
        },
        "public_entities": len(rows),
        "indexed_sections": len(domain_rows),
        "populated_sections": len(sections),
        "sections": sections,
        "category_coverage": category_report.model_dump(),
        "entities": rows,
    }


def write(index: Path, domains: Path, capabilities: Path, categories: Path, report: Path) -> dict:
    """Build and write the reconnaissance report."""
    result = build(index, domains, capabilities, categories)
    report.write_text(json.dumps(result, indent=2) + "\n")
    return result
