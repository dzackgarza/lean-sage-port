"""Reconcile indexed Sage category entities with the existing records and research role data."""

from __future__ import annotations

import csv
import json
import tomllib
from collections import Counter
from pathlib import Path

from sage_inventory.index import read_entities, read_modules
from sage_inventory.models import IndexSummary


def _research_roles(path: Path) -> dict[tuple[str, str], str]:
    roles: dict[tuple[str, str], str] = {}
    with path.open(newline="") as stream:
        for row in csv.DictReader(stream):
            category_id = row["category_id"]
            module, _, qualname = category_id.rpartition(".")
            roles[("sage.categories." + module, qualname)] = row["role"]
    return roles


def build(
    index: Path,
    categories: Path,
    research_roles: Path,
) -> dict:
    """Return an open reconciliation ledger; no unmatched entity is closed automatically."""
    inventory = tomllib.loads(categories.read_text())
    records = {
        record["sage"]: record
        for record in (*inventory.get("category", []), *inventory.get("operation", []))
    }
    roles = _research_roles(research_roles)
    modules = {module.module: module for module in read_modules(index)}
    summary = IndexSummary.model_validate_json((index / "summary.json").read_text())

    rows: list[dict] = []
    for entity in read_entities(index):
        placement = modules[entity.module].manual
        if not entity.public or placement is None or placement.section != "categories":
            continue
        selector = f"{entity.module}:{entity.qualname}"
        role = roles.get((entity.module, entity.qualname.split(".", 1)[0]))
        record = records.get(selector)
        if record is not None and record.get("relation") == "not-yet-reconciled":
            status = "provisional"
        elif record is not None:
            status = "recorded"
        elif role is not None:
            status = "research-role-only"
        else:
            status = "open-unmatched"
        rows.append(
            {
                "id": entity.id,
                "module": entity.module,
                "qualname": entity.qualname,
                "kind": entity.kind.value,
                "source_line": entity.line,
                "research_role": role,
                "recorded": record is not None,
                "status": status,
            }
        )

    counts = Counter(row["status"] for row in rows)
    return {
        "revision": summary.revision.model_dump(),
        "source": {
            "categories": str(categories),
            "research_roles": str(research_roles),
        },
        "public_entities": len(rows),
        "recorded": counts["recorded"],
        "provisional": counts["provisional"],
        "research_role_only": counts["research-role-only"],
        "open_unmatched": counts["open-unmatched"],
        "entities": rows,
    }


def write(index: Path, categories: Path, research_roles: Path, report: Path) -> dict:
    """Build and write the category reconciliation ledger."""
    result = build(index, categories, research_roles)
    report.write_text(json.dumps(result, indent=2) + "\n")
    return result
