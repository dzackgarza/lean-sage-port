# Milestone roadmap

This document partitions the implementation of `lean-sage-port` into milestones ordered by
mathematical and computational dependency. Each milestone is a coherent scope of work that can
be accepted independently. A milestone may not begin until all its listed prerequisites have
passed their acceptance conditions.

The milestones are derived from the capability inventory, the reuse maps, and the architecture
contracts. They are not arbitrary work slices. The dependency order reflects which mathematical
objects and algorithms are prerequisites for which others: a quotient ring construction must
precede field extensions; field-polynomial gcd must precede factorization; Smith normal form
must precede chain-complex homology.

Coverage numbers come from `inventory/coverage.json` at the current baseline (Sage 11.0.beta5,
38,782 public mathematical entities). They indicate scale, not completion claim.

---

## M0 — Reconnaissance and foundation (prerequisite for all)

**Purpose**: Establish the contracts, architecture, and infrastructure that all implementation
milestones depend on.

**Sections in scope**: All (this milestone resolves the meta-level, not mathematical content).

**Prerequisites**: None.

**Acceptance conditions** (the SC-001–SC-007 of `specs/001-native-computation/spec.md`):

- SC-001: Every baseline manual section and public entity has a reviewed scope disposition.
- SC-002: Every foundational obligation has a source-backed reuse decision and licence disposition.
- SC-003: All runtime-construction and composition probes pass CI on runtime inputs.
- SC-004: Every planned implementation issue has contract, dependency, and acceptance content
  sufficient to proceed without a fresh reconnaissance.
- SC-005: The dependency graph is acyclic and each edge names an actual consumed prerequisite.
- SC-006: The pinned environment builds in CI and the independent oracle path executes.
- SC-007: Independent review leaves no unresolved foundational decision hidden in implementation.

**Current status** — partially done. What remains:

| Task | Status |
| --- | --- |
| Sage 11.0.beta5 baseline pinned | ✓ Done — `inventory/sage/release.toml` |
| Reuse surveys: Mathlib, Hex, lean-categories | ✓ Done — `inventory/reuse/` |
| Architecture contracts documented | ✓ Done — `docs/architecture.md` |
| DSL dispatch owner resolved | ✓ Done — `docs/architecture.md` §"Native selection at the DSL boundary" |
| Runtime probes written | ✓ Done — `Probes/RuntimeQuotient.lean`, `Probes/RuntimeGeneric.lean` |
| Probes pass CI | **Open** — T008–T011 in `specs/001-native-computation/tasks.md` |
| Capability inventory complete | **Open** — 38,324 of 38,782 entities unaccounted |
| Domain specifications complete | **Open** — 2 of ~20 mathematical-domain specs done |
| Implementation issues published | **Open** — T013–T014 |
| Adversarial review | **Open** — T015 |

M0 is in progress. M1 may proceed in parallel for its independent sub-scope (integers and
rationals), since those capability records and reuse decisions are already complete. All other
milestones wait for M0 SC-001 through SC-007.

---

## M1 — Integers, rationals, and core modular arithmetic

**Purpose**: The arithmetic foundation that every algebraic algorithm uses.

**Sections in scope**: `rings_standard` (integers and rationals), `finite_rings` (modular
arithmetic layer only — `ZMod n`, CRT, primitive roots, multiplicative orders).

**Entity count**: ~550 entities across the two sections.

**Prerequisites**: M0 SC-003 (probes pass), M0 SC-002 (reuse decisions for these sections).

**Capability records** (all already exist in `integers-and-rationals.toml` and `finite-rings.toml`):

