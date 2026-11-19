"""Measure the Sage category inventory against the indexed public category entities."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from sage_inventory.index import read_entities, read_modules
from sage_inventory.models import IndexSummary, Revision


class CategoryCoverage(BaseModel):
    """Machine-readable coverage of the Sage category framework inventory."""

    model_config = ConfigDict(extra="forbid")

    revision: Revision
    public_entities: int
    represented: int
    reconciled: int
    provisional: int
    catalogue_mapped: int
    ownership_gaps: int
    unaccounted: int
    category_records: int
    operation_records: int
    catalogue_categories: int
    catalogue_operations: int
    missing_entities: tuple[str, ...]


def measure(index: Path, categories: Path) -> CategoryCoverage:
    """Compare category-inventory selectors with public ``sage.categories`` entities."""
    entities = read_entities(index)
    modules = {module.module: module for module in read_modules(index)}
    public = sorted(
        entity.id
        for entity in entities
        if entity.public
        and modules[entity.module].manual is not None
        and modules[entity.module].manual.section == "categories"
    )
    inventory = tomllib.loads(categories.read_text())
    category_records = inventory.get("category", [])
    operation_records = inventory.get("operation", [])
    selectors = {
        record["sage"]
        for record in (*category_records, *operation_records)
    }
    records = {
        record["sage"]: record
        for record in (*category_records, *operation_records)
    }
    missing = tuple(entity_id for entity_id in public if entity_id not in selectors)
    represented_ids = set(public) - set(missing)
    provisional = sum(
        records[entity_id].get("relation") == "not-yet-reconciled"
        for entity_id in represented_ids
    )
    catalogue_mapped = sum(bool(records[entity_id].get("catalogue")) for entity_id in represented_ids)
    ownership_gaps = sum(
        records[entity_id].get("relation") == "absent"
        for entity_id in represented_ids
    )
    return CategoryCoverage(
        revision=IndexSummary.model_validate_json((index / "summary.json").read_text()).revision,
        public_entities=len(public),
        represented=len(public) - len(missing),
        reconciled=len(represented_ids) - provisional,
        provisional=provisional,
        catalogue_mapped=catalogue_mapped,
        ownership_gaps=ownership_gaps,
        unaccounted=len(missing),
        category_records=len(category_records),
        operation_records=len(operation_records),
        catalogue_categories=sum(bool(record.get("catalogue")) for record in category_records),
        catalogue_operations=sum(bool(record.get("catalogue")) for record in operation_records),
        missing_entities=missing,
    )
