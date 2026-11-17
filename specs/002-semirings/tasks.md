# Tasks: Semiring computations

**Input**: [spec.md](spec.md), [plan.md](plan.md), [contracts/semiring-computations.md](contracts/semiring-computations.md), and the source-selected doctests in `inventory/capabilities/semirings.toml`.

Tasks below describe later implementation. This feature package is a specification; no task is marked complete by the inventory or this document.

## Phase 1: Natural-number computation (US1, P1)

**Goal**: Expose existing `Nat` operations as the natural-number semiring computation.

**Independent test**: Runtime `Nat` inputs satisfy the selected `NonNegativeIntegerSemiring` source examples and ordinary semiring identities through public operations.

- [ ] T001 [US1] Connect Lean core `Nat` to the owner-supplied natural-number semiring catalogue operation in `LeanSagePort/Semirings/Natural.lean`; preserve `Nat` as the element type.
- [ ] T002 [US1] Add source-selected natural-number cases, including the additive generator family, and runtime arithmetic assertions through the public operation in `Acceptance/Semirings.lean`.

## Phase 2: Tropical values and arithmetic (US2, P1)

**Goal**: Construct both tropical orientations over a runtime ordered additive base and compute with finite values and selected infinity.

**Independent test**: Source-selected `TropicalSemiring` and `TropicalSemiringElement` cases pass for both orientations, including zero, one, finite inverse and division failure.

- [ ] T003 [US2] Resolve the mathematical object and operation contracts at `lean-categories` and their catalogue ids at `lean-cas-dsl`, as specified by `inventory/capabilities/semirings.toml`; record the owner resolution in `inventory/reuse/lean-categories.toml` before exposing native operations.
- [ ] T004 [US2] Implement tagged finite/infinity values with retained base and orientation in `LeanSagePort/Semirings/Tropical.lean` under those owner contracts.
- [ ] T005 [US2] Implement min/max addition, base-addition multiplication, natural powers, finite inverse and exact failure behavior in `LeanSagePort/Semirings/Tropical.lean`.
- [ ] T006 [US2] Implement the documented multiplicative-order result through its owner catalogue operation in `LeanSagePort/Semirings/Tropical.lean`.
- [ ] T007 [US2] Add source-selected tropical arithmetic and multiplicative-order cases plus semiring identities through public operations in `Acceptance/Semirings.lean`.

## Phase 3: Tropical transport (US3, P2)

**Goal**: Lift an explicit order-preserving additive base map and compose the induced maps.

**Independent test**: Integer-to-rational source case and runtime identity/composition cases preserve infinity and map endpoints.

- [ ] T008 [US3] Resolve the transport map contract and catalogue id with the mathematical owner, recording the result in `inventory/reuse/lean-categories.toml`.
- [ ] T009 [US3] Implement finite-value mapping, infinity preservation and map composition in `LeanSagePort/Semirings/TropicalMap.lean`.
- [ ] T010 [US3] Add source-selected transport cases and runtime map-law assertions through the public map in `Acceptance/Semirings.lean`.

## Phase 4: Tropical matrices (US4, P2)

**Goal**: Compute closure and extremal cycle mean for matrices over the selected tropical semiring.

**Independent test**: Source-selected matrix cases pass, including unbounded-cycle, empty and nonsquare cases; small exact cycle means agree with independent cycle enumeration.

- [ ] T011 [US4] Supply the `matrices.arithmetic` capability for semiring coefficients through the existing Mathlib/Hex representation contract in `LeanSagePort/Matrix/SemiringArithmetic.lean`.
- [ ] T012 [US4] Resolve closure and cycle-mean catalogue operations with their mathematical owner and record the owner result in `inventory/reuse/lean-categories.toml`.
- [ ] T013 [US4] Implement weak and strong tropical matrix closure with the source's unbounded-cycle behavior in `LeanSagePort/Semirings/TropicalMatrix.lean`.
- [ ] T014 [US4] Implement exact rational-base Karp extremal cycle mean and no-cycle behavior in `LeanSagePort/Semirings/TropicalMatrix.lean`.
- [ ] T015 [US4] Add source-selected closure and mean cases plus independent cycle enumeration for small rational matrices through the public operations in `Acceptance/Semirings.lean`.

## Dependencies and execution order

US1 and US2 have no computational dependency on one another. US3 consumes tropical values from US2. US4 consumes tropical values from US2 and generic semiring matrix arithmetic (`matrices.arithmetic`, T011). Closure and cycle mean can proceed independently once those inputs and their owner contracts exist. The owner resolution tasks precede exposing their corresponding native operations; they do not authorize a local substitute ontology. The same `Acceptance/Semirings.lean` file is shared by all stories, so acceptance edits are sequential.

## Completion rule

Each story closes when its public Lean operation accepts runtime input and satisfies the independent test above. Declared types, source records, successful builds, or tests of internal representations alone do not close a story. Native Lean builds and acceptance run in CI under `AGENTS.md`.