- `integers.arithmetic` — bignum ring operations (`lean-core.int`, GMP-backed, `reusable`)
- `rationals.arithmetic` — reduced-fraction field (`lean-core.rat.arithmetic`, `reusable`)
- `monoids.power` — binary powering in any monoid
- `euclidean.division` — quotient/remainder, divisibility, exact quotient
- `euclidean.gcd` and `euclidean.xgcd` — normalized gcd, lcm, Bézout
- `rationals.rounding` — floor, ceiling, truncation, rounding
- `integers.modular-inverse` — inverse mod n via xgcd
- `integers.modular-power` — a^n mod m with Montgomery/Barrett
- `modular.crt` — Chinese remainder reconstruction
- `modular.multimodular-basis` — Garner product-tree basis
- `modular.rational-reconstruction` — scalar and vector rational reconstruction
- `modular.primitive-root` — smallest generator of (Z/n)^*
- `modular.residue-sets` — quadratic residues, integers coprime to n
- `modular.multiplicative-order` — order of a unit mod n
- `integers.radix-representation` — base-b digits, bit operations, byte conversions
- `integers.roots-and-perfect-powers` — integer roots, perfect-power detection
- `integers.integer-logarithm` — floor log base b
- `integers.valuation` — p-adic valuation and cofactor
- `integers.primality-proving` — BPSW, Miller-Rabin, Pocklington/ECPP
- `integers.factorization` — Pollard rho, ECM, QS; Hex supplies the executable core
- `integers.multiplicative-functions` — phi, sigma, Möbius, Carmichael lambda

**Key reuse decisions already established**:
- Lean core `Int`/`Nat`: GMP-backed, `reusable` for arithmetic
- `lean-core.int.modpow`, `hex.HexArith.pow-mod`: modular exponentiation, `reusable`
- `hex.HexArith.extended-gcd`: xgcd with GMP extern, `reusable`
- `hex.HexModular.crt` and `hex.HexModular.rational-reconstruction`: `reusable`
- `hex.HexPrimality.miller-rabin`, `hex.HexPrimality.pocklington-certificates`,
  `hex.HexECPP.certificate-checker`: primality, `reusable`
- `hex.HexIntFactor`: Pollard rho, ECM, `reusable`
- `hex.HexIntFactor.multiplicative-order`: `adaptable` (wrapper needed)
- Mathlib `Nat.totient`, `ArithmeticFunction.moebius`: `adaptable` (linear in n; product-formula wrapper needed)

**Acceptance**: Every selected Sage entity in `rings_standard` and the modular-arithmetic
portion of `finite_rings` passes same-input oracle comparison with the Sage image in
`docs/oracles.md`. Map retention is verified by the M0 probes for all quotient and extension
types constructed in this milestone.

---

## M2 — Univariate polynomials and power series

**Purpose**: The polynomial ring over arbitrary executable coefficient rings, including
arithmetic, division, gcd, factorization, and truncated power series.

**Sections in scope**: `polynomial_rings` (univariate subset), `power_series`, `semirings`
(tropical arithmetic — already in `semirings.toml`).

**Entity count**: ~570 entities (1,710 in `polynomial_rings`, but multivariate and
noncommutative are deferred to M3).

**Prerequisites**: M1 (integers and finite-field coefficient arithmetic), M0 SC-003.

**Capability records** (exist in `polynomials.toml`, `polynomial-algorithms.toml`,
`semirings.toml`; power series needs new records):

- `polynomials.univariate-arithmetic` — ring ops, division, evaluation (Hex `DensePoly`, `reusable`)
- `polynomials.extended-gcd` — monic gcd and Bézout over fields, primitive gcd over Z
- `polynomials.univariate-factorization` — square-free, Berlekamp, Zassenhaus, Hensel
- Power series arithmetic — `TSeries` ring over `NatInverses` coefficient (Hex `HexTruncatedSeries`)
- Power series inverse, sqrt, exp, log, composition, reversion (Hex `HexTruncatedSeries`, `reusable`)
- Semiring arithmetic — tropical, min-plus (Mathlib `Tropical`, `reusable`)

**Key reuse decisions**:
- `hex.HexPoly.dense-poly`, `hex.HexPoly.arith-mul-eval`, `hex.HexPoly.div-mod`: `reusable`
- `hex.HexPoly.gcd-xgcd`, `hex.HexPoly.pseudo-division`: `reusable`
- `hex.HexBerlekamp.berlekamp-factor`, `hex.HexBerlekampZassenhaus.factorize`: `adaptable`
- `hex.HexTruncatedSeries.*`: `reusable` (inverse, sqrt, exp/log, comp/rev all done through 7)
- `hex.HexModArith.ntt`, `hex.HexModArith.multiprime-int-convolution`: `reusable`
  (required for FFT-based polynomial multiplication)

**Outstanding probe obligation**: The M0 composed-construction probe must include a polynomial
over a quotient-ring coefficient domain before this milestone may close the coefficient-domain
generality contract.

