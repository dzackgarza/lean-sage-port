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
- [x] T004 [P] [US1] Complete formal reuse decisions in `inventory/reuse/mathlib-core.toml`
  and the upstream catalogue map for the capabilities identified by T002.
  Every one of the 372 records states a reuse status with its evidence: 34 `reusable`, 238
  `adaptable`, 22 `formalized-not-executable`, 8 `specified-unimplemented`, 70 `missing`. The 71
  records that name no component are the `missing` ones and the single `specified-unimplemented`
  record whose contract has no Lean counterpart; each carries the evidence for the absence.
  The catalogue map is decided per record and checked by `sage-inventory coverage`: 73 records name
  45 distinct ids of `inventory/reuse/lean-categories.toml`, all present, and the other 299 state
  `[]`. The emptiness was swept against the 502 catalogue operations and functors by token overlap
  over the capability sentences; the only matches at or above 0.25 shared-token similarity were
  `euclidean.xgcd` / `mor.sets.gcd`, `integers.divisors` and
  `quadratic.hilbert-symbol-realization` / `mor.sets.nat_prime_factors`, and
  `power-series.specialized` / `mor.sets.power_series_of_coefficients`. Reviewing those four
  against the component declarations: the catalogue's `mor.sets.gcd` is the ℤ-specific gcd map
  already claimed by `euclidean.gcd` and `polynomial-algorithms`' gcd record, not the Bézout
  parametrization; `mor.sets.nat_prime_factors` returns the prime divisors, not the divisor list
  or a Hilbert-symbol realization; `mor.sets.power_series_of_coefficients` builds a series from a
  coefficient sequence, which is a construction, not the specialized series arithmetic. No id was
  added on a similarity score alone; a component is claimed only when the record's contract is
  the component's contract.
- [x] T005 [P] [US1] Complete executable reuse and licence decisions in `inventory/reuse/`
  and `inventory/references/` for those same capabilities.
  `inventory/references/engines.toml` holds 101 engines, each with a licence, its evidence, a
  version and the names Sage calls it by. Nine backend tokens named no engine. `libgap` and
  `mwrank` were aliases: the GAP C library and the eclib program, so they became `sage_backends`
  entries of `gap` and `eclib`. `bliss`, `msolve` and `boost` were engines without a record and
  now have one, with the licence read from the checkout (`build/pkgs/bliss/SPKG.rst` LGPL3,
  `build/pkgs/msolve/SPKG.rst` GPL v2+, both confirming upstream) and from boost.org for the
  header-only library Sage has no package record for. Four tokens were Sage's own plumbing, not
  engines, and were removed from the five records that named them: `interface:abc` (abstract
  interfaces), `interface:process` (the subprocess wrapper), `interface:pd_links` and
  `interface:qsieve` (no such module; the sieve is PARI's, already named by `pari`). Every backend
  token of every record now resolves to an engine id or an engine's `sage_backends` entry; the new
  `test_every_recorded_backend_names_a_reference_engine` fails when one does not.
- [x] T006 [US1] Resolve algorithm-family alternatives in capability dependencies, including
  the primality/factorization cycle identified in `research.md`, before deriving a DAG.
  `sage-inventory graph` derives `inventory/dependency-graph.json`: 372 capabilities, 352 edges,
  155 roots, 11 levels. Neither a capability nor an edge is invented; `derive` refuses a duplicate
  id, a prerequisite that names no record, and a cycle, so the artifact is acyclic by construction.
  The primality/factorization relation is an edge, not a cycle: `integers.factorization`
  depends on `integers.primality-proving`, which depends on `integers.trial-division` and
  `integers.modular-power`. A probabilistic primality test decides a candidate and a factorization
  consumes the certificates it produces, so the direction is the one the algorithms use.
- [x] T007 [US1] Complete the domain specification hierarchy under `specs/` and `docs/`:
  the master product contract defines the fixed scope and output taxonomy,
  `docs/domain-specifications.md` routes every section to its milestone and capability files,
  and `specs/004-milestones/plan.md` supplies the dependency-ordered implementation gates.
  Per-operation semantics remain in the 372 source-backed capability records; source doctests
  and oracle input obligations are expanded and checked in
  `inventory/capability-evidence.json`, so broad selectors never stand alone as source evidence.

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
