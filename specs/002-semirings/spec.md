# Feature Specification: Semiring computations

**Feature directory**: `specs/002-semirings`
**Created**: 2026-11-17
**Status**: Draft; owner-controlled tropical object and operation contracts remain unresolved
**Source**: `inventory/capabilities/semirings.toml`, Sage 11.0.beta5 at `c00171e47d6e68d8148d7ee10c4dd77b71a97662`

## User Scenarios & Testing

### User Story 1 — Compute in the natural-number semiring (Priority: P1)

A user constructs the nonnegative integers and combines runtime elements with semiring operations. The elements remain available to later computations over the same object.

**Independent test**: Reuse the doctests selected by `semirings.natural-numbers`; apply addition, multiplication and power to runtime natural numbers and check ordinary arithmetic identities.

**Acceptance scenarios**:

1. Given `a,b ∈ ℕ`, addition and multiplication return `a+b` and `a*b` in the same semiring.
2. Given `a ∈ ℕ` and `n ∈ ℕ`, power returns `a^n`, including `a^0 = 1`.
3. The distinguished `0` and `1` act as additive and multiplicative identities.
4. The source's selected additive semigroup generator family contains `0` and `1`; `1` generates positive natural numbers under addition.

### User Story 2 — Compute in tropical semirings (Priority: P1)

A user selects min-plus or max-plus over a linearly ordered additive commutative group with decidable comparison and computes with finite base values and the selected infinity. The convention and base remain attached to every result.

**Independent test**: Run the selected `TropicalSemiring` and `TropicalSemiringElement` source doctests for both conventions; compare operations on further runtime inputs with Sage and verify semiring identities.

**Acceptance scenarios**:

1. For finite `a,b`, tropical addition selects `min(a,b)` or `max(a,b)` and multiplication returns base addition `a+b`.
2. Tropical zero is the selected infinity; tropical one is finite base zero. Infinity is absorbing under multiplication and neutral under addition.
3. A finite element has the base-group inverse under tropical multiplication; inversion or division by tropical zero fails. Natural powers use repeated tropical multiplication. Any wider exponent domain requires its own documented base operation.
4. Multiplicative order returns `1` for tropical one and infinity otherwise, including the absorbing element.
5. For a base with a separately selected element called `1`, the Sage `gens` accessor returns the tropical lift of that element and infinity. This accessor does not supply a generator for an arbitrary ordered additive group.

### User Story 3 — Transport tropical values (Priority: P2)

A user supplies an order-preserving additive base map between compatible tropical semirings. The induced map sends finite values through that map, preserves infinity, and remains composable.

**Independent test**: Reuse the `TropicalToTropical` doctests for integer-to-rational transport; compare application to runtime finite values and infinity. Check identity and composition on the same inputs.

**Acceptance scenarios**:

1. The transported map has explicit source and target tropical semirings and preserves zero, one, addition and multiplication.
2. Composition of two admissible base maps agrees with successive tropical transport, including on infinity.
3. A change of orientation requires an explicit mathematical map; an order-preserving base map alone does not silently change min-plus to max-plus.

### User Story 4 — Compute tropical matrix invariants (Priority: P2)

A user forms a square tropical matrix and computes its weak or strong path closure, or its extremal cycle mean when the base supports exact means. Results keep the coefficient semiring and matrix indices.

**Independent test**: Reuse doctests selected by `semirings.tropical-matrix-closure` and `semirings.tropical-cycle-mean`. Compare entries and failures with Sage; for small matrices, enumerate directed cycles independently to check means.

**Acceptance scenarios**:

1. Weak closure returns the tropical sum of positive powers; strong closure includes the identity. The result remains a matrix over the original tropical semiring.
2. A cycle that makes a closure unbounded produces the documented cycle failure, including the convention and matrix context.
3. For an exact rational base, min-plus cycle mean returns the minimum cycle mean and max-plus returns the maximum cycle mean. An empty square matrix returns tropical infinity; nonsquare input fails. A matrix with no finite cycle returns the selected infinity under the mathematical empty-extremum convention; this additional case needs independent acceptance because the Sage source handles only its zero-matrix branch.