**Acceptance**: Sage doctests for all selected entities in `polynomial_rings` univariate and
`power_series`, plus runtime oracle comparisons at integer, `ZMod p`, and polynomial-quotient
coefficient domains.

---

## M3 — Multivariate polynomials, Gröbner bases, and commutative algebra

**Purpose**: Multivariate polynomial rings, ideals, Gröbner bases, quotient rings, and the
commutative-algebra operations on them.

**Sections in scope**: `polynomial_rings` (multivariate), `rings` (general commutative ring
constructions: quotient rings, localizations, integral domains), `algebras` (commutative
algebras over a ring).

**Entity count**: ~3,150 entities (`polynomial_rings` multivariate remainder: ~1,140;
`rings`: 306; `algebras`: 1,942 — the last is large and will need extensive exclusion analysis).

**Prerequisites**: M2 (univariate polynomials), M1 (finite-field arithmetic).

**Capability records** (partially exist; Gröbner and commutative-ring constructions need new
records):

- `polynomials.multivariate-arithmetic` — sparse `MvPoly`, monomial orders (Hex `HexMvPoly`, `reusable`)
- `ideals.groebner-basis` — reduced Gröbner basis (Hex `HexGroebner`, `reusable` with certified fallback)
- `ideals.ideal-membership` — test, normal form
- `rings.quotient-ring` — polynomial quotient by ideal
- `rings.localization` — ring of fractions
- `rings.primary-decomposition` — primary decomposition of a polynomial ideal
- `algebras.tensor-product` — over a commutative ring (Mathlib `TensorProduct`, `formalized-not-executable`; computation gap)
- `algebras.exterior-algebra` — Mathlib `ExteriorAlgebra`, same gap

**Key reuse decisions**:
- `hex.HexMvPoly.sparse-mvpoly`, `hex.HexMvPoly.monomial-orders`: `reusable`
- `hex.HexGroebner.basis`: `reusable` (certified Lean fallback, `@[extern]` allowed)
- Mathlib `Ideal.Quotient`: `formalized-not-executable` — a computational representation bridge is required
- `hex.HexPolyFp.Quotient.Ring` and `HexPolyFpTheory.fpPolyEquiv`: `adaptable` — the
  Hex quotient ↔ `AdjoinRoot` equivalence is the outstanding formal bridge from `docs/architecture.md`

**Notable open obligation**: The `interpret` map in `Probes/RuntimeQuotient.lean` names the
unproved bridge between `FpPoly.Quotient` and Mathlib `AdjoinRoot`. This is an explicit
open debt that must be resolved or explicitly deferred with a formal certificate before M3
acceptance. It does not block M1 or M2.

**Acceptance**: Sage doctests for selected multivariate and commutative-ring entities, Gröbner
basis comparisons via the oracle at the same monomial order, and quotient-ring round-trip tests.

---

## M4 — Linear algebra: matrices, modules, and lattices

**Purpose**: Matrix computations, module structure, Smith and Hermite normal forms, lattice
operations.

**Sections in scope**: `matrices`, `modules`, `tensor_free_modules`, `lattices`
(the lattice portion of `matrices`, currently in `lattices.toml`).

**Entity count**: ~1,900 entities (`matrices`: 754; `modules`: 719; `tensor_free_modules`: 179;
lattice entities spread across `matrices`).

**Prerequisites**: M1 (integer and modular arithmetic), M2 (polynomial arithmetic for
characteristic polynomial and rational normal form).

**Capability records** (partially exist in `linear-algebra.toml` and `lattices.toml`):

- `matrices.arithmetic` — construction, sum, product over a semiring (`adaptable`: Hex `HexMatrix`)
- `matrices.rank` — over a field or Z (Hex `HexRank`, `adaptable`)
- `matrices.kernel` — nullspace over a field, saturated Z-kernel (Hex `HexRowReduce`, `adaptable`; `HexHermite`, unreleased)
- `matrices.smith-normal-form` — integer Smith with unimodular transforms (Hex `HexSmith`, unreleased)
- `matrices.hermite-normal-form` — row Hermite with transform (Hex `HexHermite`, unreleased)
- `matrices.determinant` — exact integer and field determinant (Hex `HexDeterminant`, `reusable` or `adaptable`)
- `matrices.echelon-form` — reduced row echelon, pivot sequence
- `matrices.solve` — linear systems with certificate or infeasibility proof
- `matrices.characteristic-polynomial` — Berkowitz/Hessenberg
- `matrices.rational-normal-form` — Frobenius invariant factors
- `lattices.*` — lattice reduction (LLL, BKZ), Gram matrix, Voronoi cell
  (sources in `references/lattice-engines/` research tables; Hex `HexLattice` family)
