"""Build the module-level reconnaissance scope ledger."""

from __future__ import annotations

import json
import tomllib
from collections import Counter, defaultdict
from pathlib import Path

from sage_inventory.coverage import load_records, select
from sage_inventory.models import CapabilityStatus
from sage_inventory.index import read_entities, read_modules
from sage_inventory.models import IndexSummary


PHASES = {
    "categories": "R0",
    "sets": "R1",
    "monoids": "R1",
    "groups": "R1",
    "semirings": "R1",
    "rings": "R1",
    "finite_rings": "R1",
    "modules": "R1",
    "tensor_free_modules": "R1",
    "polynomial_rings": "R2",
    "power_series": "R2",
    "noncommutative_polynomial_rings": "R2",
    "algebras": "R2",
    "quivers": "R2",
    "homology": "R2",
    "resolutions": "R2",
    "matrices": "R3",
    "linear_algebra": "R3",
    "polynomial_algorithms": "R3",
    "number_fields": "R3",
    "function_fields": "R3",
    "padics": "R3",
    "valuations": "R3",
    "quadratic_forms": "R3",
    "lattices": "R3",
    "combinat": "R4",
    "graphs": "R4",
    "matroids": "R4",
    "coding": "R4",
    "cryptography": "R4",
    "logic": "R4",
    "sat": "R4",
    "game_theory": "R4",
    "curves": "R5",
    "arithmetic_curves": "R5",
    "schemes": "R5",
    "manifolds": "R5",
    "topology": "R5",
    "riemannian_geometry": "R5",
    "hyperbolic_geometry": "R5",
    "euclidean_spaces": "R5",
    "knots": "R5",
    "calculus": "R6",
    "functions": "R6",
    "numerical": "R6",
    "rings_numerical": "R6",
    "stats": "R6",
    "probability": "R6",
    "asymptotic": "R6",
    "dynamics": "R6",
    "constants": "R6",
    "modfrm": "R7",
    "modsym": "R7",
    "modabvar": "R7",
    "drinfeld_modules": "R7",
    "drinfeld_modular": "R7",
    "anderson_motives": "R7",
    "hecke": "R7",
    "lfunctions": "R7",
}


def build(index: Path, domains: Path, capabilities: Path, categories: Path) -> dict:
    """Return one non-closing scope row for every indexed public source module."""
    domain_rows = {
        row["id"]: row for row in tomllib.loads(domains.read_text())["section"]
    }
    entities = read_entities(index)
    modules = {module.module: module for module in read_modules(index)}
    capability_records, exclusion_records = load_records(capabilities)
    public_entities = [entity for entity in entities if entity.public]
    selected_capabilities = {
        entity.id
        for record in capability_records
        if record.status is CapabilityStatus.SOURCE_RECONCILED
        for selector in record.sage
        for entity in select(selector, public_entities)
    }
    selected_exclusions = {
        entity.id
        for record in exclusion_records
        for selector in record.sage
        for entity in select(selector, public_entities)
    }

    grouped: dict[str, list] = defaultdict(list)
    for entity in entities:
        if entity.public:
            grouped[entity.module].append(entity)

    rows = []
    for module, module_record in sorted(modules.items()):
        public = grouped.get(module, [])
        placement = module_record.manual
        section = placement.section if placement else "unlisted"
        domain = domain_rows.get(section)
        if section == "categories":
            category_inventory = tomllib.loads(categories.read_text())
            category_selectors = {
                record["sage"]
                for record in (*category_inventory.get("category", []), *category_inventory.get("operation", []))
            }
            accounted = sum(entity.id in category_selectors for entity in public)
            capabilities_count = 0
            exclusions_count = 0
        else:
            accounted = sum(entity.id in selected_capabilities or entity.id in selected_exclusions for entity in public)
            capabilities_count = sum(entity.id in selected_capabilities for entity in public)
            exclusions_count = sum(entity.id in selected_exclusions for entity in public)
        open_count = len(public) - accounted
        rows.append(
            {
                "module": module,
                "source_path": module_record.path,
                "section": section,
                "phase": PHASES.get(section, "UNASSIGNED"),
                "disposition": domain["disposition"] if domain else "unlisted",
                "public_entities": len(public),
                "capability_entities": capabilities_count,
                "excluded_entities": exclusions_count,
                "accounted_entities": accounted,
                "open_entities": open_count,
                "status": (
                    "not-in-denominator"
                    if not public
                    else "open"
                    if open_count
                    else "accounted-awaiting-review"
                ),
            }
        )

    counts = Counter(row["status"] for row in rows)
    return {
        "revision": IndexSummary.model_validate_json((index / "summary.json").read_text()).revision.model_dump(),
        "indexed_modules": len(rows),
        "public_entities": sum(row["public_entities"] for row in rows),
        "accounted_entities": sum(row["accounted_entities"] for row in rows),
        "open_entities": sum(row["open_entities"] for row in rows),
        "open_modules": counts["open"],
        "rows": rows,
    }


def write(index: Path, domains: Path, capabilities: Path, categories: Path, report: Path) -> dict:
    result = build(index, domains, capabilities, categories)
    report.write_text(json.dumps(result, indent=2) + "\n")
    return result
