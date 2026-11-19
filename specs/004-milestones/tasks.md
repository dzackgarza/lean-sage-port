# Tasks: Dependency-ordered milestone roadmap

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts/milestone-schema.md](contracts/milestone-schema.md)

**Organization**: Tasks are grouped by user story. US1 (dependency order) and US2 (parallelism)
are both P1 and can be worked on together after Phase 2. US3 (completion tracking) follows once
the section-to-milestone table is correct.

## Phase 1: Setup

**Purpose**: Establish the directory structure and supersede the hand-written `docs/milestones.md`.

- [x] T001 Spec Kit spec written at `specs/004-milestones/spec.md`
- [x] T002 Research, data model, quickstart, plan, and contract written
- [x] T003 Redirect `docs/milestones.md` to point at `specs/004-milestones/plan.md` as the
  authoritative source (the hand-written content there becomes input, not the deliverable)

---

## Phase 2: Foundational (blocking prerequisites for all stories)

**Purpose**: Verify the prerequisite DAG is acyclic and the section-to-milestone mapping is
complete. These must hold before US1 or US2 can be accepted.

- [x] T004 [US1] Verify the milestone prerequisites against the derived capability graph and
  record the distinction between operation edges and implementation-gate prerequisites in
  `plan.md` §"Verification snapshot". No cycle or hidden dependency was found.
- [x] T005 [P] [US2] Topologically sort the prerequisite edges from `plan.md` and verify that
  the ASCII diagram in §"Dependency graph" agrees with the computed order. Record any
  discrepancy as an amendment to the diagram. Fail and amend `plan.md` if any cycle is found.
- [x] T006 Verify that `docs/domain-specifications.md` has a Milestone column entry for every
  section with `disposition = "mathematical"` in `inventory/domains.toml`, and that every
  entry agrees with `plan.md`. Run the quickstart scenario 4 check and fix any discrepancies.

**Checkpoint**: DAG is acyclic and section assignment table is complete and consistent.

---

## Phase 3: User Story 1 — Determine what must be built before what (P1)

**Goal**: Every milestone has a spec entry that lets an implementer identify prerequisites,
capability records, and reuse evidence without opening files outside `specs/004-milestones/`
and `inventory/`.

**Independent test**: Read milestone M4's spec entry. Identify three Hex components, their
reuse status, and the M1 capability that delivers the required arithmetic primitive — using
only files in this spec and `inventory/`. All three must be findable without further lookup.

- [x] T007 [US1] For each milestone whose `**Capability files**` lists "new file needed",
  record the gap as an open task in that milestone's GitHub tracking issue (issues #2–#15).
  Link each gap to the specific section and an example entity that would go into the new record.
- [x] T008 [P] [US1] For each milestone whose `**Reuse files**` says "survey at capability-
  writing time", confirm that the relevant component ids are not already present in an existing
  `inventory/reuse/*.toml` file. If found, update `plan.md` to name them explicitly.
- [x] T009 [US1] For the `polynomial_rings` split between M2 and M3, run
  `sage-inventory unaccounted <index> <capabilities> polynomial_rings` and confirm that the
  unaccounted entities match the split predicate in `plan.md` (multivariate selectors only).
  Adjust the predicate in `plan.md` if the boundary does not hold.
