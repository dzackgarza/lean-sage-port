# Master product specification

## Product identity

**Lean Sage Port** targets native, executable Lean 4 computations for the mathematical
objects and operations admitted by the `lean-categories` and `lean-cas-dsl` catalogues. The
baseline is SageMath **11.0.beta5**, indexed at commit
`c00171e47d6e68d8148d7ee10c4dd77b71a97662`. The product scope is the complete pinned Sage
manual taxonomy below; source accounting is recorded in the reconnaissance and capability
inventories, while executable acceptance is established separately by same-input comparison
with the pinned Sage oracle.

## Scope table

The source of truth for section disposition is [`inventory/domains.toml`](../../inventory/domains.toml);
this table is a readable assembled view, not a second authority.

| section_id | title | disposition | milestone | status |
| --- | --- | --- | --- | --- |
| `algebras` | Algebras | mathematical | M3 | in-scope |
| `anderson_motives` | Anderson Motives | mathematical | M11 | in-scope |
| `arithgroup` | Arithmetic Subgroups of {\rm SL}_2(\ZZ) | mathematical | M11 | in-scope |
| `arithmetic_curves` | Elliptic and Hyperelliptic Curves | mathematical | M10 | in-scope |
| `asymptotic` | Asymptotic Expansions | mathematical | M12 | in-scope |
| `calculus` | Symbolic Calculus | mathematical | M12 | in-scope |
| `categories` | Categories | mathematical | M0 | in-scope |
| `coding` | Coding Theory | mathematical | M13 | in-scope |
| `coercion` | Coercion | implementation-support | — | excluded |
| `combinat` | Combinatorics | mathematical | M8 | in-scope |
| `constants` | Mathematical Constants | mathematical | M12 | in-scope |
| `cpython` | Python Technicalities | implementation-support | — | excluded |
| `cryptography` | Cryptography | mathematical | M13 | in-scope |
| `curves` | Plane and Space Curves | mathematical | M10 | in-scope |
| `data_structures` | Data Structures | implementation-support | — | excluded |
| `databases` | Databases | reference-data | — | excluded |
| `diophantine_approximation` | Diophantine Approximation | mathematical | M7 | in-scope |
| `discrete_geometry` | Combinatorial and Discrete Geometry | mathematical | M9 | in-scope |
| `doctest` | Test Framework | implementation-support | — | excluded |
| `documentation` | Documentation System | implementation-support | — | excluded |
| `drinfeld_modular` | Drinfeld Modular Forms | mathematical | M11 | in-scope |
| `drinfeld_modules` | Drinfeld Modules | mathematical | M11 | in-scope |
| `dynamics` | Discrete Dynamics | mathematical | M8 | in-scope |
| `euclidean_spaces` | Euclidean Spaces and Vector Calculus | mathematical | M12 | in-scope |
| `finite_rings` | Finite Rings and Fields | mathematical | M1 | in-scope |
| `function_fields` | Function Fields | mathematical | M7 | in-scope |
| `functions` | Elementary and Special Functions | mathematical | M12 | in-scope |
| `game_theory` | Game Theory | mathematical | M13 | in-scope |
| `games` | Games | mathematical | M13 | in-scope |
| `graphs` | Graph Theory | mathematical | M8 | in-scope |
| `groups` | Groups | mathematical | M6 | in-scope |
| `hecke` | General Hecke Algebras and Hecke Modules | mathematical | M11 | in-scope |
| `history_and_license` | History and License | implementation-support | — | excluded |
| `homology` | Chain Complexes and their Homology | mathematical | M5 | in-scope |
| `hyperbolic_geometry` | Hyperbolic Geometry | mathematical | M9 | in-scope |
| `interfaces` | Interpreter Interfaces | implementation-support | — | excluded |
| `knots` | Knot Theory | mathematical | M9 | in-scope |
| `lfunctions` | L-Functions | mathematical | M11 | in-scope |
| `libs` | C/C++ Library Interfaces | implementation-support | — | excluded |
| `logic` | Symbolic Logic | mathematical | M13 | in-scope |
| `manifolds` | Manifolds and Differential Geometry | mathematical | M9 | in-scope |
| `matrices` | Matrices and Spaces of Matrices | mathematical | M4 | in-scope |
| `matroids` | Matroid Theory | mathematical | M8 | in-scope |
| `misc` | Utilities | implementation-support | — | excluded |
| `modabvar` | Modular Abelian Varieties | mathematical | M11 | in-scope |
| `modfrm` | Modular Forms | mathematical | M11 | in-scope |
| `modsym` | Modular Symbols | mathematical | M11 | in-scope |
| `modules` | Vectors and Modules | mathematical | M4 | in-scope |
| `monoids` | Monoids | mathematical | M14 | in-scope |
| `noncommutative_polynomial_rings` | Noncommutative Polynomials | mathematical | M13 | in-scope |
| `number_fields` | Number Fields | mathematical | M7 | in-scope |
| `numerical` | Numerical Optimization | mathematical | M12 | in-scope |
| `oremodules` | Modules over Ore rings | mathematical | M13 | in-scope |
| `padics` | p-adic Numbers | mathematical | M7 | in-scope |
| `parallel` | Parallel Computing | implementation-support | — | excluded |
| `plot3d` | 3D Graphics | presentation | — | excluded |
| `plotting` | 2D Graphics | presentation | — | excluded |
| `polynomial_rings` | Commutative Polynomials | mathematical | M2–M3 | in-scope |
| `power_series` | Power Series and Laurent Series | mathematical | M2 | in-scope |
| `probability` | Probability | mathematical | M12 | in-scope |
| `quadratic_forms` | Quadratic Forms | mathematical | M4 | in-scope |
| `quat_algebras` | Quaternion Algebras | mathematical | M3 | in-scope |
| `quivers` | Quivers | mathematical | M8 | in-scope |
| `references` | Bibliographic References | implementation-support | — | excluded |
| `repl` | Command Line Interface | implementation-support | — | excluded |
| `resolutions` | Resolutions | mathematical | M5 | in-scope |
| `riemannian_geometry` | Parametrized Surfaces | mathematical | M9 | in-scope |
| `rings` | Rings | mathematical | M3 | in-scope |
| `rings_numerical` | Real and Complex Numbers | mathematical | M12 | in-scope |
| `rings_standard` | Integers and Rational Numbers | mathematical | M1 | in-scope |
| `sat` | SAT solvers | mathematical | M13 | in-scope |
| `schemes` | Schemes | mathematical | M10 | in-scope |
| `semirings` | Semirings | mathematical | M2 | in-scope |
| `sets` | Sets | mathematical | M14 | in-scope |
| `spkg` | External Packages | implementation-support | — | excluded |
| `stats` | Statistics | mathematical | M12 | in-scope |
| `structure` | Parents and Elements | implementation-support | — | excluded |
| `tensor_free_modules` | Tensors on Free Modules of Finite Rank | mathematical | M4 | in-scope |
| `topology` | Cell Complexes, Simplicial Complexes, and Simplicial Sets | mathematical | M9 | in-scope |
| `valuations` | Discrete Valuations | mathematical | M7 | in-scope |

