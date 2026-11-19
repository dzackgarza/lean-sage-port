# Implementation Plan: Euclidean arithmetic

**Feature directory**: `specs/003-euclidean-arithmetic`
**Specification**: [spec.md](spec.md)
**Status**: Specification only; owner contracts remain open.

## Technical context

- **Language/build**: Lean 4 and Lake at the repository's resolved versions; Lean compiles in CI.
- **Mathematical owner**: Mathlib `EuclideanDomain` supplies quotient/remainder, a well-founded relation and generic gcd/xgcd. `lean-categories` owns the mathematical object and operation catalogue; `lean-cas-dsl` owns stable language ids.
- **Executable reuse**: Lean core integer division/gcd; Mathlib generic Euclidean algorithms when the instance is executable; Hex exact integer division and released dense polynomial divMod/gcd/xgcd. See `inventory/reuse/mathlib-core.toml` and `inventory/reuse/hex.toml` for declarations and revision status.
- **Reference**: Official Sage 11.0.beta5 via `inventory/sage/release.toml`; capability selectors in `inventory/capabilities/integers-and-rationals.toml`; additional univariate polynomial source doctests at `sage.rings.polynomial.polynomial_element:Polynomial.quo_rem`, `Polynomial.gcd`, `Polynomial.lcm`, `Polynomial.xgcd`.
- **Testing**: Selected source doctests and same-input Sage oracle checks. Public operation identities supply independent comparison where outputs are noncanonical.
- **Domain**: Executable Euclidean quotient/remainder and decidable equality. Normalized gcd needs a selected associate normal form; rational gcd/lcm has its own source convention. Integer quotient/remainder has the Sage floor convention.

## Constitution check

| Principle | Consequence |
| --- | --- |
| Native computation | Lean computes all public results; Sage supplies source tests and oracle output. |
| Existing mathematical authority | Reuse Mathlib EuclideanDomain and upstream catalogue operations; no new local Euclidean type. |
| Reuse before new algorithms | Dispatch to existing Lean core, Mathlib and Hex implementations at their supported domains. |
| Generality and composition | Keep the coefficient domain and selected associate convention in outputs. |
| Independent acceptance | Check reconstruction, decrease, gcd divisibility and Bézout identities, not a particular certificate tuple. |

The source and reuse choices pass. Catalogue operation and normalization ownership remain unresolved; the feature cannot enter implementation until the upstream contracts are specified.

## Phase 0: Research

[research.md](research.md) records the source conventions, reusable declarations and the distinctions between generic Euclidean laws and domain-specific normalization.

## Phase 1: Design and contracts

[data-model.md](data-model.md) records retained mathematical data. [contracts/euclidean-operations.md](contracts/euclidean-operations.md) gives public signatures and failure behavior. [quickstart.md](quickstart.md) identifies the source acceptance route.

## Later implementation structure

```text
LeanSagePort/Euclidean/Division.lean
LeanSagePort/Euclidean/Gcd.lean
LeanSagePort/Euclidean/Xgcd.lean
Acceptance/Euclidean.lean
```

These paths are target modules at the native computation owner, not new semantic types. Operations should reuse the current `EuclideanDomain` instance and existing algorithms. Integer quotient convention and unit normalization are explicit selections. Polynomial storage may use Hex dense representations with a documented realization of the Mathlib polynomial object.

## Dependency order

Division with remainder supplies an input to both gcd and extended gcd. Gcd and xgcd can run separately once division and selected normalization are available; xgcd does not computationally consume the gcd producer. List operations fold the pair contracts. Exact division consumes quotient/remainder plus a zero-remainder check. The owner-controlled catalogue and normalization contracts precede exposing each public operation. No algorithmic edge is inferred from a theorem merely comparing two outputs.

## Post-design constitution check

The design does not duplicate Mathlib's generic Euclidean algorithms or introduce a new number system. It distinguishes the exact integer remainder convention from the generic well-founded decrease law, and it compares noncanonical certificates mathematically. Owner catalogue gaps are explicit. Implementation readiness is pending their resolution.