- [x] T010 [US1] For the M3 open obligation (Hex FpPoly.Quotient ↔ AdjoinRoot bridge), confirm
  that the obligation is recorded in `Probes/RuntimeQuotient.lean` and in the M3 tracking issue
  (#4), with explicit deferred-status or resolution target. Update `plan.md` if either is missing.

**Checkpoint**: Every milestone entry is self-contained per the milestone-schema contract.

---

## Phase 4: User Story 2 — Identify what can be worked on in parallel (P1)

**Goal**: The `plan.md` dependency graph section explicitly names all permitted parallel pairs
and confirms there is no capability-level `depends_on` edge between them.

**Independent test**: Take M2 and M4 (listed as parallelizable). Search all capability files
for `depends_on` entries that cross from M2 to M4 or M4 to M2. Confirm zero cross-edges.

- [x] T011 [P] [US2] For each pair listed as "Parallelism permitted" in `plan.md`, query the
  capability files: for every capability in milestone A, check whether its `depends_on` names
  any capability in milestone B, and vice versa. Document the query result (zero cross-edges
  confirmed, or detected edge requiring plan amendment) in a new section of `plan.md`.
- [x] T012 [P] [US2] For the M2 ∥ M4 pair specifically: confirm that `matrices.arithmetic`'s
  `depends_on` does not name any polynomial capability, and that `polynomials.univariate-
  arithmetic`'s `depends_on` does not name any matrix capability. Add the evidence to `plan.md`.
- [x] T013 [US2] Update `plan.md` §"Parallelism permitted" to include explicit evidence for
  each listed pair. Format: add a table with columns "Pair | Checked capabilities | Result"
  replacing the current assertions with verifiable citations from T011 and T012.

**Checkpoint**: Every parallelism claim in `plan.md` is backed by a zero-cross-edge confirmation.

---

## Phase 5: User Story 3 — Track completion without ambiguity (P2)

**Goal**: Running `sage-inventory unaccounted` for every section of a given milestone is a
single, deterministic operation whose output unambiguously reports coverage state.

**Independent test**: Run the quickstart scenario 1 check for M1 sections. Confirm it returns
the expected current unaccounted count (not zero — M1 is not yet fully accounted), and that
running it a second time returns the same count (deterministic).

- [x] T014 [US3] For each milestone in `plan.md`, record the current unaccounted entity count
  (from `inventory/coverage.json`) in the milestone's acceptance-coverage field alongside the
  command, so the starting gap is documented. Format:
  `[command] — current gap: N entities`.
- [x] T015 [P] [US3] Verify that `inventory/coverage.json` is up to date by re-running
  `sage-inventory coverage` and confirming its output matches the entity counts in `plan.md`.
  Update `plan.md` if counts have drifted.
- [x] T016 [US3] Add a note to `plan.md` §"Milestone definitions" header that explicitly
  distinguishes coverage-complete (accounting gate) from accepted (implementation gate), so
  no reader can conflate them.

**Checkpoint**: Every milestone has a documented current gap count and both acceptance tiers
are explicitly distinguished.

---

## Phase 6: Polish and cross-cutting

- [x] T017 Remove the redirect `docs/milestones.md` placeholder file content and replace it
  with a one-line pointer to `specs/004-milestones/plan.md` (matches FR-009).
- [x] T018 [P] Update GitHub issues #2–#15 to reference `specs/004-milestones/plan.md` as the
  authoritative milestone spec, replacing any references to the now-superseded `docs/milestones.md`.
- [x] T019 Run the full quickstart scenario suite (scenarios 1–5) and confirm all pass or
  document the expected failing state with a known open task.
- [x] T020 Run `sage-inventory capability-evidence` and require every source-reconciled capability
  to have expanded source locations plus an explicit Sage-oracle or contract-input obligation.
  Record the generated ledger at `inventory/capability-evidence.json`; correct the
  `semirings.tropical-base-change` source example so its private implementation doctest is not
  hidden behind a public wrapper selector.

---

## Dependencies and execution order

- **Phase 1**: No dependencies — T001–T002 already complete; T003 is a file edit.
- **Phase 2**: Depends on Phase 1. T004 and T005 can run in parallel. T006 follows T005
  (needs the confirmed sort order to verify the table).
- **Phase 3**: Depends on Phase 2 (DAG confirmed before cross-referencing). T007, T008 can
  run in parallel. T009 and T010 depend only on Phase 2.
- **Phase 4**: Depends on Phase 2 (DAG confirmed). T011, T012 can run in parallel. T013
  depends on T011 and T012.
- **Phase 5**: Depends on Phase 2 (section assignment complete). T014, T015 can run in
  parallel. T016 follows T014.
- **Phase 6**: Depends on Phases 3, 4, 5.

## Completion rule

A story closes when its independent test passes. The milestone feature itself closes when
all six phases are complete and the quickstart scenario suite passes.