- Module operations: free module over a ring, finitely generated module, free cover, rank

**Key reuse decisions**:
- `hex.HexMatrix.dense-matrix`: `reusable` (type-level dimensions; runtime-sized result needs dimension witness)
- `hex.HexDeterminant.*`: check released status at import time
- `hex.HexSmith.snf`, `hex.HexSmith.snf-certificate`: `reusable` (unreleased at survey — verify before import)
- `hex.HexHermite.*`: `adaptable` (unreleased; integral-kernel computation is a dependency of M5)
- `hex.HexLattice.*`: check per component in `hex.toml`
- Mathlib `Matrix.det`, `Matrix.rank`: `formalized-not-executable` — computation bridges required
- `mathlib.linalg.smith-normal-form`: `formalized-not-executable` — Hex supplies the executable

**Research table cross-reference**: `~/research/references/lattice-engines/` holds method
inventories for lattices, with Sage, Oscar, PARI/GP, FLINT, NTL, and fpylll conventions.
Read those before writing capability records for the lattice section.

**Acceptance**: Sage doctests for selected matrix and module entities, Smith/Hermite certificate
verification, lattice-reduction comparisons against PARI/GP and fpylll.

---

## M5 — Homological algebra and chain complexes

**Purpose**: Chain complexes of finite free modules, their homology with representatives, chain
maps, cones, and mapping cylinders.

**Sections in scope**: `homology`, `resolutions`.

**Entity count**: 120 entities.

**Prerequisites**: M4 (Smith normal form for integer homology, kernel for field homology).

**Capability records** (exist in `homological-algebra.toml`; `resolutions` needs new records):

- `complexes.finite-free-construction` — graded matrix assembly (Mathlib `HomologicalComplex`, `formalized-not-executable`)
- `complexes.homology-with-representatives` — Z invariant factors, field dimension, cycle representatives
- `complexes.shift` — grading shift with sign convention
- `complexes.chain-maps` and composition
- `complexes.cone-cylinder` — mapping cone and cylinder
- `resolutions.*` — free resolutions, Betti numbers, projective dimension

**Key reuse decisions**:
- `mathlib.homology.complexes`: `formalized-not-executable`
- `hex.HexSmith.snf` (from M4): executable prerequisite for integer homology
- `hex.HexRowReduce.nullspace-span` (from M4): executable prerequisite for field homology
- `hex.HexHermite.lattice-membership-kernel` (from M4): integer kernel basis

**Acceptance**: Sage doctests in `homology/chain_complex.py`, including the displayed
`Z x C3` integer homology and Klein-bottle examples; cycle-class arithmetic tests.

---

## M6 — Finite groups and representation theory

**Purpose**: Finite permutation groups, group-theoretic algorithms, and linear representations.

**Sections in scope**: `groups`, `algebras` (group algebras), `rings` (group ring constructions).

**Entity count**: ~1,000 entities (908 in `groups`; partial `algebras`/`rings` overlap deferred
to M3 for the ring constructions).

**Prerequisites**: M1 (integer arithmetic for group orders), M4 (matrices for representations).

**Capability records** (most exist in `groups.toml`; representation theory needs new records):

- `groups.permutation-group` — from generators (Hex `HexPermGroup`, `reusable`)
- `groups.order-and-membership` — Schreier-Sims order and sifting (Hex, `reusable`)
- `groups.orbit` and `groups.stabilizer`
- `groups.cosets` — left and right cosets
- `groups.sylow` — Sylow subgroups
- `groups.derived-series` — lower central, derived, composition series
- `groups.abstract-group` — finitely presented groups, Todd-Coxeter coset enumeration
- `groups.abelian` — finitely generated abelian groups, invariant factors (uses M4 Smith)
- `groups.representations` — character table, irreducible decomposition

