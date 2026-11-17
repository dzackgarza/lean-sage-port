# Project constitution

`lean-sage-port` implements the full mathematical computation of SageMath natively in Lean 4.
Its target is every intrinsic mathematical operation in the Sage 11.0.beta5 reference manual.

This document is permanent. It records the commitments that govern all implementation work and
cannot be revised without updating every specification and implementation issue that depends on
it. Sections that have not yet been reached by an active milestone are listed here with their
preconditions, not implied away.

---

## Scope

The target is complete: every mathematical domain in the Sage reference manual is in scope.
Implementation is partitioned into milestones by mathematical dependency, not by ambition.
"Complete" means every public Sage entity has either an implemented native computation or a
justified exclusion in a capability record. The exclusion must state a reason
(`infrastructure`, `external-interface`, `presentation`, `data`, or `deprecated`);
"not yet interesting" is not a reason.

The scope boundary runs along the mathematical content of the manual, not along Sage's Python
class structure. A thousand Sage methods that specialize one intrinsic operation belong to one
capability record for that operation. Sage's runtime coercion machinery, its parent/element
hierarchy, graphics, documentation, and test infrastructure are not mathematical capabilities.

---

## Ten permanent commitments

### 1  Lean-native computation

Mathematical algorithms execute through Lean implementations. External systems — Sage, PARI/GP,
FLINT, GAP, Singular — supply independent expected values as test oracles. They are not runtime
computation providers. The only allowed external calls at computation time are those already
present in Hex's approved `@[extern]` interfaces (GMP, CLMUL, `lean_int_div_exact`,
Groebner kernel variants with certified Lean fallbacks, and opaque hooks with verified
certificate checkers).

### 2  Maximum reuse

An existing executable Lean implementation is reused unless source evidence shows that it cannot
satisfy the required mathematical contract. The reuse decision must cite the specific declaration,
path, and reason. "No implementation found" is a valid conclusion only after searching every
file in `inventory/reuse/`. A missing implementation in Hex is a gap to report upstream, not an
authorization to write a competing one.

### 3  Single mathematical authority

This repository defines no mathematical ontology. Every object, operation, and morphism is
identified by its stable catalogue id in `lean-categories`/`lean-cas-dsl`. When the catalogue
lacks an entry for a required operation, the gap is filed with its owner. This repository does
not introduce a parallel registry or a competing definition of the same mathematical concept.

### 4  Mathematical generality

An operation is specified at its actual mathematical scope. `euclidean.gcd` is one record for
gcd in Euclidean domains; it is not duplicated for integers, rationals, and polynomials
separately. Specializations appear as entries in the same record or as `generalizes` links when
their algorithm or contract genuinely differs.

### 5  Executable functionality

A noncomputable Mathlib definition supplies mathematical semantics. It does not discharge a
computational obligation. `matrices.rank` is closed only when a computed rank value passes its
acceptance tests, not when `Matrix.rank` is imported and stated.

### 6  Composability

The result of one computation is usable as the input to the next. A quotient ring built at
runtime retains its defining polynomial, constant embedding, and selected generator. A matrix
over a quotient ring retains both its matrix structure and its coefficient ring. Flattening a
construction to a display value and reconstructing it for the next step is not composability.

### 7  Independent acceptance

Correctness is established against independently sourced expected values: existing Sage
doctests at the indexed baseline, published mathematical examples, or second computations
through a different path. An implementation's own unit test, its local `#guard`, or a
hard-coded fixture does not establish correctness of a general operation.

### 8  Verification scope

Formal Lean proofs of correctness are welcome and strengthen a bridge to the mathematical
semantics. They are not automatically required as a precondition for closing a capability.
Where Hex supplies an executable algorithm with a proof of its core property, that proof is
reused. Where a proof is absent, independent acceptance testing takes its role. The obligation
to eventually prove correctness of a core bridge (such as the Hex quotient–`AdjoinRoot`
equivalence identified in `docs/architecture.md`) is recorded explicitly and does not block
other work.

### 9  Functional priority

An operation is delivered before its optimization. Performance targets are part of a
capability's contract when they are part of its computational applicability — an algorithm
whose constant factor makes it unusable at the required input size fails its contract. When
Hex supplies a benchmarked algorithm that meets the operational scale, it is reused rather than
replaced by a slower proof-carrying alternative.

### 10  Growth by extension

New mathematical domains integrate through the existing catalogue contracts and the existing
execution architecture. Adding a new domain must not require rebuilding or replumbing any
already-accepted capability. The architecture probe acceptance (SC-003 of the reconnaissance
spec) is the evidence that the extension mechanism works; each new milestone must not introduce
dependencies that violate it.

---

## Ownership boundaries

| Owner | Owns |
| --- | --- |
| `dzackgarza/lean-categories` | Category, object, operation, morphism, and functor identities and their mathematical definitions. |
| `dzackgarza/lean-cas-dsl` | The catalogue export, the user-facing language, and the kernel's admission and realization protocol. |
| `leanprover/hex` | Executable algorithms and their computational representations; the released packages are `import HexX`, never `import Hex`. |
| this repository | Native Lean computations that realize catalogue operations, keyed by their stable catalogue id. |

A computation in this repository consumes a catalogue object or operation and may depend on
Hex representations. It does not define the mathematics it computes.

---

## What does not belong here

- A new category, object, or operation definition that belongs in `lean-categories`.
- A second stable-id catalogue or a parallel operation-registration mechanism.
- A competing implementation of a Hex component (unless Hex has explicitly acknowledged the gap
  and the licence permits the independent work).
- An opaque external-engine call substituting for a native algorithm at computation time.
- A specification that accepts a hard-coded example in lieu of a general computation.
- A Lean source file that suppresses all warnings or uses `sorry` outside a designated probe.
- An import of the aggregate `import Hex` (pulls every `*Theory` library and TauCeti).

---

## Readiness conditions for the full target

The reconnaissance assignment (spec `001-native-computation`) establishes the foundation. Its
readiness conditions (SC-001 through SC-007) must all be met before large-scale implementation
begins. The milestone roadmap (`docs/milestones.md`) partitions the subsequent implementation
work. A milestone is ready to begin when all its stated prerequisites have passed their own
readiness conditions.

No percentage of the full Sage manual coverage should be inferred from completing any single
milestone. Each milestone closes when its stated public operations pass their independent
acceptance. The ultimate completion condition is that `sage-inventory unaccounted` returns
nothing for every mathematical section of the manual.

---

## Provenance

Sage baseline: `11.0.beta5`, official commit `36e49d91b0568f07ad4373362c15ce8970587e67`.
Index scanned from fork `c00171e47d6e68d8148d7ee10c4dd77b71a97662`. See
`inventory/sage/release.toml` for the scoped equivalence proof.

Lean toolchain, Mathlib, and Hex revisions: `lean-toolchain`, `lakefile.toml`, `lake-manifest.json`.
Python inventory environment: `tools/inventory/uv.lock`.
