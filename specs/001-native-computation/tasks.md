# Tasks: Native computation reconnaissance

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), and the existing inventory contracts.

These tasks complete the reconnaissance assignment. CAS implementation specifications follow
the accepted contracts; their live work graph belongs in GitHub issues.

## User Story 1 — Specify computations in every target domain

**Acceptance**: Every indexed entity of the source is `reconciled`, `excluded` or
`category-record`, and every intrinsic operation has its domain, output, reuse decision, actual
prerequisites and existing test/oracle sources.

- [x] T001 [US1] Pin official Sage `11.0.beta5` and its indexed-content equivalence in
  `inventory/sage/release.toml`; preserve the scanned fork revision in `inventory/sage/index/summary.json`.
- [x] T002 [US1] Generate the reconnaissance ledger over every indexed entity of the source,
  public and underscore, in all 3,041 modules: `inventory/coverage.json` (state counts per manual
  section and per package outside the manual), `inventory/reconnaissance.json` (one row per
  module, with its crediting batches and, outside the manual, its importing sections) and
  `inventory/reconnaissance-entities.jsonl.gz` (one row per entity, with its state and selecting
  records). An entity closes only when a source-reconciled worklog batch names its module.
- [ ] T003 [US1] Read every module of the source and complete `inventory/capabilities/` and
  `inventory/reconnaissance-worklog.toml` in the phase order of [plan.md](plan.md), until
  `sage-inventory remaining` prints nothing for every manual section and every package outside
  the manual. The live state counts are in `inventory/coverage.json`; this file does not copy them.
- [ ] T004 [P] [US1] Complete formal reuse decisions in `inventory/reuse/mathlib-core.toml`
  and the upstream catalogue map for every capability record that T003 produces.
  Each of the 372 current records states a reuse status with its evidence, and its catalogue map
  is checked by `sage-inventory coverage` (73 records name ids of
  `inventory/reuse/lean-categories.toml`, all present). The task stays open while T003 adds
  records. A catalogue id is claimed only when the record's contract is the component's contract,
  never on a similarity score alone.
- [ ] T005 [P] [US1] Complete executable reuse and licence decisions in `inventory/reuse/`
  and `inventory/references/` for every capability record that T003 produces.
  `inventory/references/engines.toml` holds 101 engines, each with a licence, its evidence, a
  version and the names Sage calls it by. Every backend token of every current record resolves to
  an engine id or an engine's `sage_backends` entry;
  `test_every_recorded_backend_names_a_reference_engine` fails when one does not. The task stays
  open while T003 adds records.
- [ ] T006 [US1] Resolve algorithm-family alternatives in capability dependencies before
  deriving a DAG, for every capability record that T003 produces.
  `sage-inventory graph` derives `inventory/dependency-graph.json` and refuses a duplicate id, a
  prerequisite that names no record, and a cycle, so the artifact is acyclic by construction.
  The primality/factorization cycle identified in `research.md` is resolved as an edge:
  `integers.factorization` depends on `integers.primality-proving`, which depends on
  `integers.trial-division` and `integers.modular-power`, because a factorization consumes the
  certificates that a primality test produces. The task stays open while T003 adds records.
- [ ] T007 [US1] Complete the domain specification hierarchy under `specs/` and `docs/` over
  the records that T003 produces: the master product contract defines the fixed scope and output
  taxonomy, `docs/domain-specifications.md` routes every section to its milestone and capability
  files, and `specs/004-milestones/plan.md` supplies the dependency-ordered implementation gates.
  Per-operation semantics stay in the capability records; source doctests and oracle input
  obligations are expanded and checked in `inventory/capability-evidence.json`, so broad
  selectors never stand alone as source evidence.

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
- [ ] T012 [US2] Verify the pinned Lake build and runtime probe commands through `just test` and
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
composition over their results. T012 validates the executable probes through `just test`. T013 then
checks the complete artifact set. T014–T016 consume the completed specifications and accepted
architecture.

Implementation priority is derived only after those inputs exist. The workstream labels in the
project brief are domain partitions, not dependency edges or independently implementable modules.
