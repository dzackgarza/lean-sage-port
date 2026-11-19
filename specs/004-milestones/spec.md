# Feature Specification: Dependency-ordered milestone roadmap

**Feature Branch**: `004-milestones`
**Created**: 2026-11-17
**Status**: Draft
**Scope**: All the functionality of the Sage source, partitioned into independently acceptable milestones.

## User Scenarios & Testing

### User Story 1 — Determine what must be built before what (Priority: P1)

An implementer wants to start work on a mathematical domain. They need to know which
prior milestones must be complete before theirs can begin, what capability records already
exist, what reuse decisions are already established, and what acceptance conditions close the
milestone — without re-doing the reconnaissance executed under
`specs/001-native-computation/` and summarized by the M0 roadmap gate.

**Why this priority**: Without a clear dependency order, implementers either block each other
(by starting on something whose prerequisites aren't ready) or duplicate work (by re-surveying
reuse evidence already in `inventory/reuse/`). This is the primary consumer value of the
milestone structure.

**Independent Test**: Given any two milestones A and B where A is listed as a prerequisite of
B, there exists at least one capability in B whose `depends_on` field names a capability
delivered in A. The prerequisite relationship is not asserted; it is derivable from the
capability inventory.

**Acceptance Scenarios**:

1. **Given** the capability inventory and reuse maps, **when** an implementer reads milestone
   M4's spec, **then** they can identify every Hex component needed, its reuse status, and
   which prior milestone delivers each required arithmetic primitive — without opening any
   file outside `specs/004-milestones/` and `inventory/`.

2. **Given** a new capability added to `inventory/capabilities/`, **when** its `depends_on`
   field is set, **then** it falls unambiguously into one milestone by the section-to-milestone
   assignment in this spec, with no milestone containing capabilities whose prerequisites span
   a later milestone.

3. **Given** a milestone's acceptance condition, **when** an implementer asks "is this milestone
   done?", **then** the answer is deterministic: `sage-inventory remaining` prints nothing
   for the milestone's sections and its modules outside the manual have no open entity, AND every
   selected entity passes oracle comparison. No judgment
   call required.

---

### User Story 2 — Identify what can be worked on in parallel (Priority: P1)

A team working on two milestones simultaneously needs to know that their work does not create
hidden coupling — that the mathematical output of one milestone is not silently consumed by
another at the same level.

**Why this priority**: Parallelism without explicit interface contracts causes integration
failures that are expensive to untangle. This story makes the permitted parallelism explicit
and bounded.

**Independent Test**: For any two milestones listed as independently executable in the
dependency graph, no capability in one has a `depends_on` entry that names a capability in
the other.

**Acceptance Scenarios**:

1. **Given** the dependency graph in `plan.md`, **when** two milestones are on the same
   "level" (neither is a prerequisite of the other), **then** there is no capability-level
   `depends_on` edge between them.

2. **Given** the M0 architecture probes passing `just test`, **when** M1 begins and M14 residual work
   is scheduled, **then** M14 does not claim or defer the foundational `categories` ledger and
   its remaining work does not require computation delivered by M1.

---

### User Story 3 — Track completion without ambiguity (Priority: P2)

A project maintainer needs to know, at any point, exactly how much of the Sage source
has been accounted for in the capability inventory versus actually implemented. These two
measures are distinct and must not be conflated.

**Why this priority**: Confusing "entity has a capability record" with "capability is
implemented" is the primary source of false completion claims. This story makes both measures
machine-queryable and permanently distinct.

**Independent Test**: Running `sage-inventory remaining` (command form in `plan.md`,
"Coverage gate") for every section in a milestone prints nothing if and only if every entity in
that section is `reconciled`, `excluded` or `category-record`: a record selects it and a
source-reconciled worklog batch names its module. This is a coverage measure, not an
implementation measure.

**Acceptance Scenarios**:

1. **Given** a milestone whose sections are all accounted for in `inventory/capabilities/`,
   **when** `sage-inventory remaining` is run for each of its sections, **then** it prints
   nothing — regardless of whether any native Lean computation has been written.

2. **Given** a milestone whose acceptance conditions are met (all entities pass oracle
   comparison), **when** the same `sage-inventory remaining` check is run, **then** it still
   prints nothing — the two conditions are independent and both must hold.

---

### Edge Cases

- A section belongs to two milestones (e.g., `polynomial_rings` spans M2 for univariate and
  M3 for multivariate). The section-to-milestone assignment must name the split explicitly
  with a distinguishing predicate (e.g., "univariate entities only").
- A capability's `depends_on` names a capability from a later milestone. This is a dependency
  cycle and must be surfaced as a spec error rather than silently permitted.