**Key reuse decisions**:
- `hex.HexPermGroup.*`: `reusable` for the stabilizer-chain family
- `hex.HexPermGroupTheory.group-bridge`: Mathlib bridge, `formalized-not-executable`
- GAP is a reference oracle; it is not a computation provider

**Acceptance**: Sage doctests for `groups/perm_gps/permgroup.py` selected entities; character
table comparisons with GAP as oracle.

---

## M7 — Number fields, function fields, valuations, and p-adics

**Purpose**: Number field arithmetic, their rings of integers, ideals, class groups, unit
groups, and local arithmetic.

**Sections in scope**: `number_fields`, `function_fields`, `valuations`, `padics`.

**Entity count**: ~1,590 entities in the first three; 535 in `padics`.

**Prerequisites**: M1 (integer arithmetic), M2 (polynomial factorization for field extensions),
M3 (Gröbner bases for ideal operations), M4 (lattice reduction for LLL-based algorithms in
number fields).

**Capability records** (all need new records):

- `numberfields.arithmetic` — algebraic integer ring, basis, trace, norm, discriminant
- `numberfields.ideal-arithmetic` — ideal products, norms, prime factorization of ideals
- `numberfields.class-group` — class group and class number
- `numberfields.unit-group` — Dirichlet's theorem, generators of the unit group
- `numberfields.embeddings` — real and complex embeddings, conjugates
- `padics.arithmetic` — p-adic integer and rational arithmetic, Newton lifting
- `padics.hensel` — Hensel's lemma and p-adic factorization
- `valuations.*` — discrete valuation rings, valuation of an element

**Key reuse decisions**: Survey at capability-writing time. At the current survey date, Mathlib
has number field theory (`Mathlib.NumberTheory.NumberField.*`) but most of it is
`formalized-not-executable`. Hex has no number-field component in `hex.toml`. PARI is the
reference backend. License check required before any PARI algorithm translation.

**Acceptance**: Sage doctests in `number_fields/`, PARI as oracle for class-group and unit-group
computations.

---

## M8 — Combinatorics and graph theory

**Purpose**: Combinatorial structures and graph algorithms.

**Sections in scope**: `combinat`, `graphs`, `matroids`, `quivers`, `dynamics` (symbolic
dynamics), `sat`.

**Entity count**: ~10,350 entities (combinat is the largest single section: 8,177 entities).

**Prerequisites**: M1 (integer arithmetic for counts and generating functions), M2 (polynomial
arithmetic for generating functions), M6 (permutation groups for symmetry classes).

**Capability records** (partially exist in `graphs.toml`; `combinat` needs extensive new
records given its size):

- Graph algorithms: `graphs.isomorphism` (nauty, Hex `NautyFFI`), `graphs.coloring`,
  `graphs.cycles`, `graphs.flow`, `graphs.planarity`, ...
- Combinatorics: generating functions, partitions, tableaux, symmetric functions, species, ...
- Matroids: representability, circuits, rank function
- SAT: DPLL/CDCL decision procedure with certified unsatisfiability

**Key reuse decisions**:
- `hex.Hex.bench-oracles` includes nauty FFI: `adaptable`
- Mathlib has `Finset`, `Finpartition`, `SimpleGraph.*`: check executability per component
- Combinat is the largest section and will require the most exclusion analysis (many methods
  are specializations of generic combinatorial constructions)

**Acceptance**: The combinat section has 47,908 doctests — the largest oracle corpus in the
manual. The scale of this milestone means acceptance runs must be automated against the oracle
rather than hand-verified.

---

## M9 — Discrete geometry, topology, and differential geometry

**Purpose**: Polytopes, simplicial complexes, manifolds, hyperbolic geometry, and
knot theory.

**Sections in scope**: `discrete_geometry`, `topology` (simplicial/cell complexes),
`hyperbolic_geometry`, `knots`, `manifolds`, `riemannian_geometry`.

**Entity count**: ~2,774 entities.

**Prerequisites**: M4 (linear algebra for polytope computations), M5 (chain complexes for
simplicial homology), M6 (groups for deck transformations and knot groups).

**Capability records** (all need new records):

- Polytope operations: H-representation, V-representation, face lattice, volume
- Simplicial homology: (depends on M5 chain-complex homology)
- Knot invariants: Alexander polynomial, Jones polynomial
- Manifold atlas operations: tangent vectors, differential forms
- Hyperbolic geometry: upper half-plane and disk model operations