## Output-contract taxonomy

These are the four established output guarantees from [`docs/capability-records.md`](../../docs/capability-records.md).
No fifth category is permitted without a specification amendment.

| Category | Definition | Existing capability example |
| --- | --- | --- |
| `exact` | The computation returns the mathematically correct value under its stated input domain, with no numerical error. | `hecke.documented-algorithms` in [`inventory/capabilities/hecke.toml`](../../inventory/capabilities/hecke.toml). |
| `approximate` | The result is an approximation with a stated precision or error bound, enclosure, or estimator semantics. | `floating.runtime-precision-real-arithmetic` in [`inventory/capabilities/numerical-analysis.toml`](../../inventory/capabilities/numerical-analysis.toml). |
| `heuristic` | The result may be wrong and no correctness bound is claimed; the failure mode is recorded in `exactness_notes`. | `integers.probable-primality` in [`inventory/capabilities/integers-and-rationals.toml`](../../inventory/capabilities/integers-and-rationals.toml). |
| `conditional` | The result is correct under a named mathematical, convergence, field, or backend hypothesis recorded in `exactness_notes`. | `homology.chain-complexes` in [`inventory/capabilities/homology.toml`](../../inventory/capabilities/homology.toml). |

## Completion condition

The product is complete only when both independent tiers pass.

### Tier 1 — source and capability coverage

The following command is runnable from the repository root and checks every section declared
in `inventory/domains.toml`:

```sh
for section in $(python3 -c 'import tomllib; print(" ".join(s["id"] for s in tomllib.load(open("inventory/domains.toml","rb"))["section"] if s["disposition"] == "mathematical"))'); do
  (cd tools/inventory && uv run sage-inventory unaccounted ../../inventory/sage/index ../../inventory/capabilities "$section" --categories ../../inventory/categories/sage-categories.toml) || exit 1
done
```