### Edge cases

The source doctests cover zero and one, finite and infinite tropical elements, min/max orientation, empty matrices, nonsquare matrices, and unbounded cycles. Division by infinity and incompatible base maps are failures. The nonzero acyclic cycle-mean case is a supplemental mathematical obligation; Sage's source raises an empty-extremum error for it. A matrix algorithm must not claim exact output on an approximate base without a precision contract.

## Requirements

### Functional requirements

- **FR-001**: Expose `ℕ` with its existing mathematical semiring operations, executable Lean natural-number arithmetic, and the selected additive generator family documented by the source.
- **FR-002**: Construct min-plus and max-plus semirings over linearly ordered additive commutative groups with decidable comparison, using Mathlib's `MinTropical (WithTop R)` and `MaxTropical (WithBot R)` structures. Preserve base, orientation and selected infinity in runtime elements.
- **FR-003**: Compute tropical addition, multiplication, natural powers, finite multiplicative inverse, and the documented identity and failure cases on runtime inputs.
- **FR-004**: Compute the multiplicative-order convention in `semirings.tropical-multiplicative-order`.
- **FR-005**: Construct and compose transport induced by an order-preserving additive base map while preserving source, target and infinity.
- **FR-006**: Compute weak and strong path closures for square tropical matrices, with the source-defined failure for unbounded cycles.
- **FR-007**: Compute exact extremal cycle means for the rational-base domain in the capability record; preserve the source's empty-matrix and nonsquare behavior.
- **FR-008**: Use the existing generic semiring matrix arithmetic contract `matrices.arithmetic`. Native operations must attach to owner-supplied mathematics and catalogue ids; missing ids are resolved at their owner.
- **FR-009**: Accept operations using baseline Sage source doctests and same-input oracle comparisons. Compare intrinsic values and retained maps, not display strings. No external CAS executes the native operation.

### Key mathematical objects

- **Natural-number semiring**: Mathlib/Lean's `Nat` with semiring structure; no new number system.
- **Tropical semiring**: An ordered additive base, min/max orientation, finite values and one selected infinity.
- **Tropical map**: An admissible base map and its induced semiring map with explicit source and target.
- **Tropical matrix**: A finite indexed matrix over a selected tropical semiring; closure and mean retain that coefficient domain.

## Success criteria

- **SC-001**: Each of the six capability records in `inventory/capabilities/semirings.toml` has a public runtime computation satisfying its exact contract.
- **SC-002**: Source doctests selected by those records and the same-input independent oracle comparisons pass within their stated domains, including meaningful failure cases.
- **SC-003**: Values, maps and matrices produced by one operation remain usable in the next operation with base, orientation, source, target and indices preserved.

## Clarifications

### Session 2026-11-17

- `TropicalSemiringElement.__pow__` in the baseline accepts some rational exponents when the base supports them. FR-003 requires natural powers at generic group scope. A wider exponent operation is conditional on the base's scaling contract; it is not inferred from ordered-group structure.
- `TropicalToTropical` in the baseline demonstrates integer-to-rational coercion. The mathematical contract requires an explicit order-preserving additive base map; a bare conversion is insufficient to justify a general map.
- The source's `extremum_cycle_mean` checks membership under `RR` and uses division by path length. This specification's exact contract uses rational values and exact rational division. Approximate real semantics require a separate precision contract.
- Natural-number arithmetic uses Lean's existing `Nat`. Sage's `NN` construction and additive generator family are source examples, not authority for another natural-number type.
- The baseline `TropicalSemiring.gens` returns `(base one, infinity)` for bases such as `ℤ` and `ℚ`. An ordered additive group has no canonical base one. The accessor therefore needs a selected base element and does not change the general tropical semiring construction's domain.

## Unresolved owner contracts

`inventory/capabilities/semirings.toml` has no catalogue ids for tropical object construction, multiplicative order, base change, closure or cycle mean. The mathematical owner must determine the corresponding operations and the DSL owner must expose their stable ids. The `MinTropical`/`MaxTropical` realization and public operations cannot be declared implementation-ready until those contracts are reconciled. The current feature specification states the required behavior without inventing local ids.
