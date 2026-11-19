# Tasks: Native computation reconnaissance

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), and the existing inventory contracts.

These tasks complete the reconnaissance assignment. CAS implementation specifications follow
the accepted contracts; their live work graph belongs in GitHub issues.

## User Story 1 — Specify computations in every target domain

**Acceptance**: Every manual section has complete source disposition and every intrinsic operation
has its domain, output, reuse decision, actual prerequisites and existing test/oracle sources.

- [x] T001 [US1] Pin official Sage `11.0.beta5` and its indexed-content equivalence in
  `inventory/sage/release.toml`; preserve the scanned fork revision in `inventory/sage/index/summary.json`.
- [x] T002 [US1] Generate `inventory/reconnaissance.json` with one disposition and accounting
  row for every public indexed manual entity, including source, algorithm, reference and backend
  metadata.
- [x] T003 [US1] Complete `inventory/capabilities/` against every section in
  `inventory/domains.toml`; resolve each remaining entity reported by the existing unaccounted query.
  Every section is accounted for: 31,940 entities by source-reconciled capability records, 4,124 by
  exclusions, and the 2,718 entities of `categories` by the category and operation records of
  `inventory/categories/sage-categories.toml`, which the coverage measure counts as
  `by_category_record`. Both `sage-inventory coverage` and `sage-inventory unaccounted` report no
  remainder when given that file.
- [ ] T004 [P] [US1] Complete formal reuse decisions in `inventory/reuse/mathlib-core.toml`
  and the upstream catalogue map for the capabilities identified by T002.
- [ ] T005 [P] [US1] Complete executable reuse and licence decisions in `inventory/reuse/`
  and `inventory/references/` for those same capabilities.
- [ ] T006 [US1] Resolve algorithm-family alternatives in capability dependencies, including
  the primality/factorization cycle identified in `research.md`, before deriving a DAG.
- [ ] T007 [US1] Complete domain Spec Kit specifications under `specs/`, reusing capability
  contracts and source doctests rather than duplicating their content.

## User Story 2 — Validate runtime construction and composition

**Acceptance**: General native computations accept runtime domain parameters and retain the
maps and chosen structure required by later operations; same-input oracle comparisons pass.

- [x] T008 [US2] Resolve the native algorithm-selection interface from the DSL formal-side
  sources and record its concrete owner and signatures in `docs/architecture.md`.
- [ ] T009 [US2] Complete `Probes/RuntimeQuotient.lean` and its public executable entry point
  for runtime quotient/extension construction using existing Hex representations.
- [ ] T010 [US2] Complete `Probes/RuntimeGeneric.lean` across integer, modular, polynomial
  and quotient coefficient domains using the same generic operations.
- [ ] T011 [US2] Exercise retained defining maps, selected generators and ordered composition
  through the public probe entry point; compare against the reference computations in
  `docs/oracles.md` and record the accepted mechanism in `docs/architecture.md`.
- [ ] T012 [US2] Verify the pinned Lake build and runtime probe commands through CI and
  the separately pinned oracle environment; retain run provenance and timing evidence.

## User Story 3 — Prepare independently executable implementation contracts

**Acceptance**: Each implementation obligation identifies its existing mathematical owner,
reusable source, inputs, public computation, source acceptance and actual input dependencies.

- [ ] T013 [US3] Run specification consistency analysis after T012 and resolve gaps between
  the constitution, master/domain specifications, architecture and tasks.
- [ ] T014 [US3] Derive implementation specifications from the completed capability/reuse
  records and accepted architecture. Each task must terminate at a public computation.
- [ ] T015 [US3] Publish the resulting implementation obligations and typed prerequisite
  relationships as GitHub issues; check cycles and source evidence for every dependency.
- [ ] T016 [US3] Perform independent adversarial review of the specifications and dependency
  relationships, correct findings at their owners, and verify the readiness conditions in issue 1.

## Dependencies and execution order

T001 fixes the source against which T002 and T003 complete accounting. T004 and T005 can survey
disjoint upstream sources in parallel, but their scope is bounded by T003. T006 uses the actual
algorithms from T003–T005. T007 consumes those contracts. T008 records the native interface
needed by the probes. T009 and T010 test runtime construction using that interface; T011 tests
composition over their results. T012 validates the executable probes through CI. T013 then
checks the complete artifact set. T014–T016 consume the completed specifications and accepted
architecture.

Implementation priority is derived only after those inputs exist. The workstream labels in the
project brief are domain partitions, not dependency edges or independently implementable modules.
