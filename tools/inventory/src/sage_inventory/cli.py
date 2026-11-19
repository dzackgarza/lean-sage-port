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


@app.command
def coverage(
    index: Path, capabilities: Path, reuse: Path, report: Path, categories: Path | None = None
) -> None:
    """Validate the capability records and write the coverage report.

    Fails when a record refers to an unknown capability, reuse component or catalogue id, or when a
    selector matches nothing in the index.

    Args:
        index: The index directory (`inventory/sage/index`).
        capabilities: Directory of capability records (`inventory/capabilities`).
        reuse: Directory of reuse surveys (`inventory/reuse`).
        report: The report file to write (`inventory/coverage.json`).
        categories: The category inventory (`inventory/categories/sage-categories.toml`). Its
            category and operation records account for the entities of the `categories` section.
    """
    _logging()
    try:
        result = coverage_logic.measure(index, capabilities, reuse, categories)
    except coverage_logic.InventoryError as error:
        sys.exit(f"capability inventory is inconsistent:\n{error}")
    report.write_text(result.model_dump_json(indent=2) + "\n")
    print(f"Sage {result.revision.version} ({result.revision.commit[:12]}): {result.public_entities} documented public entities")
    print(
        f"  by capability {result.by_capability}  excluded {result.excluded}  "
        f"by category record {result.by_category_record}  unaccounted {result.unaccounted}"
    )
    print(f"  capabilities {result.capabilities}  attached to the catalogue {result.attached_to_catalogue}")
    for section in result.sections:
        print(
            f"  {section.section:34} {section.public_entities:6} "
            f"cap {section.by_capability:6} excl {section.excluded:6} "
            f"cat {section.by_category_record:6} open {section.unaccounted:6}"
        )


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
def reconnaissance(index: Path, domains: Path, capabilities: Path, categories: Path, report: Path) -> None:
    """Write the exhaustive entity-level reconnaissance ledger.

    Args:
        index: The indexed Sage checkout (`inventory/sage/index`).
        domains: The manual section taxonomy (`inventory/domains.toml`).
        capabilities: Curated capability records (`inventory/capabilities`).
        categories: Category framework records (`inventory/categories/sage-categories.toml`).
        report: The reconnaissance report (`inventory/reconnaissance.json`).
    """
    result = reconnaissance_logic.write(index, domains, capabilities, categories, report)
    counts = {
        accounting: sum(section.get(accounting, 0) for section in result["sections"])
        for accounting in ("capability", "category-record", "exclusion", "unaccounted")
    }
    print(
        f"Sage {result['revision']['version']} ({result['revision']['commit'][:12]}): "
        f"{result['public_entities']} public manual entities"
    )
    print("  " + "  ".join(f"{key} {value}" for key, value in counts.items()))


@app.command
def reconnaissance_scope(index: Path, domains: Path, capabilities: Path, categories: Path, report: Path) -> None:
    """Write the module-level scope and progress ledger without closing semantic work."""
    from sage_inventory import scope as scope_logic

    result = scope_logic.write(index, domains, capabilities, categories, report)
    print(
        f"Sage {result['revision']['version']} ({result['revision']['commit'][:12]}): "
        f"{result['indexed_modules']} indexed public modules"
    )
    print(
        f"  entities {result['public_entities']}  accounted {result['accounted_entities']}  "
        f"open {result['open_entities']}  open modules {result['open_modules']}"
    )


@app.command
def capability_evidence(index: Path, capabilities: Path, report: Path) -> None:
    """Expand every capability selector into source evidence and oracle-input obligations.

    The report makes broad selectors auditable: every selected entity has a source path and line,
    doctest count, references and module backends. A source-reconciled capability must also have
    at least one selected public entity and one independent oracle-input/test obligation.
    """
    result = evidence_logic.write(index, capabilities, report)
    if result["unresolved"]:
        sys.exit("capability evidence is incomplete:\n" + "\n".join(result["unresolved"]))
    print(
        f"Sage {result['revision']['version']} ({result['revision']['commit'][:12]}): "
        f"{result['capabilities']} capabilities with expanded source evidence"
    )


@app.command
def unaccounted(index: Path, capabilities: Path, name: str, categories: Path | None = None) -> None:
    """List the public entities of one section that no capability or exclusion selects.

    Prints one line per entity: its id, its kind and the number of doctests in its docstring,
    separated by tabs.

    Args:
        index: The index directory (`inventory/sage/index`).
        capabilities: Directory of capability records (`inventory/capabilities`).
        name: A manual section (`polynomial_rings`), or a package outside the manual as the coverage
            report names it (`sage.rings`).
        categories: The category inventory (`inventory/categories/sage-categories.toml`), whose
            records account for the entities of the `categories` section.
    """
    try:
        entities = coverage_logic.unaccounted(index, capabilities, name, categories)
    except coverage_logic.InventoryError as error:
        sys.exit(str(error))
    for entity in entities:
        print(f"{entity.id}\t{entity.kind.value}\t{entity.doctests}")


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