The generated reports are [`inventory/coverage.json`](../../inventory/coverage.json),
[`inventory/reconnaissance.json`](../../inventory/reconnaissance.json), and
[`inventory/reconnaissance-scope.json`](../../inventory/reconnaissance-scope.json). Tier 1
accounts for source entities; it does not imply that native Lean code exists.

An entity is **accounted for** exactly when a capability record has a selector matching that
entity or a justified `[[exclusion]]` records why it is outside executable mathematical scope.
Category records account for the `categories` section under the same rule; they do not turn
source accounting into implementation acceptance.

### Tier 2 — native implementation acceptance

For every capability selector, execute the same admissible runtime input against the native
Lean implementation and the pinned Sage oracle image
`ghcr.io/dzackgarza/sage@sha256:dadfded3a44fb8314266afb3225855b5ba531b49a53ac70ed844b457435fcfc0`.
Compare canonical exact results by mathematical equality; compare approximate, heuristic and
conditional results using the contract and assumptions in the capability record. Tier 2 is
accepted only when every selected entity has passed its capability's oracle comparisons.

## Ownership boundaries

| Component type | Owner | Traceable example |
| --- | --- | --- |
| Mathematical object identity, axioms, and catalogue ids | `lean-categories` | `catalogue.cat.rings` in [`inventory/reuse/lean-categories.toml`](../../inventory/reuse/lean-categories.toml). |
| Admission, wire types, kernel protocol, and realization boundary | `lean-cas-dsl` | The `lean-cas-dsl` source entry and `CasCatalogue` declarations recorded in [`inventory/reuse/lean-categories.toml`](../../inventory/reuse/lean-categories.toml). |
| Formal mathematical definitions and noncomputable proofs | Mathlib | `mathlib.linalg.rank` in [`inventory/reuse/mathlib-core.toml`](../../inventory/reuse/mathlib-core.toml). |
| Released executable algorithms | `leanprover/hex` | `hex.HexArith.extended-gcd` in [`inventory/reuse/hex.toml`](../../inventory/reuse/hex.toml). |
| Native computation under an admitted catalogue contract | This repository | Native capability records and implementations in `inventory/capabilities/` and the Lean source tree. |
| Independent reference oracle | Sage, PARI, GAP, FLINT, and other cited engines | Reference-engine provenance in [`inventory/references/`](../../inventory/references/). |

Routing rule: report a new mathematical object or stable id to `lean-categories` or
`lean-cas-dsl`; reuse an existing Hex algorithm where it covers the contract; put only the
native adapter or computation owned by this repository here.

## Cross-product obligations

These obligations are tracked by the milestone roadmap rather than duplicated here.

| Obligation | Blocking scope | Owner |
| --- | --- | --- |
| Hex `FpPoly.Quotient` ↔ `AdjoinRoot` formal bridge | M3 quotient-ring acceptance | This repository; [`Probes/RuntimeQuotient.lean`](../../Probes/RuntimeQuotient.lean) is the current probe. |
| DSL `NativeCompute` port at the `Realize.send` boundary | M1 and later DSL integration | `lean-cas-dsl`, upstream issue 85. |
| HexSmith and HexHermite release status | M4 matrix and lattice acceptance | Verify at import and retain the result in the relevant capability record. |
| GPL licence review for crypto and coding translations | M13 | Required before translating affected source or algorithms. |
| Oracle image currency | All milestones | [`docs/oracles.md`](../../docs/oracles.md) owns the image identity and source-revision warning. |

## Specification hierarchy

| Level | Authority | Pointer |
| --- | --- | --- |
| Project constitution | Permanent scope and ownership commitments | [`docs/constitution.md`](../../docs/constitution.md) |
| Master product contract | This global scope, taxonomy, completion condition, and ownership boundary | This document |
| Reconnaissance specification | Source indexing, entity accounting, and evidence ledger | [`specs/001-native-computation/spec.md`](../001-native-computation/spec.md) |
| Dependency-ordered roadmap | Milestones, prerequisites, and cross-milestone obligations | [`specs/004-milestones/plan.md`](../004-milestones/plan.md) |
| Domain specifications | Section-level routes to capability contracts | [`docs/domain-specifications.md`](../../docs/domain-specifications.md) |
| Capability records | One mathematical operation/construction, its hypotheses, reuse, and oracle contract | [`docs/capability-records.md`](../../docs/capability-records.md) and [`inventory/capabilities/`](../../inventory/capabilities/) |
| Native implementation specifications | Per-milestone executable work and acceptance | [`specs/004-milestones/`](../004-milestones/) and the owning domain specs |