**Key reuse decisions**: Survey at capability-writing time.

**Acceptance**: Sage doctests in respective sections; independent oracle cross-checks for
polytope volumes and knot invariants.

---

## M10 — Arithmetic geometry

**Purpose**: Elliptic curves, hyperelliptic curves, schemes, and arithmetic geometry.

**Sections in scope**: `arithmetic_curves`, `curves`, `schemes`.

**Entity count**: ~2,176 entities.

**Prerequisites**: M2 (polynomial arithmetic), M3 (ideal and Gröbner computations),
M7 (number fields and p-adic arithmetic for curves over number fields), M4 (lattice reduction
for Mordell-Weil group computations).

**Capability records** (partially exist in `arithmetic-geometry.toml`):

- `elliptic.point-group-law` — chord-and-tangent addition (Mathlib `EllipticCurve.Affine`, `reusable`)
- `elliptic.finite-field-point-count` — BSGS and PARI `ellcard` (`adaptable`)
- `elliptic.local-reduction` — Tate's algorithm (`adaptable`)
- `elliptic.global-minimal-model`
- `elliptic.mordell-weil` — rational points, 2-descent (significant PARI dependency)
- `schemes.*` — affine and projective schemes, structure sheaf

**Key reuse decisions**:
- Mathlib `EllipticCurve.Affine.Formula`: `reusable` for point arithmetic
- PARI/GP: oracle for all higher-level number-theoretic computations over elliptic curves;
  not a computation provider

**Acceptance**: Sage doctests in `arithmetic_curves/`; point-count comparisons with PARI;
Mordell-Weil rank comparisons.

---

## M11 — Modular forms, L-functions, and analytic number theory

**Purpose**: Modular forms, modular symbols, Hecke operators, L-functions.

**Sections in scope**: `modfrm`, `modsym`, `hecke`, `lfunctions`, `arithgroup`,
`modabvar`, `drinfeld_modular`, `drinfeld_modules`, `anderson_motives`.

**Entity count**: ~3,250 entities.

**Prerequisites**: M7 (number fields), M10 (elliptic curves for modularity connections),
M6 (groups for modular group arithmetic), M4 (linear algebra for Hecke matrix computations).

**Notes**: This is the most mathematically specialized milestone. The capability records will
require active research input from the domain owners. Many algorithms in this area have no
existing Lean implementation. PARI, eclib, and flint are the primary reference backends.

**Acceptance**: Sage doctests; PARI and eclib as oracles for L-function computations.

---

## M12 — Calculus, special functions, and numerical analysis

**Purpose**: Symbolic calculus, special functions, asymptotic expansions, numerical
optimization, real and complex number arithmetic.

**Sections in scope**: `calculus`, `functions`, `asymptotic`, `constants`, `numerical`,
`rings_numerical`, `euclidean_spaces`, `probability`, `stats`.

**Entity count**: ~2,330 entities.

**Prerequisites**: M2 (power series for symbolic calculus backends), M1 (exact arithmetic
underpinning interval arithmetic).

**Capability records** (partially exist in `numerical-analysis.toml`; symbolic calculus and
special functions need new records):

- Symbolic differentiation and integration (finite algorithm families only)
- Special functions: gamma, zeta, Bessel, hypergeometric
- Asymptotic expansions with explicit big-O terms
- Interval arithmetic and rigorous enclosures
- Numerical optimization: Newton, quasi-Newton, interior point
- Probability distributions and statistics

**Notes**: The boundary between exact symbolic and approximate numerical computation is
explicit in every capability record. Sage's symbolic calculus delegates much to Maxima;
the native computation must specify which computations are exact (e.g., derivative of a
polynomial) and which are approximate with stated error bounds.

**Acceptance**: Sage doctests; exact computations compared with symbolic expected values;
approximate computations compared with the oracle within the stated error bound.

---

## M13 — Coding theory, cryptography, game theory, and remaining discrete mathematics

**Purpose**: Error-correcting codes, cryptographic primitives, matroids, SAT, and game theory.

**Sections in scope**: `coding`, `cryptography`, `game_theory`, `games`, `logic` (propositional
and first-order satisfiability), `quivers` (not covered in M8), `oremodules`.

**Entity count**: ~1,000 entities.

