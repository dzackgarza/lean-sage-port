"""The index and the coverage measure, exercised on a small checkout with Sage's source shapes.

`fixtures/checkout` holds a Python module, a Cython module, a module the manual does not list, a
two-document manual section and one package. Every expected value below is read off those files.
"""

from __future__ import annotations

import gzip
import json
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from sage_inventory.cli import app
from sage_inventory.coverage import InventoryError, measure, unaccounted
from sage_inventory.index import CheckoutError, build_index, load_baseline
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


def test_coverage_counts_documented_public_entities_by_capability_exclusion_and_remainder(index: Path) -> None:
    report = measure(index, FIXTURES / "capabilities", FIXTURES / "reuse")
    # Documented and public: 5 in fast_integer, 5 in demo_ring. `stray` is outside the manual.
    # The capability selects xgcd, gcd_list and demo_gcd; the exclusion selects Element and Element.inverse.
    assert (report.public_entities, report.by_capability, report.excluded, report.unaccounted) == (10, 3, 2, 5)
    assert (report.capabilities, report.exclusions) == (1, 1)
    (section,) = report.sections
    assert (section.section, section.doctests, section.doctests_by_capability) == ("rings_standard", 7, 3)
    # `sage.rings.unlisted:stray` is public, outside the manual, and selected by no record.
    (package,) = report.unlisted
    assert (package.package, package.public_entities, package.unaccounted) == ("sage.rings", 1, 1)


def test_unaccounted_lists_the_entities_of_a_section_that_no_record_selects(index: Path) -> None:
    # The capability selects xgcd, gcd_list and demo_gcd; the exclusion selects Element and Element.inverse.
    listed = {entity.id for entity in unaccounted(index, FIXTURES / "capabilities", "rings_standard")}
    assert listed == {
        "sage.rings.fast_integer:FastInteger",
        "sage.rings.fast_integer:FastInteger.double",
        "sage.rings.fast_integer:fast_valuation",
        "sage.rings.demo_ring:DemoRing",
        "sage.rings.demo_ring:DemoRing.order",
    }
    # A module outside the manual is addressed by its package.
    (stray,) = unaccounted(index, FIXTURES / "capabilities", "sage.rings")
    assert stray.id == "sage.rings.unlisted:stray"
    with pytest.raises(InventoryError):
        unaccounted(index, FIXTURES / "capabilities", "no_such_section")


def test_unaccounted_command_prints_one_line_per_entity(index: Path, capsys: pytest.CaptureFixture[str]) -> None:
    app(["unaccounted", str(index), str(FIXTURES / "capabilities"), "sage.rings"], result_action="return_value")
    assert capsys.readouterr().out == "sage.rings.unlisted:stray\tfunction\t0\n"


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
    ],
    ids=["selector-matches-nothing", "unknown-dependency", "unknown-reuse-component"],
)
def test_coverage_rejects_records_that_refer_to_nothing(index: Path, tmp_path: Path, old: str, new: str) -> None:
    with pytest.raises(InventoryError):
        measure(index, _records_with(tmp_path, old, new), FIXTURES / "reuse")


def test_coverage_command_writes_the_report_and_fails_on_inconsistent_records(index: Path, tmp_path: Path) -> None:
    report = tmp_path / "coverage.json"
    arguments = [str(FIXTURES / "reuse"), str(report)]
    app(["coverage", str(index), str(FIXTURES / "capabilities"), *arguments], result_action="return_value")
    assert json.loads(report.read_text())["unaccounted"] == 5

    broken = _records_with(tmp_path, "depends_on = []", 'depends_on = ["euclidean.division"]')
    with pytest.raises(SystemExit) as stopped:
        app(["coverage", str(index), str(broken), *arguments], result_action="return_value")
    assert stopped.value.code not in (0, None)


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
