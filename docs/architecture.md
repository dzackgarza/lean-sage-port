# Native computation architecture: source-checked candidate

This contract is a candidate for the reconnaissance probes. It does not certify their results.
Source revisions read: `lean-categories` `8782c22ba613a022a84a1e910b6489cc2503e29a`,
`lean-cas-dsl` `24172bfde0fe2d8818b91d87aee23e02453cf9ab`, Mathlib
`6d97e8ad9c32c778e7000ffda543a29488155467`; the Hex source survey in
`inventory/reuse/hex.toml` identifies released Hex `f4b180cfe51692a4e41587d731c92c08a9a63bc4`
and development Hex `3a1b9813b1d1876ae0c89f5cfc20da05547bd854`.

## Ownership and the live boundary

`lean-categories` owns category, object, construction, morphism and operation identities.
Its `LeanCategories/Catalogue/Registry/Entry.lean` defines `ObjectEntry`, `OperationEntry`,
functor and comparison entries. `Semantics/Algebra/NamedRings.lean` gives `ZMod n` as a
parametric ring object; `Semantics/Algebra/Polynomials.lean` gives `R[x]`, its constant map,
generator and evaluation at a selected algebra map. A native algorithm must use these
identities. It may choose data structures; it cannot redefine the mathematics.

`lean-cas-dsl` owns the language, semantic resolution and public request/reply contract.
`CasCatalogue/Registry.lean` imports the upstream semantic state read-only.
`CasCatalogue/Admission.lean` names forms and operations, while
`CasCatalogue/Realize.lean` retains the ordered structural route, its actual applications,
the selected object comparison and session ownership. `StructuredResult.Result` retains
a construction's diagram, cone, apex and packet. A native implementation that serves this
language must preserve those fields through the published interface. A new local registry
or alternate public DSL would create a second authority.

Hex owns many computational representations and algorithms. Its `HexMatrix` dense
matrix is a row-major `Vector` with dimensions in the Lean type, with a Mathlib
equivalence in `HexMatrixTheory`; `HexPermGroup` has a checked stabilizer chain and a
Mathlib-facing theory bridge. These are candidates for direct reuse, not designs to
reimplement. The reuse map distinguishes released packages from unreleased `hex-dev` code.

The DSL's leaf rule does not constrain an independent native Lean library. Its `INTENT.md`
places native computation on the formal side; `AGENTS.md` forbids a *leaf* from shipping
Lean code or certifying itself. This repository can supply a native Lean library that
the formal side or kernel imports. It does not become an opaque external-engine leaf.
`lean-categories`' catalogue entries name the mathematical declarations, while the DSL's
`Admission`, `Wire` and `StructuredResult.Result` are the existing public entry and result
types for language evaluation. The native library can expose typed computations using
those declared mathematical objects, and the kernel can consume them through its
existing admission and realization path. No second registry or language is required.

The surveyed `ObjectEntry` and `OperationEntry` contain semantic declaration names and
binding data, not an algorithm registration field. `MonoLiftComputation` and
`MonoLiftFactorComputation` are examples of callable computational obligations owned by
`lean-categories`; they do not constitute a generic evaluator for all operations.
The exact kernel mechanism for choosing a native implementation of an arbitrary
catalogue operation remains to be identified in source and exercised. This is an
integration contract gap, not an ownership contradiction.

## Computation contracts

