"""The index and the coverage measure, exercised on a small checkout with Sage's source shapes.

`fixtures/checkout` holds a Python module, a Cython module, a module the manual does not list, a
two-document manual section and one package. Every expected value below is read off those files.
"""

from __future__ import annotations

import gzip
import json
import shutil
import subprocess
import tomllib
from pathlib import Path

import pytest
import yaml

from sage_inventory.cli import app
from sage_inventory.coverage import InventoryError, measure, remaining
from sage_inventory.evidence import build as build_evidence
from sage_inventory.graph import GraphError, derive
from sage_inventory.index import CheckoutError, build_index, load_baseline
from sage_inventory.models import Algorithm, Capability, Exactness, Reuse, ReuseStatus
from sage_inventory.reconnaissance import build as build_reconnaissance
from sage_inventory.scan import scan_file

FIXTURES = Path(__file__).parent / "fixtures"
REPOSITORY = Path(__file__).parents[3]


def _git(checkout: Path, *arguments: str) -> str:
    command = ["git", "-C", str(checkout), "-c", "core.hooksPath=/dev/null", *arguments]
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture
def checkout(tmp_path: Path) -> Path:
    """A committed git checkout of the fixture tree."""
    root = tmp_path / "sage"
    shutil.copytree(FIXTURES / "checkout", root)
    _git(root, "init", "--quiet")
    _git(root, "add", "--all")
    _git(root, "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", "commit", "--quiet", "-m", "x")
    return root


@pytest.fixture
def baseline(checkout: Path, tmp_path: Path) -> Path:
    path = tmp_path / "baseline.yaml"
    configuration = yaml.safe_load((REPOSITORY / "inventory/sage/baseline.yaml").read_text())
    configuration["checkout"] = str(checkout)
    path.write_text(yaml.safe_dump(configuration))
    return path


@pytest.fixture
def index(baseline: Path, tmp_path: Path) -> Path:
    output = tmp_path / "index"
    build_index(load_baseline(baseline), output)
    return output


def _entities(index: Path) -> dict[str, dict]:
    with gzip.open(index / "entities.jsonl.gz", "rt") as stream:
        return {record["id"]: record for record in map(json.loads, stream)}


