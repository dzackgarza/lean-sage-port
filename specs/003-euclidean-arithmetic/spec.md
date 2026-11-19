# Feature Specification: Euclidean arithmetic

**Feature directory**: `specs/003-euclidean-arithmetic`
**Created**: 2026-11-17
**Status**: Draft; catalogue and normalization contracts require owner review
**Source**: `euclidean.division`, `euclidean.gcd`, `euclidean.xgcd` in `inventory/capabilities/integers-and-rationals.toml`; official Sage 11.0.beta5 as reconciled in `inventory/sage/release.toml`

## User Scenarios & Testing

### User Story 1 — Divide with remainder (Priority: P1)

A user supplies two elements of a Euclidean domain with an executable division operation. The result is a quotient and remainder in that domain; exact divisibility can then be decided without changing the coefficient domain.

**Independent test**: Reuse source doctests selected by `euclidean.division` and compare same-input Sage computations. For generic domains, check reconstruction and Euclidean decrease through public operations; include integers and univariate polynomials over a field.

**Acceptance scenarios**:

1. Given `a,b ∈ R` with `b ≠ 0`, return `q,r ∈ R` with `a = qb+r` and either `r=0` or the selected Euclidean measure decreasing below that of `b`.
2. For Sage-compatible integer floor division, return `|r|<|b|` with `r=0` or `sign(r)=sign(b)`. For example, `231` divided by `-2` yields `(-116,-1)`.
3. A zero divisor produces an explicit failure at the public operation, although Mathlib's raw `EuclideanDomain.quotient a 0` uses an internal zero convention.
4. Exact division succeeds precisely when the remainder is zero and returns `q` with `qb=a`. The divisibility decision agrees with this condition.

### User Story 2 — Compute normalized gcd and lcm (Priority: P1)

A user requests gcd or lcm of elements in a domain with an executable Euclidean operation and a selected rule for associates. The result is usable as a divisor and in further computations.

**Independent test**: Reuse the `euclidean.gcd` source doctests and compare same-input Sage results under each domain's selected normalization. Check divisibility, greatestness and list folds; use integer and field-polynomial cases.

**Acceptance scenarios**:

1. Gcd divides both inputs, and every common divisor divides it. Lcm is divisible by both and divides every common multiple; each uses the selected associate normal form.
2. For integers, gcd and lcm are nonnegative; `gcd(0,0)=0`, `lcm(0,a)=0`, `gcd([])=0` and `lcm([])=1` under the source list convention.
3. For univariate polynomials over a field, a nonzero gcd is monic; `gcd(0,0)=0`.
4. Rational gcd/lcm use the source's numerator-denominator rule on reduced fractions. This is a domain-specific selection, not a consequence of field Euclidean structure alone.

### User Story 3 — Obtain Bézout coefficients (Priority: P2)

A user requests extended gcd for two elements, or for a finite list under the source wrapper convention. The result includes coefficients that certify the returned gcd and can be used in later exact computations.

**Independent test**: Reuse the `euclidean.xgcd` source doctests and compare the returned gcd under the selected normalization. Check the Bézout identity for runtime inputs; the coefficients need not equal Sage's when multiple valid certificates exist.

**Acceptance scenarios**:

1. For `a,b ∈ R`, return `(g,s,t)` with `g=sa+tb` and `g` equal to the selected gcd result. For integer inputs, `g≥0`.
2. For a finite list `(a₁,…,aₙ)`, return `(g,s₁,…,sₙ)` with `g=Σsᵢaᵢ`. The source wrapper gives `(0,)` for an empty list and `(a,1)` for a singleton; the singleton's associate choice follows that source convention.
3. For `(0,0)`, return gcd zero and any coefficients satisfying the identity. No minimality bound is imposed on coefficients.

### Edge cases

The contract distinguishes a zero divisor from a zero dividend. It handles both signs of an integer divisor, zero gcd inputs, empty and singleton lists, unit associates, polynomial leading coefficients, and a field's noncanonical gcd selection. A domain without executable Euclidean division or a selected unit normalization cannot claim the normalized gcd operation.

## Requirements

### Functional requirements

- **FR-001**: Use an owner-supplied Euclidean-domain structure with executable quotient and remainder. Support every coefficient domain for which the selected operation's hypotheses and implementation are available; the mechanism is generic, not duplicated by type name.
- **FR-002**: Compute quotient/remainder, divisibility and exact quotient with the reconstruction, decrease and failure conditions of User Story 1.
- **FR-003**: State the integer quotient convention explicitly and preserve it for both signs of inputs.
- **FR-004**: Compute normalized gcd and lcm for pairs and finite lists using a selected associate convention; retain the source's empty-list identities.
- **FR-005**: Support integer and field-polynomial normalization, with rational gcd/lcm governed by its separate source convention.
- **FR-006**: Compute pair and finite-list Bézout certificates with the identity in User Story 3. Coefficients are not required to be minimal or representation-identical to a reference certificate.
- **FR-007**: Reuse Lean core integer arithmetic, Mathlib generic `EuclideanDomain.gcd/xgcd`, and available Hex integer and polynomial algorithms as applicable. A generic interface must dispatch only where the domain's actual operations are executable.
- **FR-008**: Connect public computations to existing mathematical and catalogue contracts. Missing division, lcm or xgcd catalogue ids belong to their upstream owner; this repository does not define substitute semantics.
- **FR-009**: Use selected baseline Sage doctests and same-input oracle comparisons. Test mathematical identities for noncanonical coefficients and normalize exact outputs by the stated domain rule.

### Key mathematical objects

- **Euclidean domain**: A commutative ring with executable quotient/remainder and a well-founded decrease relation. A numeric degree function is one sufficient presentation, not the only one.
- **Associate normal form**: A selected representative of each unit-associate class, such as nonnegative integers or monic field polynomials.
- **Division result**: Quotient and remainder in one domain, with reconstruction and decrease.
- **Bézout certificate**: A gcd and coefficients whose linear combination equals it.

## Success criteria

- **SC-001**: The three capability contracts have public runtime computations across every supported domain with the required executable structure, including integer and field-polynomial examples.
- **SC-002**: Selected source doctests and same-input oracle comparisons pass; noncanonical Bézout coefficients pass by their identity and normalized gcd.
- **SC-003**: Division results feed gcd, and gcd/Bézout results feed subsequent exact computations without changing the coefficient domain or losing the selected normalization.

## Clarifications

### Session 2026-11-17

- Sage `Integer.quo_rem` uses the divisor's sign for a nonzero remainder. The generic Euclidean law is reconstruction and decrease; the signed integer convention is an additional selection.
- Sage `Integer.xgcd` and `arith.misc:xgcd` explicitly give no minimality guarantee. Only the normalized gcd and Bézout identity are required.
- Mathlib `EuclideanDomain.gcd/xgcd` are generic executable definitions when the instance and equality decision are executable, but generic gcd returns an arbitrary associate. Normalization is an additional obligation.
- `arith.misc:xgcd` supports finite lists, including empty and singleton conventions. The source's singleton result can retain its input associate even when pair gcd is normalized.

## Unresolved owner contracts

The catalogue map identifies `mor.sets.gcd` for one gcd operation but no general Euclidean division, lcm or extended-gcd id. The mathematical owner must state the generic operations and normalization data; the DSL owner must expose stable ids. The feature is not implementation-ready until those contracts are reconciled with the existing Mathlib operations and source-specific integer/rational conventions.
