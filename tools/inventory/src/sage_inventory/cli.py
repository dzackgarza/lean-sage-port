"""Command line of the Sage capability inventory."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from cyclopts import App

from sage_inventory import coverage as coverage_logic
from sage_inventory import index as index_logic
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
def coverage(index: Path, capabilities: Path, reuse: Path, report: Path) -> None:
    """Validate the capability records and write the coverage report.

    Fails when a record refers to an unknown capability or reuse component, or when a selector
    matches nothing in the index.

    Args:
        index: The index directory (`inventory/sage/index`).
        capabilities: Directory of capability records (`inventory/capabilities`).
        reuse: Directory of reuse surveys (`inventory/reuse`).
        report: The report file to write (`inventory/coverage.json`).
    """
    _logging()
    try:
        result = coverage_logic.measure(index, capabilities, reuse)
    except coverage_logic.InventoryError as error:
        sys.exit(f"capability inventory is inconsistent:\n{error}")
    report.write_text(result.model_dump_json(indent=2) + "\n")
    print(f"Sage {result.revision.version} ({result.revision.commit[:12]}): {result.public_entities} documented public entities")
    print(f"  by capability {result.by_capability}  excluded {result.excluded}  unaccounted {result.unaccounted}")
    for section in result.sections:
        print(
            f"  {section.section:34} {section.public_entities:6} "
            f"cap {section.by_capability:6} excl {section.excluded:6} open {section.unaccounted:6}"
        )


@app.command
def unaccounted(index: Path, capabilities: Path, name: str) -> None:
    """List the public entities of one section that no capability or exclusion selects.

    Prints one line per entity: its id, its kind and the number of doctests in its docstring,
    separated by tabs.

    Args:
        index: The index directory (`inventory/sage/index`).
        capabilities: Directory of capability records (`inventory/capabilities`).
        name: A manual section (`polynomial_rings`), or a package outside the manual as the coverage
            report names it (`sage.rings`).
    """
    try:
        entities = coverage_logic.unaccounted(index, capabilities, name)
    except coverage_logic.InventoryError as error:
        sys.exit(str(error))
    for entity in entities:
        print(f"{entity.id}\t{entity.kind.value}\t{entity.doctests}")


@app.command
def schema() -> None:
    """Print the JSON Schema of a capability record file (`inventory/capabilities/*.toml`)."""
    print(json.dumps(CapabilityFile.model_json_schema(), indent=2))