def _lines(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def test_python_entities_are_the_classes_functions_and_methods_but_not_local_functions(index: Path) -> None:
    entities = _entities(index)
    found = {name: (e["kind"], e["public"]) for name, e in entities.items() if e["module"] == "sage.rings.demo_ring"}
    assert found == {
        "sage.rings.demo_ring:DemoRing": ("class", True),
        "sage.rings.demo_ring:DemoRing.order": ("method", True),
        "sage.rings.demo_ring:DemoRing._repr_": ("method", False),
        "sage.rings.demo_ring:DemoRing.Element": ("class", True),
        "sage.rings.demo_ring:DemoRing.Element.inverse": ("method", True),
        "sage.rings.demo_ring:demo_gcd": ("function", True),
        "sage.rings.demo_ring:_private": ("function", False),
    }
    assert entities["sage.rings.demo_ring:DemoRing"]["bases"] == ["Parent", "UniqueRepresentation"]


def test_cython_entities_include_def_and_cpdef_and_omit_cdef(index: Path) -> None:
    entities = _entities(index)
    found = {name: e["kind"] for name, e in entities.items() if e["module"] == "sage.rings.fast_integer"}
    assert found == {
        "sage.rings.fast_integer:FastInteger": "class",
        "sage.rings.fast_integer:FastInteger.xgcd": "method",
        "sage.rings.fast_integer:FastInteger._add_": "method",
        "sage.rings.fast_integer:FastInteger.double": "method",
        "sage.rings.fast_integer:fast_valuation": "function",
        "sage.rings.fast_integer:gcd_list": "function",
    }
    assert entities["sage.rings.fast_integer:FastInteger"]["bases"] == [
        "sage.structure.element.EuclideanDomainElement"
    ]


def test_docstring_facts_belong_to_the_entity_that_states_them(index: Path) -> None:
    entities = _entities(index)
    order = entities["sage.rings.demo_ring:DemoRing.order"]
    assert (order["doctests"], order["algorithm"], order["references"]) == (1, True, ["BCP1997", "Coh1993"])
    ring = entities["sage.rings.demo_ring:DemoRing"]
    assert (ring["doctests"], ring["algorithm"], ring["references"]) == (2, False, [])
    assert entities["sage.rings.fast_integer:FastInteger.xgcd"]["doctests"] == 2
    assert entities["sage.rings.fast_integer:FastInteger"]["doctests"] == 1


def test_module_records_carry_title_engines_features_and_manual_placement(index: Path) -> None:
    modules = {record["module"]: record for record in _lines(index / "modules.jsonl")}
    demo = modules["sage.rings.demo_ring"]
    assert demo["title"] == "Demonstration rings"
    assert demo["backends"] == ["interface:gap", "numpy", "pari"]
    assert demo["features"] == ["database_gap", "sage.libs.pari"]
    assert demo["doctests"] == 4
    assert demo["manual"] == {
        "group": "Mathematics / Basic Rings and Fields",
        "section": "rings_standard",
        "section_title": "Integers and Rational Numbers",
        "headings": ["Integers", "Demonstrations"],
    }
    fast = modules["sage.rings.fast_integer"]
    assert (fast["language"], fast["title"], fast["backends"]) == ("cython", "Fast integers", ["gmp", "pari"])
    assert fast["manual"]["headings"] == ["Integers"]
    assert modules["sage.rings.unlisted"]["manual"] is None


def test_module_records_list_the_indexed_modules_they_import(index: Path) -> None:
    modules = {record["module"]: record for record in _lines(index / "modules.jsonl")}
    # `fast_integer` by a relative, parenthesized import; `unlisted` as a submodule imported by name;
    # `sage.version` by `lazy_import`. `sage.structure.parent` and the engines are outside this checkout.
    assert modules["sage.rings.demo_ring"]["imports"] == [
        "sage.rings.fast_integer",
        "sage.rings.unlisted",
        "sage.version",
    ]
    # Cython: `demo_ring` and `sage.version` inside a function body, `unlisted` by `lazy_import`.
    assert modules["sage.rings.fast_integer"]["imports"] == [
        "sage.rings.demo_ring",
        "sage.rings.unlisted",
        "sage.version",
    ]
    # The docstring of `unlisted` shows import statements as text; the module imports nothing.
    assert modules["sage.rings.unlisted"]["imports"] == []


def test_summary_sections_and_packages_describe_the_checkout(index: Path, checkout: Path) -> None:
    summary = json.loads((index / "summary.json").read_text())
    assert summary == {
        "revision": {"version": "11.0.beta5", "commit": _git(checkout, "rev-parse", "HEAD")},
        "modules": 4,
        "manual_modules": 2,
        "entities": 14,
        "public_entities": 11,
        "manual_public_entities": 10,
        "doctests": 7,
        "packages": 1,
    }
    sections = {record["section"]: record for record in _lines(index / "sections.jsonl")}
    assert (sections["rings_standard"]["modules"], sections["rings_standard"]["public_entities"]) == (2, 10)
    assert (sections["references"]["group"], sections["references"]["modules"]) == ("General Information", 0)
    assert _lines(index / "packages.jsonl") == [
        {
            "name": "flint",
            "type": "standard",
            "version": "3.4.0",
            "license": "FLINT is licensed GPL v2+.",
            "website": "http://groups.google.co.uk/group/flint-devel",
        }
    ]


def test_index_refuses_a_checkout_with_uncommitted_source_changes(baseline: Path, checkout: Path, tmp_path: Path) -> None:
    (checkout / "src/sage/rings/unlisted.py").write_text("def changed(a):\n    return a\n")
    with pytest.raises(CheckoutError):
        build_index(load_baseline(baseline), tmp_path / "index")


def _worklog(tmp_path: Path, index: Path, *batches: tuple[str, str, list[str]]) -> Path:
    """A worklog for the fixture index: one batch per `(id, status, modules)`."""
    commit = json.loads((index / "summary.json").read_text())["revision"]["commit"]
    text = f'version = 1\nbaseline_version = "11.0.beta5"\nbaseline_commit = "{commit}"\n'
    for identifier, status, modules in batches:
        text += (
            f'\n[[batch]]\nid = "{identifier}"\nsections = ["rings_standard"]\nmodules = {json.dumps(modules)}\n'
            f'status = "{status}"\nsource_files = []\nmanual_files = []\nrecords = []\ntests = []\n'
            'evidence = "fixture"\nopen_questions = []\n'
        )
    path = tmp_path / "worklog.toml"
    path.write_text(text)
    return path


def _categories(tmp_path: Path, *named: str) -> Path:
    path = tmp_path / "categories.toml"
    path.write_text("".join(f'[[operation]]\nid = "{name}"\nsage = "{name}"\n\n' for name in named))
    return path


@pytest.fixture
def worklog(index: Path, tmp_path: Path) -> Path:
    """`fast_integer` has been read in full; `demo_ring` is being read."""
    return _worklog(
        tmp_path,
        index,
        ("read-fast-integer", "source-reconciled", ["sage.rings.fast_integer"]),
        ("read-demo-ring", "in-progress", ["sage.rings.demo_ring"]),
    )


def _states(index: Path, worklog: Path, categories: Path) -> dict[str, str]:
    _, rows = build_reconnaissance(index, FIXTURES / "capabilities", categories, worklog)
    return {row["id"]: row["state"] for row in rows}


def test_a_record_closes_an_entity_only_in_a_module_that_a_source_reconciled_batch_names(
    index: Path, worklog: Path, tmp_path: Path
) -> None:
    # The capability selects xgcd, gcd_list and demo_gcd; the exclusion selects Element and Element.inverse.
    states = _states(index, worklog, _categories(tmp_path))
    assert states == {
        "sage.rings.fast_integer:FastInteger": "unaccounted",
        "sage.rings.fast_integer:FastInteger.xgcd": "reconciled",
        "sage.rings.fast_integer:FastInteger._add_": "unaccounted",
        "sage.rings.fast_integer:FastInteger.double": "unaccounted",
        "sage.rings.fast_integer:fast_valuation": "unaccounted",
        "sage.rings.fast_integer:gcd_list": "reconciled",
        # `demo_ring` is only in progress: its records scope entities and close none.
        "sage.rings.demo_ring:DemoRing": "unaccounted",
        "sage.rings.demo_ring:DemoRing.order": "unaccounted",
        "sage.rings.demo_ring:DemoRing._repr_": "unaccounted",
        "sage.rings.demo_ring:DemoRing.Element": "scoped",
        "sage.rings.demo_ring:DemoRing.Element.inverse": "scoped",
        "sage.rings.demo_ring:demo_gcd": "scoped",
        "sage.rings.demo_ring:_private": "unaccounted",
        # Outside the manual, and still in the denominator.
        "sage.rings.unlisted:stray": "unaccounted",
    }
    read = _worklog(tmp_path, index, ("read-both", "source-reconciled", ["sage.rings.fast_integer", "sage.rings.demo_ring"]))
    states = _states(index, read, _categories(tmp_path))
    assert (
        states["sage.rings.demo_ring:demo_gcd"],
        states["sage.rings.demo_ring:DemoRing.Element"],
        states["sage.rings.demo_ring:DemoRing.order"],
    ) == ("reconciled", "excluded", "unaccounted")


def test_category_records_close_the_entities_they_name(index: Path, worklog: Path, tmp_path: Path) -> None:
    categories = _categories(tmp_path, "sage.rings.fast_integer:fast_valuation", "sage.rings.demo_ring:DemoRing.order")
    states = _states(index, worklog, categories)
    assert states["sage.rings.fast_integer:fast_valuation"] == "category-record"
    assert states["sage.rings.demo_ring:DemoRing.order"] == "category-record"


def test_coverage_counts_every_indexed_entity_by_state(index: Path, worklog: Path, tmp_path: Path) -> None:
    report = measure(index, FIXTURES / "capabilities", FIXTURES / "reuse", _categories(tmp_path), worklog)
    # 14 entities, 11 public, 7 doctests; the states are those of the test above.
    total = report.total
    assert (total.entities, total.public_entities, total.doctests) == (14, 11, 7)
    assert (total.unaccounted, total.scoped, total.reconciled, total.excluded, total.category_record) == (9, 3, 2, 0, 0)
    assert (report.modules, report.credited_modules) == (4, 1)
    assert (report.capabilities, report.attached_to_catalogue, report.exclusions) == (1, 1, 1)
    (section,) = report.sections
    assert (section.part, section.entities, section.unaccounted, section.scoped, section.reconciled) == (
        "rings_standard",
        13,
        8,
        3,
        2,
    )
    (package,) = report.unlisted
    assert (package.part, package.entities, package.unaccounted) == ("sage.rings", 1, 1)


def test_remaining_lists_the_open_entities_of_a_section_or_package(index: Path, worklog: Path, tmp_path: Path) -> None:
    categories = _categories(tmp_path)
    rows = remaining(index, FIXTURES / "capabilities", categories, worklog, "rings_standard")
    listed = {entity.id: state.value for entity, state in rows}
    assert len(listed) == 11
    assert listed["sage.rings.demo_ring:demo_gcd"] == "scoped"
    assert listed["sage.rings.fast_integer:FastInteger._add_"] == "unaccounted"
    assert "sage.rings.fast_integer:FastInteger.xgcd" not in listed
    ((stray, state),) = remaining(index, FIXTURES / "capabilities", categories, worklog, "sage.rings")
    assert (stray.id, state.value) == ("sage.rings.unlisted:stray", "unaccounted")
    with pytest.raises(InventoryError):
        remaining(index, FIXTURES / "capabilities", categories, worklog, "no_such_section")


def test_remaining_command_prints_one_line_per_open_entity(
    index: Path, worklog: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    arguments = [str(index), str(FIXTURES / "capabilities"), str(_categories(tmp_path)), str(worklog), "sage.rings"]
    app(["remaining", *arguments], result_action="return_value")
    assert capsys.readouterr().out == "sage.rings.unlisted:stray\tunaccounted\tfunction\t0\n"


@pytest.mark.parametrize(
    ("status", "modules"),
    [
        ("source-reconciled", ["sage.rings"]),
        ("source-reconciled", ["sage.rings.*"]),
        ("in-progress", ["sage.no_such_package.*"]),
    ],
    ids=["reconciled-package-name", "reconciled-pattern", "pattern-matches-nothing"],
)
def test_worklog_credits_only_exact_indexed_modules(
    index: Path, tmp_path: Path, status: str, modules: list[str]
) -> None:
    worklog = _worklog(tmp_path, index, ("claim", status, modules))
    with pytest.raises(InventoryError):
        measure(index, FIXTURES / "capabilities", FIXTURES / "reuse", _categories(tmp_path), worklog)


def test_worklog_must_describe_the_indexed_commit(index: Path, worklog: Path, tmp_path: Path) -> None:
    other = tmp_path / "other.toml"
    commit = json.loads((index / "summary.json").read_text())["revision"]["commit"]
    other.write_text(worklog.read_text().replace(commit, "0" * 40))
    with pytest.raises(InventoryError):
        measure(index, FIXTURES / "capabilities", FIXTURES / "reuse", _categories(tmp_path), other)


def test_capability_evidence_expands_selectors_to_source_and_oracle_rows(index: Path) -> None:
    report = build_evidence(index, FIXTURES / "capabilities")
    assert report["unresolved"] == []
    (record,) = [row for row in report["records"] if row["id"] == "euclidean.gcd"]
    assert {entity["id"] for entity in record["source_entities"]} == {
        "sage.rings.fast_integer:FastInteger.xgcd",
        "sage.rings.fast_integer:gcd_list",
        "sage.rings.demo_ring:demo_gcd",
    }
    assert all(entity["source_path"].startswith("src/sage/rings/") for entity in record["source_entities"])
    assert record["oracle_input_status"] == "source-doctest-backed"


def _records_with(tmp_path: Path, old: str, new: str) -> Path:
    directory = tmp_path / "capabilities"
    directory.mkdir()
    text = (FIXTURES / "capabilities/rings.toml").read_text()
    assert old in text
    (directory / "rings.toml").write_text(text.replace(old, new))
    return directory


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ('"sage.rings.*:*gcd*"', '"sage.rings.*:*resultant*"'),
        ("depends_on = []", 'depends_on = ["euclidean.division"]'),
        ('components = ["mathlib.int-gcd"]', 'components = ["mathlib.nat-gcd"]'),
        ('catalogue = ["mor.sets.gcd"]', 'catalogue = ["mor.sets.lcm"]'),
    ],
    ids=["selector-matches-nothing", "unknown-dependency", "unknown-reuse-component", "unknown-catalogue-id"],
)
def test_coverage_rejects_records_that_refer_to_nothing(
    index: Path, worklog: Path, tmp_path: Path, old: str, new: str
) -> None:
    with pytest.raises(InventoryError):
        measure(index, _records_with(tmp_path, old, new), FIXTURES / "reuse", _categories(tmp_path), worklog)


