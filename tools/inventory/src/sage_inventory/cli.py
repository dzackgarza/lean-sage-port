"""Command line of the Sage capability inventory."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from cyclopts import App

from sage_inventory import categories as categories_logic
from sage_inventory import coverage as coverage_logic
from sage_inventory import evidence as evidence_logic
from sage_inventory import graph as graph_logic
from sage_inventory import index as index_logic
from sage_inventory import reconnaissance as reconnaissance_logic
from sage_inventory.models import CapabilityFile

app = App(help="Index the local SageMath checkout and measure what the capability inventory accounts for.")


def _logging() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(asctime)s %(name)s %(levelname)s %(message)s")


@app.command
def index(baseline: Path, output: Path) -> None:
    """Index every module, class, function and method of the local Sage checkout.

    The index records the checkout's commit. The command fails when the indexed paths have
    uncommitted changes, because the recorded commit would then not describe the content.

    Args:
        baseline: The baseline configuration (`inventory/sage/baseline.yaml`).
        output: Directory that receives the index (`inventory/sage/index`).
    """
    _logging()
    print(index_logic.build_index(index_logic.load_baseline(baseline), output).model_dump_json(indent=2))


_STATES = ("unaccounted", "scoped", "reconciled", "excluded", "category_record")


def _state_line(row: dict) -> str:
    return "  ".join(f"{state.replace('_', '-')} {row[state]}" for state in _STATES)


@app.command
def coverage(
    index: Path, capabilities: Path, reuse: Path, categories: Path, worklog: Path, report: Path
) -> None:
    """Validate the records and the worklog, and write the coverage report over every indexed entity.

    Fails when a record refers to an unknown capability, reuse component or catalogue id, when a
    selector matches nothing in the index, or when a worklog batch names no indexed module.

    Args:
        index: The index directory (`inventory/sage/index`).
        capabilities: Directory of capability records (`inventory/capabilities`).
        reuse: Directory of reuse surveys (`inventory/reuse`).
        categories: The category inventory (`inventory/categories/sage-categories.toml`).
        worklog: The source-reading worklog (`inventory/reconnaissance-worklog.toml`).
        report: The report file to write (`inventory/coverage.json`).
    """
    _logging()
    try:
        result = coverage_logic.measure(index, capabilities, reuse, categories, worklog)
    except coverage_logic.InventoryError as error:
        sys.exit(f"capability inventory is inconsistent:\n{error}")
    report.write_text(result.model_dump_json(indent=2) + "\n")
    total = result.total
    print(
        f"Sage {result.revision.version} ({result.revision.commit[:12]}): {total.entities} indexed entities "
        f"({total.public_entities} public) in {result.modules} modules, {result.credited_modules} credited"
    )
    print("  " + _state_line(total.model_dump()))
    print(f"  capabilities {result.capabilities}  attached to the catalogue {result.attached_to_catalogue}")
    for part in (*result.sections, *result.unlisted):
        print(f"  {part.part:34} {part.entities:6}  " + _state_line(part.model_dump()))


@app.command
def category_coverage(index: Path, categories: Path, report: Path) -> None:
    """Measure the category inventory against indexed public ``sage.categories`` entities.

    Args:
        index: The index directory (`inventory/sage/index`).
        categories: The category inventory (`inventory/categories/sage-categories.toml`).
        report: The report file (`inventory/categories/coverage.json`).
    """
    result = categories_logic.measure(index, categories)
    report.write_text(result.model_dump_json(indent=2) + "\n")
    print(
        f"Sage {result.revision.version} ({result.revision.commit[:12]}): "
        f"{result.public_entities} public category entities"
    )
    print(
        f"  represented {result.represented}  reconciled {result.reconciled}  "
        f"provisional {result.provisional}  unaccounted {result.unaccounted}  "
        f"catalogue-mapped {result.catalogue_mapped}  ownership-gaps {result.ownership_gaps}  "
        f"category records {result.category_records}  operation records {result.operation_records}"
    )


@app.command
def category_reconciliation(index: Path, categories: Path, research_roles: Path, report: Path) -> None:
    """Write an open reconciliation ledger for indexed Sage category entities.

    Args:
        index: The indexed Sage checkout (`inventory/sage/index`).
        categories: The category inventory (`inventory/categories/sage-categories.toml`).
        research_roles: The research category-role CSV.
        report: The reconciliation report (`inventory/categories/reconciliation.json`).
    """
    from sage_inventory import category_reconciliation

    result = category_reconciliation.write(index, categories, research_roles, report)
    print(
        f"Sage {result['revision']['version']} ({result['revision']['commit'][:12]}): "
        f"{result['public_entities']} public category entities"
    )
    print(
        f"  recorded {result['recorded']}  provisional {result['provisional']}  "
        f"research-role-only {result['research_role_only']}  "
        f"open-unmatched {result['open_unmatched']}"
    )


@app.command
def reconnaissance(
    index: Path, capabilities: Path, categories: Path, worklog: Path, report: Path, entities: Path
) -> None:
    """Write the reconnaissance ledger: one row per indexed module and one row per indexed entity.

    Args:
        index: The indexed Sage checkout (`inventory/sage/index`).
        capabilities: Capability and exclusion records (`inventory/capabilities`).
        categories: Category framework records (`inventory/categories/sage-categories.toml`).
        worklog: The source-reading worklog (`inventory/reconnaissance-worklog.toml`).
        report: The module ledger (`inventory/reconnaissance.json`).
        entities: The entity ledger (`inventory/reconnaissance-entities.jsonl.gz`).
    """
    try:
        result = reconnaissance_logic.write(index, capabilities, categories, worklog, report, entities)
    except coverage_logic.InventoryError as error:
        sys.exit(f"capability inventory is inconsistent:\n{error}")
    print(
        f"Sage {result['revision']['version']} ({result['revision']['commit'][:12]}): "
        f"{result['total']['entities']} indexed entities in {result['modules']} modules, "
        f"{result['credited_modules']} credited"
    )
    print("  " + _state_line(result["total"]))


@app.command
def capability_evidence(index: Path, capabilities: Path, report: Path) -> None:
    """Expand every capability selector into source evidence and oracle-input obligations.

    The report makes broad selectors auditable: every selected entity has a source path and line,
    doctest count, references and module backends. A source-reconciled capability must also have
    at least one selected entity and one independent oracle-input/test obligation.
    """
    result = evidence_logic.write(index, capabilities, report)
    if result["unresolved"]:
        sys.exit("capability evidence is incomplete:\n" + "\n".join(result["unresolved"]))
    print(
        f"Sage {result['revision']['version']} ({result['revision']['commit'][:12]}): "
        f"{result['capabilities']} capabilities with expanded source evidence"
    )


@app.command
def remaining(index: Path, capabilities: Path, categories: Path, worklog: Path, name: str) -> None:
    """List the open entities of one manual section or one package outside the manual.

    An entity is open when it is `unaccounted` (no record selects it) or `scoped` (a record selects
    it, but no source-reconciled worklog batch names its module). Prints one line per entity: its
    id, its state, its kind and the number of doctests in its docstring, separated by tabs. A part
    is closed when the command prints nothing.

    Args:
        index: The index directory (`inventory/sage/index`).
        capabilities: Directory of capability records (`inventory/capabilities`).
        categories: The category inventory (`inventory/categories/sage-categories.toml`).
        worklog: The source-reading worklog (`inventory/reconnaissance-worklog.toml`).
        name: A manual section (`polynomial_rings`), or a package outside the manual as the coverage
            report names it (`sage.rings`).
    """
    try:
        rows = coverage_logic.remaining(index, capabilities, categories, worklog, name)
    except coverage_logic.InventoryError as error:
        sys.exit(str(error))
    for entity, state in rows:
        print(f"{entity.id}\t{state.value}\t{entity.kind.value}\t{entity.doctests}")


@app.command
def graph(capabilities: Path, report: Path) -> None:
    """Derive the capability dependency graph and write it.

    Fails when a `depends_on` entry names no capability record, when an id is stated twice, or when
    the prerequisites form a cycle. Only mandatory prerequisites are edges; an algorithm family that
    consumes an extra input does not become a universal prerequisite.

    Args:
        capabilities: Directory of capability records (`inventory/capabilities`).
        report: The graph file to write (`inventory/dependency-graph.json`).
    """
    _logging()
    try:
        result = graph_logic.build(capabilities)
    except graph_logic.GraphError as error:
        sys.exit(str(error))
    report.write_text(result.model_dump_json(indent=2) + "\n")
    print(
        f"capabilities {result.capabilities}  edges {result.edges}  roots {len(result.roots)}  "
        f"levels {len(result.levels)}  widest level {max((len(level) for level in result.levels), default=0)}"
    )


@app.command
def schema() -> None:
    """Print the JSON Schema of a capability record file (`inventory/capabilities/*.toml`)."""
    print(json.dumps(CapabilityFile.model_json_schema(), indent=2))
