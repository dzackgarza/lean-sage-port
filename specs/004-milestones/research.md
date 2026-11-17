# Research: Dependency-ordered milestone roadmap

## Decision: Milestone count and granularity

**Decision**: 15 milestones (M0–M14).

**Rationale**: The dependency structure of mathematical prerequisites naturally partitions the
38,782 Sage entities into these groups. Finer granularity (e.g., splitting M8 combinatorics
from graphs) would create milestones whose prerequisites are identical and whose parallelism
is already permitted within the coarser grouping. Coarser granularity (e.g., merging M5
homological algebra into M4 linear algebra) would prevent starting homology work until all of
M4's lattice computations are done, which is an artificial block.

**Alternatives considered**:
- 7 workstreams (from the original plan brief): rejected because the workstream labels are not
  dependency edges; they are domain groupings. M8 combinatorics cannot begin until M6 group
  theory is done (Polya enumeration), but neither workstream captures this.
- One milestone per Sage section: rejected because 65 milestones at the section level creates
  unmanageable overhead and obscures the mathematical structure. Sections within a domain share
  prerequisites entirely.

---

## Decision: Section-to-milestone assignment method

**Decision**: Assign by the mathematical prerequisites of the section's intrinsic operations,
read from the `depends_on` fields of existing capability records and the structure of yet-to-be-
written records inferred from their known algorithm families.

**Rationale**: The `depends_on` field in each capability record is the ground truth. If
`polynomials.univariate-factorization` has `depends_on = ["polynomials.univariate-arithmetic",
"polynomials.extended-gcd", "integers.factorization"]`, then `polynomial_rings` (factorization)
must follow the milestone containing integer factorization (M1) and the milestone containing
polynomial gcd (M2). That places multivariate and Gröbner work after M2 by necessity.

**Alternatives considered**:
- Assign by Sage's Python module grouping: rejected because Sage's class hierarchy is not a
  mathematical ontology (the plan's constraint II). `rings_standard` and `finite_rings` both
  depend on integer arithmetic; that is not visible from the Python module names.

---

## Decision: `polynomial_rings` split across M2 and M3

**Decision**: Univariate entities (arithmetic, division, gcd, factorization, power series) go
to M2. Multivariate entities (sparse polynomial ring, monomial orders, ideals, Gröbner bases)
go to M3.

**Rationale**: Multivariate arithmetic does not depend on univariate factorization. But Gröbner
basis computation (`ideals.groebner-basis`) depends on `polynomials.multivariate-arithmetic`
which itself depends on nothing except base ring arithmetic. However, the full polynomial-rings
section in Sage also contains quotient constructions that depend on Gröbner bases, which in turn
belong with the broader commutative algebra work of M3. Splitting the section avoids blocking M2
on M3's heavier prerequisites.

**Distinguishing predicate**: M2 owns `polynomial_rings` entities whose `sage` selectors are
under `sage.rings.polynomial.polynomial_element` or `sage.rings.polynomial.polynomial_ring`
(univariate). M3 owns entities under `sage.rings.polynomial.multi_polynomial_*`,
`sage.rings.polynomial.polynomial_ideal`, and their related modules.

---

## Decision: `categories` section placement in M14

**Decision**: M14 is primarily an accounting milestone, not a computation milestone.

**Rationale**: The `categories` section has 2,718 entities. The `lean-categories` repository
owns the mathematical semantics of every category operation. Most `categories` entities either:
(a) already have a catalogue entry in `inventory/reuse/lean-categories.toml` and will be
accounted for when their associated domain milestone is complete, or
(b) are framework helpers (`is_a_`, `_make_element_constructor_`, etc.) that go to `exclusion`
with reason `implementation-support`.
The work in M14 is running `sage-inventory unaccounted categories`, categorizing the residue, and
filing gaps with `lean-categories`. This requires that the domain milestones (M1–M3 especially)
have already attached their catalogue entries to their capability records.

---

## Decision: Parallelism boundaries

**Decision**: The following pairs are explicitly parallelizable after their shared prerequisites:
- M1 and M14-accounting: M14's accounting work has no computational prerequisite on M1.
- M2 and M4: both follow M1; no M2 capability is in `depends_on` of any M4 capability (matrix
  arithmetic depends on ring arithmetic from M1, not on polynomial arithmetic).
- M5 and M6: both follow M4; chain complex homology does not depend on group theory.
- M8 and M9: both follow M4/M5/M6 respectively; graph algorithms and topology computations
  are independent.
- M12 (calculus, special functions) and M6/M8: M12 follows M1 and M2; it does not depend on
  group theory or combinatorics.

**Boundaries that are NOT parallelizable**:
- M3 must follow M2 (multivariate polynomials need univariate division as a subroutine).
- M7 must follow M2, M3, M4 (number field algorithms need Gröbner bases and lattice reduction).
- M10 must follow M3 and M7 (arithmetic geometry needs commutative algebra and number fields).
- M11 must follow M7 and M10 (modular forms need number fields and elliptic curves).

---

## Decision: Acceptance condition types

**Decision**: Two distinct acceptance tiers, both required for a milestone to close:
1. **Coverage**: `sage-inventory unaccounted` returns nothing for every section in the milestone.
   This measures that every entity has a capability record or justified exclusion. It does NOT
   measure that any native computation exists.
2. **Implementation**: Every selected entity (those with capability selectors) passes same-input
   oracle comparison against the Sage image in `docs/oracles.md`. This measures that the native
   computation exists and is correct.

A milestone may satisfy (1) before (2). Satisfying (1) is a prerequisite for starting
implementation work in that milestone. A milestone closes only when both hold.

---

## Decision: `docs/milestones.md` disposition

**Decision**: `docs/milestones.md` becomes a pointer to `specs/004-milestones/plan.md`. The
content I wrote there earlier is the input that `plan.md` supersedes. Its dependency graph and
section assignments are reproduced here with Spec Kit structure backing them.