def test_coverage_command_writes_the_report_and_fails_on_inconsistent_records(
    index: Path, worklog: Path, tmp_path: Path
) -> None:
    report = tmp_path / "coverage.json"
    categories = str(_categories(tmp_path))
    tail = [str(FIXTURES / "reuse"), categories, str(worklog), str(report)]
    app(["coverage", str(index), str(FIXTURES / "capabilities"), *tail], result_action="return_value")
    assert json.loads(report.read_text())["total"]["unaccounted"] == 9

    broken = _records_with(tmp_path, "depends_on = []", 'depends_on = ["euclidean.division"]')
    with pytest.raises(SystemExit) as stopped:
        app(["coverage", str(index), str(broken), *tail], result_action="return_value")
    assert stopped.value.code not in (0, None)


def test_reconnaissance_ledger_rows_join_modules_to_batches_and_importing_sections(
    index: Path, worklog: Path, tmp_path: Path
) -> None:
    ledger, rows = build_reconnaissance(index, FIXTURES / "capabilities", _categories(tmp_path), worklog)
    modules = {row["module"]: row for row in ledger["module_rows"]}
    assert modules["sage.rings.fast_integer"]["batches"] == ["read-fast-integer"]
    assert modules["sage.rings.demo_ring"]["batches"] == []
    # `stray` is outside the manual; both documented modules of `rings_standard` import it.
    stray = modules["sage.rings.unlisted"]
    assert (stray["manual"], stray["part"], stray["imported_by_sections"]) == (False, "sage.rings", ["rings_standard"])
    assert (stray["entities"], stray["unaccounted"]) == (1, 1)
    assert len(rows) == ledger["total"]["entities"] == 14


