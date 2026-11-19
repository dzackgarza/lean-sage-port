"""Write the reconnaissance ledger: every indexed module and every indexed entity with its state.

The ledger has two files. The module ledger (`inventory/reconnaissance.json`) has one row per
module: its manual section or package, its entity counts by state, the source-reconciled batches
that name it, and, for a module that the manual does not list, the manual sections of the modules
that import it. The entity ledger (`inventory/reconnaissance-entities.jsonl.gz`) has one row per
entity: its id, its state and the records that select it. The source facts of each entity
(path, line, doctests, references) stay in the index; the ledger joins to it by id.
"""

from __future__ import annotations

import gzip
import json
from collections import defaultdict
from pathlib import Path

from sage_inventory.coverage import counts, load, partition


def build(index: Path, capabilities: Path, categories: Path, worklog: Path) -> tuple[dict, list[dict]]:
    """Return the module ledger and the entity rows."""
    inventory = load(index, capabilities, categories, worklog)
    members: dict[str, list] = defaultdict(list)
    for entity in inventory.entities:
        members[entity.module].append(entity)
    importers: dict[str, set[str]] = defaultdict(set)
    for module in inventory.modules.values():
        if module.manual is None:
            continue
        for imported in module.imports:
            importers[imported].add(module.manual.section)

    rows = []
    for name, module in sorted(inventory.modules.items()):
        rows.append(
            {
                "module": name,
                "source_path": module.path,
                "part": partition(module),
                "manual": module.manual is not None,
                "batches": inventory.credit.get(name, []),
                "imported_by_sections": [] if module.manual else sorted(importers.get(name, ())),
                **counts(members[name], inventory.classes),
            }
        )
    entities = [
        {
            "id": entity.id,
            "public": entity.public,
            "state": inventory.classes[entity.id].state.value,
            "records": list(inventory.classes[entity.id].records),
        }
        for entity in inventory.entities
    ]
    ledger = {
        "revision": inventory.summary.revision.model_dump(),
        "total": counts(inventory.entities, inventory.classes),
        "modules": len(rows),
        "credited_modules": len(inventory.credit),
        "module_rows": rows,
    }
    return ledger, entities


def write(
    index: Path, capabilities: Path, categories: Path, worklog: Path, report: Path, entity_report: Path
) -> dict:
    """Build and write both ledger files; return the module ledger."""
    ledger, entities = build(index, capabilities, categories, worklog)
    report.write_text(json.dumps(ledger, indent=1) + "\n")
    with gzip.GzipFile(entity_report, "wb", mtime=0) as stream:
        for row in entities:
            stream.write(json.dumps(row, separators=(",", ":")).encode() + b"\n")
    return ledger