- A milestone's prerequisite is itself blocked (M0 not yet complete). The milestone may not
  begin, but its capability records and reuse decisions may be written in advance.
- A Sage entity is claimed by two capability records. `sage-inventory capability-evidence`
  lists it under `overlapping_entities`; a generic operation and its specialization may both
  select it, and any other overlap must be resolved at the capability level, not the milestone level.

## Requirements

### Functional Requirements

- **FR-001**: Every indexed entity of the Sage 11.0.beta5 source, public or underscore, MUST
  be assigned to exactly one milestone. An entity of a manual module takes the milestone of its
  section. An entity of a module outside the manual takes the earliest milestone of the sections
  that import its module, or, when no manual module imports it, of the sections that hold modules
  of its package; a package with no manual module belongs to M0.
- **FR-002**: The section-to-milestone mapping MUST be derivable from the capability inventory
  without manual lookup: a section's milestone is determined by the mathematical prerequisites
  of its intrinsic operations, not by arbitrary assignment.
- **FR-003**: Each milestone MUST state: the Sage manual sections in scope, any section splits,
  the milestones that are hard prerequisites, the capability records already established,
  key reuse decisions already in `inventory/reuse/`, and the acceptance conditions.
- **FR-004**: The prerequisite relation between milestones MUST be acyclic. A cycle is a spec
  error that blocks the milestone from being accepted.
- **FR-005**: Each milestone's acceptance condition MUST be machine-checkable: either
  `sage-inventory remaining` printing nothing (coverage), or oracle comparison passing
  (implementation), or both — stated explicitly which is required.
- **FR-006**: The milestone structure MUST reference but not duplicate capability records.
  The capability file is the contract; the milestone spec is the grouping and dependency.
- **FR-007**: The milestone for each section MUST be recorded in `docs/domain-specifications.md`
  so the section → milestone lookup is a single table read.
- **FR-008**: Two milestones MUST be explicitly marked as parallelizable only when no
  capability-level `depends_on` edge exists between them.
- **FR-009**: The `docs/milestones.md` file MUST be replaced by `specs/004-milestones/` as
  the authoritative source; `docs/milestones.md` MUST become a pointer to this spec.

### Key Entities

- **Milestone**: A named, numbered grouping of Sage manual sections with a prerequisite set,
  capability file pointers, reuse evidence pointers, and acceptance conditions.
- **Section assignment**: The mapping from a Sage manual section id to exactly one milestone
  (or a named split across two milestones for `polynomial_rings`).
- **Prerequisite edge**: A directed edge from milestone A to milestone B meaning "B may not
  begin implementation until A's acceptance conditions are met."
- **Capability pointer**: A reference from a milestone to an existing capability record
  (not a copy of its content).
- **Acceptance condition**: A machine-checkable criterion (`remaining` query, oracle run, or
  `just test`) that closes the milestone.

## Success Criteria

### Measurable Outcomes

- **SC-001**: For every milestone M1–M14, `sage-inventory remaining` run against each of
  its sections returns a known count, read from `inventory/coverage.json` — either zero (fully accounted) or a specific
  number with an open task to reach zero.
- **SC-002**: The prerequisite graph is acyclic. Verified by topological sort over the
  milestone dependency edges; any cycle surfaces as a spec error before `tasks.md` is accepted.
- **SC-003**: Every milestone that is listed as parallelizable with another has zero
  capability-level `depends_on` edges between them, verified by querying the capability files.
- **SC-004**: `docs/domain-specifications.md` has a Milestone column populated for every row,
  and the values agree with the section assignments in `specs/004-milestones/plan.md`.
- **SC-005**: No section appears in more than one milestone without an explicit split predicate
  naming the distinguishing entity subset.

## Assumptions

- Sage 11.0.beta5 is the fixed baseline. The manual is generated from the source and
  documents 2,400 of its 3,041 modules; the section taxonomy names the domains and does not bound
  the scope. The section and package counts in `inventory/coverage.json` and the module ledger
  `inventory/reconnaissance.json` are authoritative for assignment.
- M0 (reconnaissance) is an ongoing prerequisite for all other milestones. Its SC-001–SC-007
  do not need to be fully satisfied before the milestone spec itself is written, but they must
  be satisfied before any M1+ implementation begins.
- The `polynomial_rings` section is the only section that splits across milestones (univariate
  in M2, multivariate in M3). All other sections belong to exactly one milestone.
- Section `categories` (3,514 entities, 2,718 public) is foundational M0 reconnaissance work. It is
  accounted for through category records, catalogue pointers, or justified exclusions before
  downstream implementation milestones begin. M14 does not own category accounting.
- The milestone numbering (M0–M14) is stable. Adding a new milestone requires a spec amendment
  and a version bump to this feature's `plan.md`.
