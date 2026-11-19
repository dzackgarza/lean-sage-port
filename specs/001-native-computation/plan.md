# Implementation Plan: Native mathematical computation

**Branch**: `main` | **Date**: 2026-11-17 | **Spec**: [spec.md](spec.md)

## Summary

Finish reconnaissance and executable architectural validation before authorizing CAS implementation.
Use the existing source index, capability records and reuse surveys. Domain contracts draw their
acceptance from the selected Sage doctests and same-input reference computations.

## Technical Context

- Language: the Lean version in `lean-toolchain`; Python inventory tooling under the committed uv lock.
- Dependencies: the revisions in `lakefile.toml` and the committed Lake manifest, validated
  together by the architectural probe build. Reuse-map revisions identify survey evidence;
  they do not by themselves establish package compatibility.
- Mathematical owners: lean-categories semantics and lean-cas-dsl language/kernel.
- Evidence storage: existing TOML capability/reuse files and generated JSON source indexes.
- Validation: inventory schema/selector checks locally; Lean compilation and runtime probes in CI;
  baseline Sage/reference computations as independent oracles.
- Platform: the existing Linux workstation and CI environment.
- Scope: all mathematical manual sections, with explicit dispositions for implementation-support sections.
- Performance: only bounds intrinsic to a capability; no general optimization phase during reconnaissance.

## Constitution Check

The design preserves upstream semantics, executable obligations and selected structure. Existing
source tests and oracle outputs determine acceptance. The architecture remains a candidate until
runtime probes succeed. Full inventory and reuse closure remain requirements, not assumptions.
The master specification does not authorize implementation through unresolved foundational choices.

## Project Structure

| Owner | Contract or evidence |
| --- | --- |
| `inventory/domains.toml` | Complete manual taxonomy and routing |
| `inventory/capabilities/` | Intrinsic operations, domains, dependencies and oracle pointers |
| `inventory/reuse/` | Lean declarations and executable reuse evidence |
| `inventory/references/` | Algorithm engines and licences |
| `docs/architecture.md` | Runtime realization and ownership contracts, with probe obligations |
| `Probes/` | Executable discriminating architectural experiments |
| `tools/inventory/` | Existing index, schema and coverage commands |
| GitHub issues | Work ownership and computational dependency graph |

## Dependency derivation

Inventory the target before accepting a representation architecture. For each capability,
distinguish abstract results already supplied by upstream mathematics from executable results
consumed by the algorithm. Reuse records provide the first implementation choice. Missing
semantic definitions go to their owner; a noncomputable definition leaves an executable task here.

Create implementation issues from the resulting contracts, preserving capability identifiers.
A dependency edge must name the output the dependent operation consumes. Treat independent
domains as parallel only after shared interfaces and construction dependencies are resolved.
The graph must include the public operation and its composition path, not merely supporting types.

## Reconnaissance loop and execution order

The reconnaissance is executed as an append-only sequence of source batches, not as ad hoc
module selection. A batch is one Sage manual section or one tightly coupled group of sections.
For every batch, the agent must:

1. Read the section entry in `inventory/domains.toml`, its `modules.jsonl` rows, the public
   entity rows, the corresponding Sage source files, and the reference-manual pages.
2. Partition the public entities into intrinsic mathematical capabilities, framework operations,
   implementation support, presentation, reference data, or unresolved source questions.
3. Append capability/exclusion records with exact Sage selectors; append unresolved questions to
   an explicit open-work record rather than inventing a capability or silently dropping an entity.
4. For every capability, append its algorithm families, mathematical prerequisites, independent
   tests, reuse decisions, and ownership/catalogue relationship.
5. Run the selector/schema checks and regenerate coverage before beginning the next batch.

The batch order follows computational prerequisites:

| Phase | Batches | Gate before advancing |
| --- | --- | --- |
| R0 | Sage release/index, category framework, non-mathematical dispositions | Every indexed entity has a source disposition; category rows distinguish catalogue mappings from ownership gaps. |
| R1 | `sets`, `monoids`, `groups`, `semirings`, `rings`, `finite_rings`, `modules`, `tensor_free_modules` | Core carriers, maps, constructors, and inherited operations have contracts and reuse owners. |
| R2 | `polynomial_rings`, `power_series`, `noncommutative_polynomial_rings`, `algebras`, `quivers`, `homology`, `resolutions` | Polynomial, quotient, module, algebra, and chain-complex constructions compose over the R1 carriers. |
| R3 | `matrices`, `linear_algebra`, `polynomial_algorithms`, `number_fields`, `function_fields`, `padics`, `valuations`, `quadratic_forms`, `lattices` | Exact linear and arithmetic primitives have executable algorithms and independent acceptance sources. |
| R4 | `groups`, `combinat`, `graphs`, `matroids`, `coding`, `cryptography`, `logic`, `sat`, `game_theory` | Discrete capabilities are grouped by intrinsic operation, not Sage class names, and depend only on accepted R1–R3 contracts. |
| R5 | `curves`, `arithmetic_curves`, `schemes`, `manifolds`, `topology`, `riemannian_geometry`, `hyperbolic_geometry`, `euclidean_spaces`, `knots` | Geometric objects retain maps, charts, base fields, and defining data through computation. |
| R6 | `calculus`, `functions`, `numerical`, `rings_numerical`, `stats`, `probability`, `asymptotic`, `dynamics`, `constants` | Approximate and symbolic contracts state precision, error, convergence, and exactness explicitly. |
| R7 | `modfrm`, `modsym`, `modabvar`, `drinfeld_modules`, `drinfeld_modular`, `anderson_motives`, `hecke`, `lfunctions` | Specialized arithmetic domains identify their mathematical owner, algorithmic source, and prerequisite path. |

Within each phase, batches may run in parallel only after their prerequisite phase gates pass.
The live progress measure is the number of source entities with an accepted capability/exclusion
record plus the number of explicitly open source questions; generated counts alone never close a
batch.

## Architectural validation

Use the three experiments specified in `docs/architecture.md`: runtime quotient and extension
construction, generic matrix/polynomial operations over contrasting coefficient domains, and
composition retaining maps and selected data. Compare with Sage on the same input data.
Publish passing CI evidence before marking any architecture decision accepted.

## Readiness

[Issue 1](https://github.com/dzackgarza/lean-sage-port/issues/1) owns the completion gate and current
work state. The inventory's unaccounted output defines the remaining source survey. Specifications,
probes and dependency issues must undergo independent review and correction before large-scale
implementation. This plan states the derivation method; issue dependencies state the live order.
