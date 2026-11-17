# Tasks: Native computation reconnaissance

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), and the existing inventory contracts.

These tasks complete the reconnaissance assignment. CAS implementation specifications follow
the accepted contracts; their live work graph belongs in GitHub issues.

## User Story 1 — Specify computations in every target domain

**Acceptance**: Every manual section has complete source disposition and every intrinsic operation
has its domain, output, reuse decision, actual prerequisites and existing test/oracle sources.

- [ ] T001 [US1] Reconcile the immutable release baseline in `inventory/sage/baseline.yaml`
  with the indexed source provenance, preserving the existing snapshot references.
- [ ] T002 [US1] Complete `inventory/capabilities/` against every section in
  `inventory/domains.toml`; resolve each remaining entity reported by the existing unaccounted query.
- [ ] T003 [P] [US1] Complete formal reuse decisions in `inventory/reuse/mathlib-core.toml`
  and the upstream catalogue map for the capabilities identified by T002.
- [ ] T004 [P] [US1] Complete executable reuse and licence decisions in `inventory/reuse/`
  and `inventory/references/` for those same capabilities.
- [ ] T005 [US1] Resolve algorithm-family alternatives in capability dependencies, including
  the primality/factorization cycle identified in `research.md`, before deriving a DAG.
- [ ] T006 [US1] Complete domain Spec Kit specifications under `specs/`, reusing capability
  contracts and source doctests rather than duplicating their content.

## User Story 2 — Validate runtime construction and composition

**Acceptance**: General native computations accept runtime domain parameters and retain the
maps and chosen structure required by later operations; same-input oracle comparisons pass.

- [ ] T007 [US2] Resolve the native algorithm-selection interface from the DSL formal-side
  sources and record its concrete owner and signatures in `docs/architecture.md`.
- [ ] T008 [US2] Complete `Probes/RuntimeQuotient.lean` and its public executable entry point
  for runtime quotient/extension construction using existing Hex representations.
- [ ] T009 [US2] Complete `Probes/RuntimeGeneric.lean` across integer, modular, polynomial
  and quotient coefficient domains using the same generic operations.
- [ ] T010 [US2] Exercise retained defining maps, selected generators and ordered composition
  through the public probe entry point; compare against the reference computations in
  `docs/oracles.md` and record the accepted mechanism in `docs/architecture.md`.
- [ ] T011 [US2] Verify the pinned Lake build and runtime probe commands through CI and
  the separately pinned oracle environment; retain run provenance and timing evidence.

## User Story 3 — Prepare independently executable implementation contracts

**Acceptance**: Each implementation obligation identifies its existing mathematical owner,
reusable source, inputs, public computation, source acceptance and actual input dependencies.

- [ ] T012 [US3] Run specification consistency analysis after T006 and resolve gaps between
  the constitution, master/domain specifications, architecture and tasks.
- [ ] T013 [US3] Derive implementation specifications from the completed capability/reuse
  records and accepted architecture. Each task must terminate at a public computation.
- [ ] T014 [US3] Publish the resulting implementation obligations and typed prerequisite
  relationships as GitHub issues; check cycles and source evidence for every dependency.
- [ ] T015 [US3] Perform independent adversarial review of the specifications and dependency
  relationships, correct findings at their owners, and verify the readiness conditions in issue 1.

## Dependencies and execution order

T001 fixes the source against which T002 completes accounting. T003 and T004 can survey disjoint
upstream sources in parallel, but their final scope consumes T002. T005 uses the actual algorithms
from T002–T004. T006 consumes those contracts. T007 resolves the interface consumed by integration;
T008–T010 test the representation and composition mechanisms using surveyed dependencies. T011
validates those executable results. Architecture acceptance follows these probes, not their source
files. T012–T015 consume the completed specifications and accepted architecture.

Implementation priority is derived only after those inputs exist. The workstream labels in the
project brief are domain partitions, not dependency edges or independently implementable modules.
