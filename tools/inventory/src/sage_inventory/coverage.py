"""Measure how much of the indexed Sage checkout the capability inventory accounts for.

The denominator is every public entity (class, function, method) of a module that the reference
manual documents. An entity is accounted for when a capability record or an exclusion record
selects it. A selector is a shell-style pattern:

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
    CapabilityFile,
    CoverageReport,
    Entity,
    Exclusion,
    IndexSummary,
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


def select(selector: str, entities: list[Entity]) -> list[Entity]:
    module_pattern, _, name_pattern = selector.partition(":")
    module = re.compile(translate(module_pattern))
    name = re.compile(translate(name_pattern)) if name_pattern else None
    return [
        entity
        for entity in entities
        if module.match(entity.module) and (name is None or name.match(entity.qualname))
    ]


@validate_call
def measure(index: Path, capabilities_dir: Path, reuse_dir: Path) -> CoverageReport:
    """Validate the records against the index and each other, then count what they account for."""
    entities = read_entities(index)
    modules = {module.module: module for module in read_modules(index)}
    summary = IndexSummary.model_validate_json((index / "summary.json").read_text())
    capabilities, exclusions = load_records(capabilities_dir)
    components = load_components(reuse_dir)

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

    by_capability: set[str] = set()
    excluded: set[str] = set()
    for record, bucket in [(c, by_capability) for c in capabilities] + [(e, excluded) for e in exclusions]:
        for selector in record.sage:
            matched = select(selector, entities)
            if not matched:
                problems.append(
                    f"{record.id}: selector {selector!r} matches no entity of Sage {summary.revision.version}"
                )
            bucket.update(entity.id for entity in matched)
    if problems:
        raise InventoryError("\n".join(problems))

    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    groups: dict[str, str] = {}
    for entity in entities:
        placement = modules[entity.module].manual
        if placement is None or not entity.public:
            continue
        groups[placement.section] = placement.group
        row = counts[placement.section]
        row["public_entities"] += 1
        row["doctests"] += entity.doctests
        if entity.id in by_capability:
            row["by_capability"] += 1
            row["doctests_by_capability"] += entity.doctests
        elif entity.id in excluded:
            row["excluded"] += 1
        else:
            row["unaccounted"] += 1
    sections = tuple(
        SectionCoverage(
            section=section,
            group=groups[section],
            public_entities=row["public_entities"],
            by_capability=row["by_capability"],
            excluded=row["excluded"],
            unaccounted=row["unaccounted"],
            doctests=row["doctests"],
            doctests_by_capability=row["doctests_by_capability"],
        )
        for section, row in sorted(counts.items())
    )
    return CoverageReport(
        revision=summary.revision,
        capabilities=len(capabilities),
        exclusions=len(exclusions),
        public_entities=sum(section.public_entities for section in sections),
        by_capability=sum(section.by_capability for section in sections),
        excluded=sum(section.excluded for section in sections),
        unaccounted=sum(section.unaccounted for section in sections),
        sections=sections,
    )