| Question | Candidate mechanism | What must be shown |
| --- | --- | --- |
| Runtime domains | Keep parameter values and selected structure with a dependent package of carrier, operations and maps. Use `ZMod n` and `Polynomial R` where they already express the domain. | Values from distinct runtime parameters do not mix; the package can be opened for compiled computation without fixed example types. |
| Optimized data | Put dense matrices, sparse polynomials or residues behind a typed interpretation into the catalogue object. Reuse Hex theory bridges when they cover the exact type. | Interpretations commute with each operation, including normalization and failure cases. |
| Generic dispatch | Resolve the operation from its catalogue identity and actual mathematical hypotheses, then choose a compiled implementation for that structure. | The same generic algorithm works across distinct coefficient domains without method copies or equality of type names. |
| Transport | Retain actual maps, ordered functor applications, comparison direction and chosen data. Use the selected route recorded by the DSL when invoked from it. | A later computation receives the same map or construction chosen earlier; it does not reconstruct one from a display value. |
| Execution | Compose Lean functions on native values; external engines supply only reference answers. | A native result can feed a second native operation without external runtime calls. |
| Correctness | Assert the mathematical contract against independent Sage doctests, published results or second computations; formal proofs can strengthen a specific bridge. | A local algorithm proof or its own fixture cannot choose or change the expected answer. |

Lean's dependent types can express the runtime package, but its exact representation and
erasure cost are not yet validated. Hex already has executable `FpPoly.Quotient` and
`GFqRing.PolyQuotient` for prime-field polynomial quotients. `HexPolyFpTheory.fpPolyEquiv`
relates its polynomial coefficients to Mathlib's `Polynomial (ZMod p)`; the surveyed Hex
modules do not yet establish a generic ring equivalence from a quotient by a runtime
chosen polynomial to Mathlib's `AdjoinRoot`. The probe reuses Hex's quotient operations
and retains the actual polynomial, constant embedding and root; this bridge remains a
specific formal obligation. Hex matrices use type-level dimensions, so a runtime-sized
result needs a dependent dimension witness.

## Discriminating executable probes

`Probes/RuntimeGeneric.lean`, `Probes/RuntimeQuotient.lean` and `Probes/Main.lean`
contain the current executable experiments and a CLI entry point. They are
source-checked against the Hex and Mathlib APIs but have not yet passed CI. The
CLI takes a prime characteristic, a monic defining polynomial and an input
polynomial as ascending coefficient lists, and prints a canonical result.
The generic computation also runs over `Int`, `ZMod 7` and
`Hex.DensePoly Int` without an operation-specific copy. The three sample
outputs in the quotient probe were checked with the workstation's Sage
10.10.beta8 using `PolynomialRing(GF(p), 'x').quotient(f)`. The indexed target
is Sage 11.0.beta5, so this check does not establish baseline-version parity. The
quotient experiment uses Hex's existing
`FpPoly.Quotient`, the chosen characteristic and defining polynomial as run-time
inputs, and one generic polynomial/matrix computation over its result. It also
names Mathlib's actual `AdjoinRoot.mk` for the same polynomial. The missing
equivalence between these two quotient types remains an explicit probe failure
condition; retaining two parallel maps without proving their relation does not
establish representation independence.

1. **Quotient and extension domains.** Construct `ZMod n` and a polynomial quotient
   from runtime input, retain the quotient map and selected generator, perform arithmetic,
   and feed the result into a second operation. Include two different moduli and two
   different defining polynomials in one run. The catalogue currently names `ZMod n`
   and a polynomial quotient object (`inventory/reuse/lean-categories.toml`); the probe
   must verify that its actual quotient map is available and that no operation silently
   crosses the two domains.
2. **Generic coefficient domains.** Use one matrix product and one polynomial operation
   over integers, a modular ring and a polynomial coefficient ring, with coefficients
   selected at run time. Compare public results with Sage's cited doctests and check the
   interpretation of Hex data under the corresponding Mathlib operation. A separate
   hard-coded expression for each domain does not test generic dispatch.
3. **Composed constructions.** Build a quotient or extension, select its defining map,
   form a matrix or polynomial over it, then apply another construction that consumes
   both the object and map. Check endpoints, chosen generators, ordered transport route
   and the composite map. Reopen the result for another native calculation.

Passing a probe means that the same general mechanism survives the contrasting runtime
inputs and that the result satisfies independently sourced mathematical assertions.
Compilation of a fixed example or a diagram alone does not accept this architecture.
The three probes are architectural experiments; they do not stand in for the capability
inventory or for later mathematical implementation acceptance.
