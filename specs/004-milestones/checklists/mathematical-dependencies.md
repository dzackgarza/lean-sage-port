# Mathematical Dependencies Checklist: Dependency-ordered milestone roadmap

**Purpose**: Validate that the milestone prerequisite structure is grounded in actual mathematical
dependencies, that every parallelism claim is verifiable, and that the section-to-milestone
mapping is complete and unambiguous. These are requirements-quality checks — they test whether the
spec and plan are well-written, not whether any Lean code runs.
**Created**: 2026-11-17
**Feature**: [spec.md](../spec.md)

**Review Ownership**: This checklist is a reviewer-owned requirements-quality review artifact.
Mark an item `[x]` only when the reviewer determines the requirements-quality criterion is
satisfied. `[x]` does not mean implementation work is complete.

## Requirement Completeness

- [ ] CHK001 Is every Sage manual section with `disposition = "mathematical"` assigned to exactly
  one milestone (or one named split)? The spec claims FR-001; is the section count in
  `docs/domain-specifications.md` verified against `inventory/domains.toml`? [Completeness, Spec §FR-001]
- [ ] CHK002 Does every milestone entry in `plan.md` include all six required fields named in
  `contracts/milestone-schema.md`? Are any fields missing or placeholder-only? [Completeness, Spec §FR-003]
- [ ] CHK003 Are capability file pointers for all milestones either existing files or explicit "new
  file needed" entries with a named section and example entity? Or are some simply absent?
  [Completeness, Spec §FR-003]
- [ ] CHK004 Are the cross-milestone obligations in `plan.md` (Hex bridge, DSL port, licence
  review) each linked to a specific blocking milestone and an owner? Or are any stated without
  an owner? [Completeness, Spec §FR-003]
- [ ] CHK005 Is the `polynomial_rings` split predicate stated precisely enough that an implementer
  can determine which entities belong to M2 versus M3 by running `sage-inventory unaccounted`
  alone, without reading the Python source? [Completeness, Spec §FR-005, Assumptions]

## Requirement Clarity

- [ ] CHK006 Is "coverage-complete" distinguished from "accepted" in every milestone's acceptance
  conditions, or do any entries conflate the two tiers? [Clarity, Spec §FR-005, US3]
- [ ] CHK007 Is the `polynomial_rings` split predicate a verifiable entity-level predicate (names
  specific Sage module paths), or is it a human-readable description that cannot be automated?
  [Clarity, Spec §FR-005]
- [ ] CHK008 Are the "entity count" figures in each milestone entry cited from `inventory/coverage.json`
  or stated as "approximate"? Can a reader reproduce them from the named source? [Clarity, Spec §FR-003]
- [ ] CHK009 For milestones with "survey at capability-writing time" in their reuse field, is it clear
  *who* does the survey, *when* (before capability writing or simultaneously), and what the survey
  output looks like? Or is this underspecified? [Clarity, Spec §FR-003]
- [ ] CHK010 Is the distinction between a "milestone tracking issue" (#2–#15) and a "per-operation
  implementation issue" (§8 of the plan brief) stated explicitly in `plan.md` or in `tasks.md`?
  Or could a reader conflate them? [Clarity, Spec §FR-008, Gap]

## Requirement Consistency

- [ ] CHK011 Do the prerequisite edges in `plan.md` §"Dependency graph" agree with the `**Prerequisites**`
  field of each milestone entry? Are there any contradictions between the textual list and the
  ASCII diagram? [Consistency, Spec §FR-004]
- [ ] CHK012 Does the section-to-milestone table in `docs/domain-specifications.md` agree with
  `plan.md` for every row? Or are there sections assigned to different milestones in the two
  locations? [Consistency, Spec §SC-004]
- [ ] CHK013 Are the entity counts in `plan.md` consistent with `inventory/coverage.json` at the
  current baseline? Or have they drifted since the plan was written? [Consistency, Spec §SC-001]
- [ ] CHK014 Does the constitution's Principle VII ("Growth by extension: MUST NOT require rebuilding")
  have a corresponding requirement in the spec (FR-001–FR-009) that operationalizes it for milestones?
  Or is the principle stated without a testable milestone-level requirement? [Consistency, Constitution §VII]

## Acceptance Criteria Quality

- [ ] CHK015 Is every acceptance-coverage condition in `plan.md` an exact shell command that can
  be run without further interpretation? Or do any entries say "run unaccounted" without the
  full invocation? [Measurability, Spec §FR-005, SC-001]
- [ ] CHK016 Is the acceptance-implementation condition for each milestone specific enough to be
  machine-checkable (e.g., names the oracle, states "all selected entities pass"), or does any
  entry use vague language ("oracle comparisons pass" without specifying which oracle)? [Measurability, Spec §FR-005]
- [ ] CHK017 For M14 (categories, infrastructure accounting), is "N/A for infrastructure entities"
  as an implementation acceptance condition justified? Does it cover all entities, or only
  those with `exclusion` entries? Are mathematical category operations (if any) covered?
  [Measurability, Spec §FR-005]

## Scenario Coverage

- [ ] CHK018 Is there a requirement or task covering the case where a prerequisite milestone is
  found to be incomplete after a dependent milestone has begun (what is the rollback or
  blocking procedure)? [Coverage, Gap, Exception Flow]
- [ ] CHK019 Is the state transition model in `data-model.md` referenced from `tasks.md` or
  `spec.md`? Or does it exist only in the data model with no connection to acceptance or task
  completion? [Coverage, Spec §US3]
- [ ] CHK020 Are requirements specified for what happens when `sage-inventory unaccounted` returns
  entities that have no clear capability or exclusion home — entities that are genuinely ambiguous?
  [Coverage, Edge Case, Gap]

## Edge Case Coverage

- [ ] CHK021 Is there a requirement covering the case where a new Lean/Mathlib/Hex release changes
  which components are reusable, requiring a reuse decision to change mid-milestone? [Edge Case, Gap]
- [ ] CHK022 Is there a requirement or note covering the case where a section's entity count
  changes because Sage adds or removes entities between baseline versions? [Edge Case, Gap]
- [ ] CHK023 For the `combinat` section (8,177 entities, 47,908 doctests), is the requirement for
  automated oracle runs stated with enough specificity to be implementable, or is it left as
  "acceptance must be automated" without a concrete format? [Edge Case, Clarity, Spec §M8]

## Dependencies and Assumptions

- [ ] CHK024 Is the assumption "M0 reconnaissance must satisfy SC-001–SC-007 before any M1+
  implementation begins" stated as a formal prerequisite in `plan.md`, or only in `spec.md`
  assumptions? [Dependency, Spec §Assumptions]
- [ ] CHK025 Is the assumption that `polynomial_rings` is the *only* section split across
  milestones documented as an assumption that requires verification (via `sage-inventory
  unaccounted` on other large sections)? [Assumption, Spec §Assumptions]
- [ ] CHK026 Is the dependency on the DSL owner adding a `NativeCompute` port (cross-milestone
  obligation) reflected as a blocking prerequisite for any specific milestone's
  *implementation* acceptance (not just coverage)? Or is it only mentioned in a general table?
  [Dependency, Spec §FR-008, Gap]

## Notes

- Items marked `[ ]` require reviewer evaluation before the milestone spec is considered
  implementation-ready.
- CHK010 and CHK026 are likely the most consequential: conflating milestone trackers with
  per-operation implementation issues will cause §8 of the plan brief to remain undelivered,
  and failing to gate any milestone's implementation acceptance on the DSL port means
  implementers will discover the missing interface mid-work.
- Run `just test` and the quickstart scenarios before marking coverage items as satisfied.
