"""Record types of the inventory. These models are the specification of every file the tool reads or writes."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class Strict(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)


# --- baseline configuration (inventory/sage/baseline.yaml) -------------------------------------


class SourcePaths(Strict):
    source: str
    manual: str
    packages: str
    version: str
    """The file that assigns the release string, `version = '11.0.beta5'`."""


class Baseline(Strict):
    """The Sage source tree the inventory describes: a git checkout on this machine."""

    checkout: str
    paths: SourcePaths

    def root(self) -> Path:
        return Path(self.checkout).expanduser()


class Revision(Strict):
    """The state of the checkout that an index or a report describes."""

    version: str
    """Sage's release string at that commit."""
    commit: str = Field(pattern=r"^[0-9a-f]{40}$")


# --- the automated index (inventory/sage/index/) -----------------------------------------------


class EntityKind(StrEnum):
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"


class Entity(Strict):
    """One class, module-level function or method of a Sage module."""

    id: str
    """`<module>:<qualified name>`, for example `sage.rings.integer:Integer.gcd`."""
    module: str
    qualname: str
    kind: EntityKind
    public: bool
    """No component of the qualified name starts with an underscore."""
    line: int
    bases: tuple[str, ...]
    doctests: int
    """Number of `sage:` prompts in the entity's own docstring."""
    algorithm: bool
    """The docstring has an `ALGORITHM:` section."""
    references: tuple[str, ...]
    """Citation keys such as `Coh1993`, from `[Coh1993]_`."""


class ManualPlacement(Strict):
    """Where the reference manual documents a module."""

    group: str
    """Thematic group of the manual's front page, for example `Mathematics / Linear Algebra`."""
    section: str
    """Manual section directory, for example `matrices`."""
    section_title: str
    headings: tuple[str, ...]
    """Headings above the module's toctree entry inside the section."""


class Module(Strict):
    module: str
    path: str
    language: str
    """`python` or `cython`."""
    title: str
    manual: ManualPlacement | None
    classes: int
    functions: int
    methods: int
    public_entities: int
    doctests: int
    imports: tuple[str, ...]
    """Indexed modules this module imports: at module level, in function bodies, and by `lazy_import`."""
    backends: tuple[str, ...]
    """External engines and libraries the module imports."""
    features: tuple[str, ...]
    """Optional-feature tags of its doctests (`# optional - x`, `# needs x`)."""


class Package(Strict):
    """One package of the Sage distribution (`build/pkgs/<name>`)."""

    name: str
    type: str
    version: str
    license: str
    website: str


class Section(Strict):
    section: str
    group: str
    title: str
    modules: int
    public_entities: int
    doctests: int


class IndexSummary(Strict):
    revision: Revision
    modules: int
    manual_modules: int
    entities: int
    public_entities: int
    manual_public_entities: int
    doctests: int
    packages: int


# --- curated capability records (inventory/capabilities/*.toml) --------------------------------


class Exactness(StrEnum):
    EXACT = "exact"
    APPROXIMATE = "approximate"
    HEURISTIC = "heuristic"
    CONDITIONAL = "conditional"


class ReuseStatus(StrEnum):
    REUSABLE = "reusable"
    ADAPTABLE = "adaptable"
    FORMALIZED_NOT_EXECUTABLE = "formalized-not-executable"
    SPECIFIED_UNIMPLEMENTED = "specified-unimplemented"
    MISSING = "missing"


class Algorithm(Strict):
    family: str
    sources: tuple[str, ...]
    """Reference implementations and literature, for example `FLINT fmpz_poly_gcd`, `[Coh1993] Alg. 3.2.10`."""


class Reuse(Strict):
    status: ReuseStatus
    components: tuple[str, ...]
    """Component ids of `inventory/reuse/*.toml`, or fully qualified Lean declarations."""
    evidence: str


class Capability(Strict):
    """One mathematical capability: an intrinsic operation or construction, not a Sage method name."""

    id: str = Field(pattern=r"^[a-z0-9-]+(\.[a-z0-9-]+)+$")
    title: str
    statement: str
    """The operation or construction, stated mathematically."""
    domain: str
    """Hypotheses, coefficient rings and objects it applies to."""
    contract: str
    """Input and output as mathematical types, and the structure the result retains."""
    exactness: Exactness
    exactness_notes: str = ""
    generalizes: tuple[str, ...] = ()
    """Capability ids that are specializations of this generic operation."""
    algorithms: tuple[Algorithm, ...]
    depends_on: tuple[str, ...]
    """Capability ids this one consumes."""
    sage: tuple[str, ...]
    """Selectors of the Sage entities this capability accounts for (see `coverage.select`)."""
    catalogue: tuple[str, ...]
    """Ids of the `lean-categories` catalogue objects and operations that this capability computes
    (`obj.rings.integers`, `mor.sets.gcd`). Empty: the catalogue has none, a gap to report to its owner."""
    tests: tuple[str, ...]
    """Independent sources of expected values: citations, theorems, databases, second oracles."""
    reuse: Reuse
    backends: tuple[str, ...]
    """Engines Sage delegates this capability to."""
    references: tuple[str, ...]
    license_notes: str = ""


class ExclusionReason(StrEnum):
    INFRASTRUCTURE = "infrastructure"
    """Programming facilities of Sage itself: no mathematical capability."""
    EXTERNAL_INTERFACE = "external-interface"
    """A binding to another system. The capability it reaches is recorded where Sage uses it."""
    PRESENTATION = "presentation"
    """Rendering only: plotting, typesetting, notebook display."""
    DATA = "data"
    """A shipped table or database, not an algorithm."""
    DEPRECATED = "deprecated"


class Exclusion(Strict):
    """Sage entities the target does not reproduce, with the reason."""

    id: str
    reason: ExclusionReason
    rationale: str
    sage: tuple[str, ...]


class CapabilityFile(Strict):
    domain: str
    """Planning partition this file belongs to."""
    capability: tuple[Capability, ...] = ()
    exclusion: tuple[Exclusion, ...] = ()


# --- coverage report (inventory/coverage.json) -------------------------------------------------


class SectionCoverage(Strict):
    section: str
    group: str
    public_entities: int
    by_capability: int
    excluded: int
    unaccounted: int
    doctests: int
    doctests_by_capability: int


class PackageCoverage(Strict):
    """Public entities of the modules of one package that the reference manual does not list."""

    package: str
    public_entities: int
    by_capability: int
    excluded: int
    unaccounted: int


class CoverageReport(Strict):
    """The totals count documented modules. `unlisted` counts the rest of the source, by package."""

    revision: Revision
    capabilities: int
    attached_to_catalogue: int
    """Capabilities that name at least one catalogue id."""
    exclusions: int
    public_entities: int
    by_capability: int
    excluded: int
    unaccounted: int
    sections: tuple[SectionCoverage, ...]
    unlisted: tuple[PackageCoverage, ...]
