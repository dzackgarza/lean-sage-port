"""Measure how much of the indexed Sage checkout the capability inventory accounts for.

The denominator is every public entity (class, function, method) of a module that the reference
manual documents. An entity is accounted for when a capability record or an exclusion record
selects it. Entities of the `categories` section are accounted for by the category and operation
records of `inventory/categories/`, which name them one by one against the `lean-categories`
catalogue rather than by selector; a measure that is given that file counts them as
`by_category_record`. Modules that the manual does not list are counted separately, by package:
Sage documents some of them through a listed class that imports their functions as methods. A
selector is a shell-style pattern:

- `sage.rings.finite_rings.*` selects every entity of the matching modules;
- `sage.rings.integer:Integer.gcd` or `sage.matrix.*:*.determinant` selects entities by qualified name.
"""

from __future__ import annotations

import json
import re
import tomllib
from collections import defaultdict
from fnmatch import translate
from pathlib import Path

from pydantic import validate_call

from sage_inventory.index import read_entities, read_modules
from sage_inventory.models import (
    Capability,
    CapabilityStatus,
    CapabilityFile,
    CoverageReport,
    Entity,
    Exclusion,
    IndexSummary,
    Module,
    PackageCoverage,
    SectionCoverage,
)


class InventoryError(ValueError):
    """The capability records are inconsistent with each other or with the index."""


def load_records(directory: Path) -> tuple[list[Capability], list[Exclusion]]:
    capabilities: list[Capability] = []
    exclusions: list[Exclusion] = []
    for path in sorted(directory.glob("*.toml")):
        parsed = CapabilityFile.model_validate_json(json.dumps(tomllib.loads(path.read_text())))
        capabilities.extend(parsed.capability)
        exclusions.extend(parsed.exclusion)
    return capabilities, exclusions


def load_components(directory: Path) -> set[str]:
    """Component ids of the reuse surveys (`inventory/reuse/*.toml`)."""
    return {
        component["id"]
        for path in sorted(directory.glob("*.toml"))
        for component in tomllib.loads(path.read_text()).get("component", [])
    }


def load_category_entities(categories: Path | None) -> set[str]:
    """Entity ids that a category or operation record of the category inventory accounts for."""
    if categories is None:
        return set()
    inventory = tomllib.loads(categories.read_text())
    return {
        record["sage"]
        for record in (*inventory.get("category", []), *inventory.get("operation", []))
    }


def select(selector: str, entities: list[Entity]) -> list[Entity]:
    module_pattern, _, name_pattern = selector.partition(":")
    module = re.compile(translate(module_pattern))
    name = re.compile(translate(name_pattern)) if name_pattern else None
    return [
        entity
        for entity in entities
        if module.match(entity.module) and (name is None or name.match(entity.qualname))
    ]


def partition(entity: Entity, modules: dict[str, Module]) -> str:
    """The unit of the report that counts an entity: its manual section, or its package outside the manual."""
    placement = modules[entity.module].manual
    return ".".join(entity.module.split(".")[:2]) if placement is None else placement.section


@validate_call
def unaccounted(
    index: Path, capabilities_dir: Path, name: str, categories: Path | None = None
) -> list[Entity]:
    """The public entities of one manual section, or of one package outside the manual, that no record selects."""
    entities = read_entities(index)
    modules = {module.module: module for module in read_modules(index)}
    members = [entity for entity in entities if entity.public and partition(entity, modules) == name]
    if not members:
        raise InventoryError(f"no manual section and no package outside the manual is named {name!r}")
    capabilities, exclusions = load_records(capabilities_dir)
    selected = {
        entity.id
        for record in (*capabilities, *exclusions)
        for selector in record.sage
        for entity in select(selector, members)
    } | load_category_entities(categories)
    return [entity for entity in members if entity.id not in selected]


@validate_call
def measure(
    index: Path, capabilities_dir: Path, reuse_dir: Path, categories: Path | None = None
) -> CoverageReport:
    """Validate the records against the index and each other, then count what they account for."""
    entities = read_entities(index)
    modules = {module.module: module for module in read_modules(index)}
    summary = IndexSummary.model_validate_json((index / "summary.json").read_text())
    capabilities, exclusions = load_records(capabilities_dir)
    components = load_components(reuse_dir)
    category_entities = load_category_entities(categories)

    problems: list[str] = []
    ids = [record.id for record in (*capabilities, *exclusions)]
    problems += [f"duplicate id {name}" for name in sorted({name for name in ids if ids.count(name) > 1})]
    known = {capability.id for capability in capabilities}
    for capability in capabilities:
        for other in (*capability.depends_on, *capability.generalizes):
            if other not in known:
                problems.append(f"{capability.id} refers to unknown capability {other}")
        for component in capability.reuse.components:
            if component not in components:
                problems.append(f"{capability.id} refers to unknown reuse component {component}")
        for entry in capability.catalogue:
            if f"catalogue.{entry}" not in components:
                problems.append(f"{capability.id} refers to unknown catalogue id {entry}")

    by_capability: set[str] = set()
    excluded: set[str] = set()
    for record, bucket in [
        (c, by_capability)
        for c in capabilities
        if c.status is CapabilityStatus.SOURCE_RECONCILED
    ] + [(e, excluded) for e in exclusions]:
        for selector in record.sage:
            matched = [entity for entity in select(selector, entities) if entity.public]
            if not matched:
                problems.append(
                    f"{record.id}: selector {selector!r} matches no public entity of Sage "
                    f"{summary.revision.version}"
                )
            bucket.update(entity.id for entity in matched)
    if problems:
        raise InventoryError("\n".join(problems))

    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    groups: dict[str, str] = {}
    unlisted: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for entity in entities:
        if not entity.public:
            continue
        placement = modules[entity.module].manual
        if placement is None:
            row = unlisted[partition(entity, modules)]
        else:
            groups[placement.section] = placement.group
            row = counts[partition(entity, modules)]
        row["public_entities"] += 1
        row["doctests"] += entity.doctests
        if entity.id in by_capability:
            row["by_capability"] += 1
            row["doctests_by_capability"] += entity.doctests
        elif entity.id in excluded:
            row["excluded"] += 1
        elif entity.id in category_entities:
            row["by_category_record"] += 1
        else:
            row["unaccounted"] += 1
    sections = tuple(
        SectionCoverage(
            section=section,
            group=groups[section],
            public_entities=row["public_entities"],
            by_capability=row["by_capability"],
            excluded=row["excluded"],
            by_category_record=row["by_category_record"],
            unaccounted=row["unaccounted"],
            doctests=row["doctests"],
            doctests_by_capability=row["doctests_by_capability"],
        )
        for section, row in sorted(counts.items())
    )
    return CoverageReport(
        revision=summary.revision,
        capabilities=len(capabilities),
        attached_to_catalogue=sum(bool(capability.catalogue) for capability in capabilities),
        exclusions=len(exclusions),
        public_entities=sum(section.public_entities for section in sections),
        by_capability=sum(section.by_capability for section in sections),
        excluded=sum(section.excluded for section in sections),
        by_category_record=sum(section.by_category_record for section in sections),
        unaccounted=sum(section.unaccounted for section in sections),
        sections=sections,
        unlisted=tuple(
            PackageCoverage(
                package=package,
                public_entities=row["public_entities"],
                by_capability=row["by_capability"],
                excluded=row["excluded"],
                unaccounted=row["unaccounted"],
            )
            for package, row in sorted(unlisted.items())
        ),
    )