**Prerequisites**: M1 (finite-field arithmetic for linear codes and crypto), M2 (polynomial
arithmetic for cyclic codes and crypto), M4 (linear algebra for syndrome decoding), M6 (groups
for group-theoretic crypto).

**Notes**: Cryptography work requires explicit licence review before any implementation
translates Sage's existing code (GPL-2.0-or-later). Native Lean algorithms can implement the
mathematical operations independently.

**Acceptance**: Sage doctests; independently established mathematical results as oracles.

---

## M14 — Categories, coercions, and infrastructure

**Purpose**: The Sage category framework, coercion system, and the remaining
implementation-infrastructure sections that have mathematical content.

**Sections in scope**: `categories`, `sets`, `monoids`, `structure` (mathematical content
only), `coercion` (mathematical map obligations only), `semirings` (any remaining entries).

**Entity count**: ~3,000 entities (most of `categories`).

**Prerequisites**: M0 through M3 (the category operations in Sage correspond to algebraic
structures implemented in those milestones).

**Notes**: The `categories` section is owned by `lean-categories` for mathematical semantics.
Most Sage category methods are already registered through `inventory/categories/`. The work
here is completing the coverage accounting: categorizing every entity as either (a) a
capability already implemented in an earlier milestone through a catalogue entry, (b) a
framework helper excluded with a justified reason, or (c) a gap to report to `lean-categories`.

**Acceptance**: `sage-inventory unaccounted inventory/sage/index inventory/capabilities categories`
returns nothing.

---

## Dependency summary

```
M0 (foundation)
├── M1 (integers, rationals, modular arithmetic)
│   ├── M2 (univariate polynomials, power series)
│   │   ├── M3 (multivariate polynomials, Gröbner, commutative algebra)
│   │   │   └── M10 (arithmetic geometry) ──────────────────────────┐
│   │   └── M12 (calculus, special functions)                        │
│   ├── M4 (linear algebra, matrices, lattices)                      │
│   │   ├── M5 (homological algebra, chain complexes)                │
│   │   └── M9 (discrete geometry, topology) ◄── M5                 │
│   └── M6 (finite groups, representations) ──────────────────────► M10
│       └── M8 (combinatorics, graphs) ◄── M2, M6                   │
│           └── M13 (coding, crypto) ◄── M1, M2, M4, M6             │
├── M7 (number fields, valuations, p-adics) ◄── M2, M3, M4 ────────► M10
│   └── M11 (modular forms, L-functions) ◄── M7, M10, M6, M4
└── M14 (categories, infrastructure) ◄── M0 through M3
```

Parallelism is permitted when the dependency edges permit it. M1 and M14 (accounting portion
only) can proceed in parallel after M0. M2 and M4 can proceed in parallel after M1. M5 and
M6 can proceed in parallel after M4. M8 and M9 can proceed in parallel after their respective
prerequisites.

---

## Cross-milestone obligations

These items span multiple milestones and must be tracked centrally:

| Obligation | Owner milestone | Notes |
| --- | --- | --- |
| Hex quotient–`AdjoinRoot` formal bridge | M3 (or explicitly deferred) | Named in `docs/architecture.md`; the probe leaves `interpret` as `noncomputable` |
| DSL native-dispatch port | DSL owner | Specified in `docs/architecture.md`; required before any M1+ computation reaches the kernel |
| Hex `HexSmith` and `HexHermite` release status | M4 | Surveyed as unreleased; verify at import time |
| `lean-categories` catalogue gaps | Per milestone | Each missing catalogue id goes to that owner; track in issues |
| Oracle image provenance | All milestones | Oracle image pinned in `docs/oracles.md`; image source revision differs from indexed baseline |
| GPL licence review | M13 (crypto), any direct translation | Sage is GPL-2.0-or-later; translations require review |

---

## What this roadmap is not

This document is not a Gantt chart and does not assign calendar dates. It is a dependency order
and an acceptance condition structure. The speed at which individual milestones proceed depends
on the available formalized mathematics, executable algorithms, and implementer capacity at the
time each milestone begins.

A milestone may be split further into independently shippable sub-milestones by its specification
issues when the entity count or mathematical complexity warrants it. The splits must respect the
same dependency order. The constitution's completion condition — `sage-inventory unaccounted`
returns nothing for every mathematical section — is unchanged by any split.
