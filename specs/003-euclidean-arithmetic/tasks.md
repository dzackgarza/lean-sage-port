# Tasks: Euclidean arithmetic

**Input**: [spec.md](spec.md), [plan.md](plan.md), [contracts/euclidean-operations.md](contracts/euclidean-operations.md), and source-selected doctests in `inventory/capabilities/integers-and-rationals.toml`.

These tasks describe later implementation. Upstream catalogue and normalization contracts remain open. No task is marked complete by a source inventory or this specification.

## Phase 1: Owner contracts

**Purpose**: Obtain the mathematical operation and normalization contracts that public native computations must satisfy.

- [ ] T001 Resolve generic Euclidean division, gcd/lcm, extended-gcd and selected associate normalization at `lean-categories`, with stable operation ids at `lean-cas-dsl`; record exact upstream declarations and unresolved limits in `inventory/reuse/lean-categories.toml`.

## Phase 2: User Story 1 — Divide with remainder (P1)

**Goal**: Compute quotient/remainder, divisibility and exact quotient in an executable Euclidean domain.

**Independent test**: Same-input source-selected division cases, plus runtime reconstruction and decrease over integers and field polynomials; zero divisor fails publicly.

- [ ] T002 [US1] Expose the existing Mathlib Euclidean quotient/remainder operation through the native contract in `LeanSagePort/Euclidean/Division.lean`; choose Lean core integer division with Sage's divisor-sign remainder and Hex field-polynomial divMod when that representation is selected.
- [ ] T003 [US1] Implement divisibility and exact quotient from the same quotient/remainder result, preserving the coefficient domain in `LeanSagePort/Euclidean/Division.lean`.
- [ ] T004 [US1] Add selected Sage integer and polynomial division cases and runtime reconstruction/decrease assertions through the public operation in `Acceptance/Euclidean.lean`.

## Phase 3: User Story 2 — Normalized gcd and lcm (P1)

**Goal**: Return selected gcd/lcm representatives and list folds.

**Independent test**: Source-selected integer, rational and field-polynomial cases; divisibility/greatestness, lcm laws, normal forms, and zero/list identities.

- [ ] T005 [US2] Select the owner-supplied unit normalization over the generic `EuclideanDomain.gcd`, reusing `Nat.gcd`/`Int.gcd` and Hex DensePoly gcd at their supported domains in `LeanSagePort/Euclidean/Gcd.lean`.
- [ ] T006 [US2] Compute normalized lcm and pair/list folds, including empty and zero cases, in `LeanSagePort/Euclidean/Gcd.lean`.
- [ ] T007 [US2] Implement the source's reduced-rational numerator/denominator gcd/lcm rule as a domain-specific selection in `LeanSagePort/Euclidean/Gcd.lean`.
- [ ] T008 [US2] Add selected Sage gcd/lcm cases and runtime divisibility/normalization assertions through the public operation in `Acceptance/Euclidean.lean`.

## Phase 4: User Story 3 — Bézout certificates (P2)

**Goal**: Return coefficients that certify the selected gcd for pairs and finite lists.

**Independent test**: Source-selected integer and field-polynomial xgcd cases, empty/singleton list cases, and runtime Bézout identities. Coefficients may differ from Sage's.

- [ ] T009 [US3] Reuse `EuclideanDomain.xgcd`, Lean core integer coefficients and Hex integer/polynomial extended gcd at their supported domains; transport coefficients by the selected normalization unit in `LeanSagePort/Euclidean/Xgcd.lean`.
- [ ] T010 [US3] Fold pair certificates to finite lists and implement the source's empty/singleton conventions in `LeanSagePort/Euclidean/Xgcd.lean`.
- [ ] T011 [US3] Add selected Sage xgcd cases and runtime pair/list Bézout assertions through the public operation in `Acceptance/Euclidean.lean`.

## Dependencies and execution order

T001 is an owner contract prerequisite for public exposure, not a new algorithm. T002 supplies executable quotient/remainder to T003, T005 and T009. T005 does not supply a computational input to T009: both algorithms consume division and the selected normalization rule, while their gcd equality is an acceptance obligation. T006–T007 consume pair gcd/lcm and rational arithmetic as applicable. T010 consumes pair xgcd. The shared `Acceptance/Euclidean.lean` path makes T004, T008 and T011 sequential edits. Integer and polynomial implementations may use distinct existing producers behind the same mathematical contract.

## Completion rule

A story closes when its public Lean operation computes on runtime inputs in its stated domain and satisfies the independent mathematical acceptance. A declaration, representation-only test or source pointer does not close it. CI owns Lean compilation and acceptance under `AGENTS.md`.