def test_cython_parser_reads_sage_integer_source() -> None:
    """`Integer` in the local Sage checkout: a `cdef class` over `EuclideanDomainElement`.

    Its `xgcd` is a decorated `def`; `set_from_Integer` is a module-level `cdef` function.
    """
    root = load_baseline(REPOSITORY / "inventory/sage/baseline.yaml").root()
    scan = scan_file("sage.rings.integer", root / "src/sage/rings/integer.pyx", root / "src")
    entities = {entity.qualname: entity for entity in scan.entities}
    assert entities["Integer"].bases == ("sage.structure.element.EuclideanDomainElement",)
    assert entities["Integer.xgcd"].kind == "method"
    assert "set_from_Integer" not in entities
    assert {"gmp", "flint", "pari"} <= set(scan.backends)


def _capability(identifier: str, depends_on: tuple[str, ...]) -> Capability:
    """A record whose only interesting field here is its prerequisites."""
    return Capability(
        id=identifier,
        title=identifier,
        statement="Return the value.",
        domain="An integer.",
        contract="Z -> Z.",
        exactness=Exactness.EXACT,
        algorithms=(Algorithm(family="Direct", sources=("fixture",)),),
        depends_on=depends_on,
        sage=(f"fixture:{identifier}",),
        catalogue=(),
        tests=("fixture",),
        reuse=Reuse(status=ReuseStatus.MISSING, components=(), evidence="fixture"),
        backends=(),
        references=(),
    )


