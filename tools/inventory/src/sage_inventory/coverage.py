"""Classify every indexed entity of the Sage checkout by reconnaissance state, and count the states.

The denominator is every class, function and method that the index records, public or not, in
every module under `src/sage`. The reference manual is generated from that source and documents a
subset of it, so manual placement is an attribute of a module, not a bound on the scope.

A record is a claim about source; a source-reconciled worklog batch is the record that the source
was read. An entity is therefore closed only when both exist (see `State`):

- `reconciled`: a source-reconciled capability selects it and a source-reconciled batch names its
  module;
- `excluded`: an exclusion selects it and a source-reconciled batch names its module;
- `category-record`: a category or operation record of `inventory/categories/` names it.

An entity that only a record selects is `scoped`; an entity that no record selects is `unaccounted`.

A selector is a shell-style pattern:

- `sage.rings.finite_rings.*` selects every entity of the matching modules;
- `sage.rings.integer:Integer.gcd` or `sage.matrix.*:*.determinant` selects entities by qualified name.
"""

from __future__ import annotations

import json
import re
import tomllib
from collections import defaultdict
from dataclasses import dataclass
from fnmatch import translate
from pathlib import Path

from pydantic import validate_call

from sage_inventory.index import read_entities, read_modules
from sage_inventory.models import (
    OPEN_STATES,
    BatchStatus,
    Capability,
    CapabilityFile,
    CapabilityStatus,
    CoverageReport,
    Entity,
    Exclusion,
    IndexSummary,
    Module,
    PartCoverage,
    State,
    StateCounts,
    Worklog,
)


class InventoryError(ValueError):
    """The records or the worklog are inconsistent with each other or with the index."""


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


def load_category_entities(categories: Path) -> set[str]:
    """Entity ids that a category or operation record of the category inventory names."""
    inventory = tomllib.loads(categories.read_text())
    return {
        record["sage"]
        for record in (*inventory.get("category", []), *inventory.get("operation", []))
    }


def load_worklog(path: Path) -> Worklog:
    return Worklog.model_validate_json(json.dumps(tomllib.loads(path.read_text())))


def by_module(entities: list[Entity]) -> dict[str, list[Entity]]:
    grouped: dict[str, list[Entity]] = defaultdict(list)
    for entity in entities:
        grouped[entity.module].append(entity)
    return grouped


def select(selector: str, grouped: dict[str, list[Entity]]) -> list[Entity]:
    """The entities that a selector matches; `grouped` is the index by module (`by_module`)."""
    module_pattern, _, name_pattern = selector.partition(":")
    module = re.compile(translate(module_pattern))
    name = re.compile(translate(name_pattern)) if name_pattern else None
    return [
        entity
        for module_name, members in grouped.items()
        if module.match(module_name)
        for entity in members
        if name is None or name.match(entity.qualname)
    ]


def credited_modules(worklog: Worklog, modules: dict[str, Module], revision_commit: str) -> dict[str, list[str]]:
    """Map each module that a source-reconciled batch names to those batch ids.

    Fails when the worklog describes another commit, when a module entry matches no indexed module,
    or when a source-reconciled batch names anything other than exact module names.
    """
    problems: list[str] = []
    if worklog.baseline_commit != revision_commit:
        problems.append(f"worklog describes commit {worklog.baseline_commit}, the index {revision_commit}")
    credit: dict[str, list[str]] = defaultdict(list)
    for batch in worklog.batch:
        for entry in batch.modules:
            if batch.status is BatchStatus.SOURCE_RECONCILED:
                if entry not in modules:
                    problems.append(f"{batch.id}: source-reconciled batch names {entry!r}, which is no indexed module")
                    continue
                credit[entry].append(batch.id)
            elif not any(re.match(translate(entry), name) for name in modules):
                problems.append(f"{batch.id}: module entry {entry!r} matches no indexed module")
    if problems:
        raise InventoryError("\n".join(problems))
    return credit


@dataclass(frozen=True)
class Classification:
    state: State
    records: tuple[str, ...]


def classify(
    grouped: dict[str, list[Entity]],
    capabilities: list[Capability],
    exclusions: list[Exclusion],
    category_entities: set[str],
    credit: dict[str, list[str]],
) -> dict[str, Classification]:
    """The reconnaissance state and the selecting record ids of every indexed entity."""
    reconciling: dict[str, list[str]] = defaultdict(list)
    excluding: dict[str, list[str]] = defaultdict(list)
    scoping: dict[str, list[str]] = defaultdict(list)
    for record in capabilities:
        target = reconciling if record.status is CapabilityStatus.SOURCE_RECONCILED else scoping
        for selector in record.sage:
            for entity in select(selector, grouped):
                target[entity.id].append(record.id)
    for record in exclusions:
        for selector in record.sage:
            for entity in select(selector, grouped):
                excluding[entity.id].append(record.id)

    result: dict[str, Classification] = {}
    for module_name, members in grouped.items():
        read = module_name in credit
        for entity in members:
            records = tuple(dict.fromkeys((*reconciling[entity.id], *excluding[entity.id], *scoping[entity.id])))
            if entity.id in category_entities:
                state = State.CATEGORY_RECORD
            elif read and reconciling[entity.id]:
                state = State.RECONCILED
            elif read and excluding[entity.id]:
                state = State.EXCLUDED
            elif records:
                state = State.SCOPED
            else:
                state = State.UNACCOUNTED
            result[entity.id] = Classification(state, records)
    return result


