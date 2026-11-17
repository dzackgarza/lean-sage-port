"""Build the automated index of the local Sage checkout and write it under `inventory/sage/index`."""

from __future__ import annotations

import gzip
import logging
import re
import subprocess
from collections import defaultdict
from collections.abc import Iterable
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import yaml
from pydantic import BaseModel, validate_call

from sage_inventory.manual import front_page, placements
from sage_inventory.models import Baseline, Entity, IndexSummary, Module, Revision, Section
from sage_inventory.packages import read_packages
from sage_inventory.scan import Scan, scan_file

log = logging.getLogger("sage_inventory")


def load_baseline(path: Path) -> Baseline:
    return Baseline.model_validate(yaml.safe_load(path.read_text()), strict=False)


class CheckoutError(RuntimeError):
    """The checkout is not in a state that one commit describes."""


def _git(checkout: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(checkout), *arguments], check=True, capture_output=True, text=True
    ).stdout.strip()


@validate_call
def read_revision(baseline: Baseline) -> Revision:
    """Identify the checkout's commit. Refuse a tree whose indexed paths differ from that commit."""
    checkout = baseline.root()
    paths = baseline.paths
    changed = _git(checkout, "status", "--porcelain", "--", paths.source, paths.manual, paths.packages)
    if changed:
        raise CheckoutError(f"{checkout} has uncommitted changes in the indexed paths:\n{changed}")
    assigned = re.search(r"^version = '([^']+)'", (checkout / paths.version).read_text(), re.MULTILINE)
    if assigned is None:
        raise CheckoutError(f"{checkout / paths.version} assigns no version")
    return Revision(version=assigned.group(1), commit=_git(checkout, "rev-parse", "HEAD"))


def _scan(job: tuple[str, str, str]) -> tuple[str, str, Scan]:
    module, path, include = job
    return module, path, scan_file(module, Path(path), Path(include))


def _imported_modules(module: str, scan: Scan, known: frozenset[str]) -> tuple[str, ...]:
    """The indexed modules that `module` imports.

    `from a import b` names the module `a.b` when that module exists, and `a` otherwise.
    """
    found: set[str] = set()
    for imported in scan.imports:
        submodules = {f"{imported.module}.{name}" for name in imported.names} & known
        found |= submodules
        if len(submodules) < len(imported.names) or not imported.names:
            found |= {imported.module} & known
    return tuple(sorted(found - {module}))


def _module_name(path: Path, include: Path) -> str:
    parts = path.relative_to(include).with_suffix("").parts
    return ".".join(parts[:-1] if parts[-1] == "__init__" else parts)


@validate_call
def build_index(baseline: Baseline, output: Path) -> IndexSummary:
    """Index every module of the checkout at its current commit."""
    checkout = baseline.root()
    revision = read_revision(baseline)
    source = checkout / baseline.paths.source
    include = source.parent
    manual = checkout / baseline.paths.manual
    placed = placements(manual)
    files = sorted(path for suffix in ("*.py", "*.pyx") for path in source.rglob(suffix))
    jobs = [(_module_name(path, include), str(path), str(include)) for path in files]
    log.info("scanning %d source files of Sage %s (%s)", len(jobs), revision.version, revision.commit)

    known = frozenset(name for name, _, _ in jobs)
    modules: list[Module] = []
    entities: list[Entity] = []
    with ProcessPoolExecutor() as pool:
        for name, path, scan in pool.map(_scan, jobs, chunksize=16):
            entities.extend(scan.entities)
            kinds = [entity.kind.value for entity in scan.entities]
            modules.append(
                Module(
                    module=name,
                    path=str(Path(path).relative_to(checkout)),
                    language="cython" if path.endswith(".pyx") else "python",
                    title=scan.title,
                    manual=placed.get(name),
                    classes=kinds.count("class"),
                    functions=kinds.count("function"),
                    methods=kinds.count("method"),
                    public_entities=sum(entity.public for entity in scan.entities),
                    doctests=scan.doctests,
                    imports=_imported_modules(name, scan, known),
                    backends=scan.backends,
                    features=scan.features,
                )
            )

    for missing in sorted(set(placed) - known):
        log.warning("the manual lists %s, which has no source file", missing)

    in_manual = {module.module for module in modules if module.manual}
    per_section: dict[str, list[Module]] = defaultdict(list)
    for module in modules:
        if module.manual:
            per_section[module.manual.section].append(module)
    sections = [
        Section(
            section=section,
            group=group,
            title=title,
            modules=len(per_section[section]),
            public_entities=sum(module.public_entities for module in per_section[section]),
            doctests=sum(module.doctests for module in per_section[section]),
        )
        for section, (group, title) in sorted(front_page(manual).items())
    ]
    packages = read_packages(checkout / baseline.paths.packages)
    summary = IndexSummary(
        revision=revision,
        modules=len(modules),
        manual_modules=len(in_manual),
        entities=len(entities),
        public_entities=sum(entity.public for entity in entities),
        manual_public_entities=sum(entity.public for entity in entities if entity.module in in_manual),
        doctests=sum(module.doctests for module in modules),
        packages=len(packages),
    )

    output.mkdir(parents=True, exist_ok=True)
    _write_lines(output / "modules.jsonl", sorted(modules, key=lambda module: module.module))
    _write_lines(output / "sections.jsonl", sections)
    _write_lines(output / "packages.jsonl", packages)
    with gzip.GzipFile(output / "entities.jsonl.gz", "wb", mtime=0) as stream:
        for entity in sorted(entities, key=lambda entity: (entity.module, entity.line, entity.qualname)):
            stream.write(entity.model_dump_json().encode() + b"\n")
    (output / "summary.json").write_text(summary.model_dump_json(indent=2) + "\n")
    log.info("indexed %d modules, %d entities", summary.modules, summary.entities)
    return summary


def _write_lines(path: Path, records: Iterable[BaseModel]) -> None:
    path.write_text("".join(record.model_dump_json() + "\n" for record in records))


def read_entities(index: Path) -> list[Entity]:
    with gzip.open(index / "entities.jsonl.gz", "rt") as stream:
        return [Entity.model_validate_json(line) for line in stream]


def read_modules(index: Path) -> list[Module]:
    return [Module.model_validate_json(line) for line in (index / "modules.jsonl").read_text().splitlines()]
