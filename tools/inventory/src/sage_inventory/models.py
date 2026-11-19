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


class CapabilityStatus(StrEnum):
    SOURCE_RECONCILED = "source-reconciled"
    SCOPE_ONLY = "scope-only"


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
    status: CapabilityStatus = CapabilityStatus.SOURCE_RECONCILED
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


# --- reconnaissance worklog (inventory/reconnaissance-worklog.toml) ----------------------------


class BatchStatus(StrEnum):
    IN_PROGRESS = "in-progress"
    """Source reading has started; the batch credits no module."""
    SCOPE_ONLY = "scope-only"
    """Records were written or edited without a recorded reading of named modules; no credit."""
    SOURCE_RECONCILED = "source-reconciled"
    """Every module in `modules` was read in full and its records were reconciled with the source."""


class Batch(Strict):
    """One batch of source reading. Only a source-reconciled batch credits modules, and only by exact name."""

    id: str
    sections: tuple[str, ...]
    modules: tuple[str, ...] = ()
    """Module names, or shell-style module patterns in a batch that is not source-reconciled."""
    status: BatchStatus
    started: str | None = None
    source_files: tuple[str, ...]
    manual_files: tuple[str, ...]
    records: tuple[str, ...]
    reuse_records: tuple[str, ...] = ()
    tests: tuple[str, ...]
    evidence: str
    open_questions: tuple[str, ...]


class Worklog(Strict):
    version: int
    baseline_version: str
    baseline_commit: str = Field(pattern=r"^[0-9a-f]{40}$")
    batch: tuple[Batch, ...]


# --- coverage report (inventory/coverage.json) -------------------------------------------------


class State(StrEnum):
    """Reconnaissance state of one indexed entity. The last three are closed; the first two are open."""

    UNACCOUNTED = "unaccounted"
    """No record selects the entity."""
    SCOPED = "scoped"
    """A record selects the entity, but no source-reconciled batch names its module, or the record is scope-only."""
    RECONCILED = "reconciled"
    """A source-reconciled capability selects it and a source-reconciled batch names its module."""
    EXCLUDED = "excluded"
    """An exclusion selects it and a source-reconciled batch names its module."""
    CATEGORY_RECORD = "category-record"
    """A category or operation record of `inventory/categories/` names it."""


OPEN_STATES = frozenset({State.UNACCOUNTED, State.SCOPED})


class StateCounts(Strict):
    """Entities of one part of the source, by reconnaissance state."""

    entities: int
    public_entities: int
    unaccounted: int
    scoped: int
    reconciled: int
    excluded: int
    category_record: int
    doctests: int


class PartCoverage(StateCounts):
    """One manual section, or one two-level package for the modules that the manual does not list."""

    part: str
    group: str
    """Thematic group of the manual's front page; empty for a package outside the manual."""


class CoverageReport(Strict):
    """Counts over every indexed entity of the checkout: `sections` for manual modules, `unlisted` for the rest."""

    revision: Revision
    capabilities: int
    attached_to_catalogue: int
    """Capabilities that name at least one catalogue id."""
    exclusions: int
    credited_modules: int
    """Modules that a source-reconciled worklog batch names."""
    modules: int
    total: StateCounts
    sections: tuple[PartCoverage, ...]
    unlisted: tuple[PartCoverage, ...]


# --- dependency graph (inventory/dependency-graph.json) ----------------------------------------


class GraphNode(Strict):
    """One capability, with the edges the derivation resolved from its `depends_on` field."""

    id: str
    level: int
    """Longest path length from a capability with no prerequisite; 0 for a root."""
    depends_on: tuple[str, ...]
    dependents: tuple[str, ...]
    reuse: ReuseStatus
    catalogue: tuple[str, ...]
    algorithm_families: int


class DependencyGraph(Strict):
    """The edge set is the mandatory prerequisites only, never an algorithm alternative.

    A capability whose algorithm family consumes an additional input records that input in the
    algorithm's own specification, so the graph stays acyclic and the levels are a build order.
    """

    capabilities: int
    edges: int
    roots: tuple[str, ...]
    levels: tuple[tuple[str, ...], ...]
    nodes: tuple[GraphNode, ...]