def partition(module: Module) -> str:
    """The part of the report that counts a module: its manual section, or its two-level package outside the manual."""
    return ".".join(module.module.split(".")[:2]) if module.manual is None else module.manual.section


@dataclass(frozen=True)
class Inventory:
    """The index joined with the records and the worklog, classified."""

    summary: IndexSummary
    entities: list[Entity]
    modules: dict[str, Module]
    capabilities: list[Capability]
    exclusions: list[Exclusion]
    credit: dict[str, list[str]]
    classes: dict[str, Classification]


def load(index: Path, capabilities_dir: Path, categories: Path, worklog: Path) -> Inventory:
    entities = read_entities(index)
    modules = {module.module: module for module in read_modules(index)}
    summary = IndexSummary.model_validate_json((index / "summary.json").read_text())
    capabilities, exclusions = load_records(capabilities_dir)
    credit = credited_modules(load_worklog(worklog), modules, summary.revision.commit)
    classes = classify(by_module(entities), capabilities, exclusions, load_category_entities(categories), credit)
    return Inventory(summary, entities, modules, capabilities, exclusions, credit, classes)


@validate_call
def remaining(
    index: Path, capabilities_dir: Path, categories: Path, worklog: Path, name: str
) -> list[tuple[Entity, State]]:
    """The open entities of one manual section, or of one package outside the manual, with their states."""
    inventory = load(index, capabilities_dir, categories, worklog)
    members = [entity for entity in inventory.entities if partition(inventory.modules[entity.module]) == name]
    if not members:
        raise InventoryError(f"no manual section and no package outside the manual is named {name!r}")
    return [
        (entity, inventory.classes[entity.id].state)
        for entity in members
        if inventory.classes[entity.id].state in OPEN_STATES
    ]


def _problems(inventory: Inventory, components: set[str]) -> list[str]:
    capabilities, exclusions = inventory.capabilities, inventory.exclusions
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
    grouped = by_module(inventory.entities)
    for record in (*capabilities, *exclusions):
        for selector in record.sage:
            if not select(selector, grouped):
                problems.append(
                    f"{record.id}: selector {selector!r} matches no entity of Sage {inventory.summary.revision.version}"
                )
    return problems


def counts(members: list[Entity], classes: dict[str, Classification]) -> dict[str, int]:
    """Entity, public-entity and doctest totals of `members`, and their number in each state."""
    counts = {state.value.replace("-", "_"): 0 for state in State}
    for entity in members:
        counts[classes[entity.id].state.value.replace("-", "_")] += 1
    return {
        "entities": len(members),
        "public_entities": sum(entity.public for entity in members),
        "doctests": sum(entity.doctests for entity in members),
        **counts,
    }


@validate_call
def measure(
    index: Path, capabilities_dir: Path, reuse_dir: Path, categories: Path, worklog: Path
) -> CoverageReport:
    """Validate the records against the index and each other, then count every entity by state."""
    inventory = load(index, capabilities_dir, categories, worklog)
    problems = _problems(inventory, load_components(reuse_dir))
    if problems:
        raise InventoryError("\n".join(problems))

    parts: dict[str, list[Entity]] = defaultdict(list)
    groups: dict[str, str] = {}
    for entity in inventory.entities:
        module = inventory.modules[entity.module]
        parts[partition(module)].append(entity)
        if module.manual is not None:
            groups[module.manual.section] = module.manual.group
    rows = [
        PartCoverage(part=part, group=groups.get(part, ""), **counts(members, inventory.classes))
        for part, members in sorted(parts.items())
    ]
    return CoverageReport(
        revision=inventory.summary.revision,
        capabilities=len(inventory.capabilities),
        attached_to_catalogue=sum(bool(capability.catalogue) for capability in inventory.capabilities),
        exclusions=len(inventory.exclusions),
        credited_modules=len(inventory.credit),
        modules=len(inventory.modules),
        total=StateCounts(**counts(inventory.entities, inventory.classes)),
        sections=tuple(row for row in rows if row.part in groups),
        unlisted=tuple(row for row in rows if row.part not in groups),
    )