def test_dependency_graph_levels_are_a_build_order() -> None:
    """A prerequisite edge puts the dependent one level above every one of its prerequisites.

    `c` depends on `a` and `b`, `b` depends on `a`: the levels are `a`, then `b`, then `c`, and the
    two roots that share no dependent stay at level 0.
    """
    dependencies = derive((_capability("fixture.a", ()), _capability("fixture.b", ("fixture.a",)),
                           _capability("fixture.c", ("fixture.a", "fixture.b"))))
    assert dependencies.levels == (("fixture.a",), ("fixture.b",), ("fixture.c",))
    assert dependencies.edges == 3
    assert dependencies.roots == ("fixture.a",)
    assert dependencies.nodes[2].dependents == ()
    assert dependencies.nodes[0].dependents == ("fixture.b", "fixture.c")


def test_dependency_graph_rejects_a_cycle_and_an_unknown_prerequisite() -> None:
    """A cycle means an alternative was recorded as a prerequisite; an unknown id is a typo."""
    with pytest.raises(GraphError, match="cycle: fixture.a -> fixture.b -> fixture.a"):
        derive((_capability("fixture.a", ("fixture.b",)), _capability("fixture.b", ("fixture.a",))))
    with pytest.raises(GraphError, match="names no capability record: fixture.missing"):
        derive((_capability("fixture.a", ("fixture.missing",)),))


def test_every_recorded_backend_names_a_reference_engine() -> None:
    """A backend token is a name another program answers to, so it resolves to a reference engine.

    The engines manifest lists each engine's id and the names Sage calls it by; a capability record
    that names neither is claiming an implementation without a source for its licence or version.
    """
    engines = tomllib.loads((REPOSITORY / "inventory/references/engines.toml").read_text())["engine"]
    names = {engine["id"] for engine in engines}
    names.update(name for engine in engines for name in engine["sage_backends"])
    records = [
        record
        for path in sorted((REPOSITORY / "inventory/capabilities").glob("*.toml"))
        for record in tomllib.loads(path.read_text()).get("capability", [])
    ]
    unresolved = {
        (record["id"], backend)
        for record in records
        for backend in record.get("backends", [])
        if backend not in names
    }
    assert not unresolved, sorted(unresolved)
