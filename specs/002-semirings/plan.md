# Implementation Plan: Semiring computations

**Feature directory**: `specs/002-semirings`
**Specification**: [spec.md](spec.md)
**Status**: Specification for later implementation; no semiring runtime is implemented by this plan.

## Technical context

- **Language/build**: Lean 4 and Lake, using the repository's `lean-toolchain` and `lakefile.toml`.
- **Mathematical owners**: Mathlib and `lean-categories` for semiring objects and operations; `lean-cas-dsl` for catalogue ids and user language. This repository owns executable realizations.
- **Existing computation**: Lean core `Nat` arithmetic and Mathlib's `MinTropical (WithTop R)` / `MaxTropical (WithBot R)` semiring operations are reusable. `WithTop.map` and `WithBot.map` already lift finite/infinity values. Mathlib's matrix operations and Hex dense matrices are candidates for the separately owned `matrices.arithmetic` capability; the representation relation remains an integration obligation.
- **Reference baseline**: Sage 11.0.beta5 at `c00171e47d6e68d8148d7ee10c4dd77b71a97662`; exact source selectors and acceptance doctests are in `inventory/capabilities/semirings.toml`.
- **Testing**: Source doctests and same-input Sage oracle comparisons through `docs/oracles.md`; small mathematical assertions through public Lean operations. Lean builds run locally through `just test`; CI repeats it.
- **Performance**: Functional correctness first. Closure and cycle mean must complete on the small matrices in their selected source doctests; later optimization requires measurements.
- **Domain boundary**: Exact tropical values over a linearly ordered additive commutative group with decidable order. Cycle means require exact division by positive path lengths, supplied by the rational-base scope.

## Constitution check

| Principle | Design consequence |
| --- | --- |
| Native computation | Algorithms run in Lean; Sage is an oracle. |
| Existing mathematical authority | Use Mathlib/`lean-categories` semantics and catalogue contracts; send missing operation ids to their owner. |
| Reuse before new algorithms | Reuse `Nat` and Mathlib's tropical semiring types and operations; inspect Mathlib/Hex matrix implementations; use Sage's Floyd-Warshall and Karp source as algorithm references. |
| Generality and composition | Retain tropical base, orientation, infinity, matrix indices and morphism endpoints. |
| Independent acceptance | Select source doctests; compare same runtime input; use cycle enumeration only for the identified independent mean check. |

The reuse and native-computation choices pass. The owner-contract gate remains open: catalogue gaps must be resolved at their owners before implementation of those public operations. This plan does not create substitute local ids.

## Phase 0: Research and decisions

[research.md](research.md) records source-grounded domain limits, reuse and algorithm references. The owner-controlled catalogue gaps are unresolved foundational contracts, not routine implementation choices.

## Phase 1: Design and contracts

[data-model.md](data-model.md) describes mathematical data retained by runtime values and maps. [contracts/semiring-computations.md](contracts/semiring-computations.md) gives public operation signatures and failure behavior. [quickstart.md](quickstart.md) identifies the acceptance route without duplicating Sage's test corpus.

## Project structure for later implementation

```text
LeanSagePort/Semirings/Natural.lean
LeanSagePort/Semirings/Tropical.lean
LeanSagePort/Semirings/TropicalMap.lean
LeanSagePort/Semirings/TropicalMatrix.lean
Acceptance/Semirings.lean
```

These are target paths for work at the native computational owner. `Tropical.lean` should realize Mathlib's existing min/max tropical types under the runtime object contract; it must not define a second tagged tropical arithmetic. The existing package currently builds `Probes`; the implementing change will add the library and acceptance executable to Lake only when they have real callers. The generic matrix operation belongs to `matrices.arithmetic` in `inventory/capabilities/linear-algebra.toml`; semiring matrices consume that capability.

## Dependencies and public completion

`semirings.natural-numbers` is independent. `semirings.tropical-construction` supplies the value type consumed by tropical order and base change. Generic `matrices.arithmetic` plus tropical construction supply the matrices consumed by closure and cycle mean. The cycle-mean algorithm additionally consumes exact rational division. Each task closes only when its public computation works and the selected source cases pass through the native path. Catalogue gaps must be resolved at `lean-categories`/`lean-cas-dsl` before those public operations are claimed.

## Post-design constitution check

No local mathematical ontology or duplicate DSL operation is specified. Exactness and data retention are explicit. The source doctests provide the main independent acceptance corpus. The owner-contract gate remains open for catalogue entries listed as empty in `inventory/capabilities/semirings.toml`; implementation readiness cannot be claimed until they are supplied.
