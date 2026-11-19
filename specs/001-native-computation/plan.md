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
- Validation: `just check-lean <file>` while editing and `just test` (incremental Lean build,
  runtime probes, inventory checks) before each commit; CI repeats `just test`;
  baseline Sage/reference computations as independent oracles.
- Platform: the existing Linux workstation and CI environment.
- Scope: every indexed entity of every module under `src/sage` (66,424 entities in 3,041 modules
  at the baseline). The manual sections name the domains and order the reading; they do not bound it.
- Performance: only bounds intrinsic to a capability; no general optimization phase during reconnaissance.

## Constitution Check

The design preserves upstream semantics, executable obligations and selected structure. Existing
source tests and oracle outputs determine acceptance. The architecture remains a candidate until
runtime probes succeed. Full inventory and reuse closure remain requirements, not assumptions.
The master specification does not authorize implementation through unresolved foundational choices.

## Project Structure

| Owner | Contract or evidence |
| --- | --- |
| `inventory/domains.toml` | Manual sections: domain names, dispositions and capability-file routing |
| `inventory/reconnaissance-worklog.toml` | Source-reading batches; the modules that a source-reconciled batch names |
| `inventory/reconnaissance.json`, `inventory/reconnaissance-entities.jsonl.gz` | Generated ledger: the state of every module and entity |
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
module selection. A batch is a set of named modules from one Sage manual section, from one
tightly coupled group of sections, or from the modules outside the manual that those sections
import. For every batch, the agent must:

1. Read the section entry in `inventory/domains.toml`, the `modules.jsonl` rows of the batch's
   modules, all their entity rows (public and underscore), the Sage source files in full, and the
   reference-manual pages.
2. Partition the entities into intrinsic mathematical capabilities, framework operations,
   implementation support, presentation, reference data, or unresolved source questions.
3. Append capability/exclusion records with exact Sage selectors; append unresolved questions to
   an explicit open-work record rather than inventing a capability or silently dropping an entity.
4. For every capability, append its algorithm families, mathematical prerequisites, independent
   tests, reuse decisions, and ownership/catalogue relationship.
5. Append the batch to `inventory/reconnaissance-worklog.toml`, naming each module that was read.
   Mark it `source-reconciled` only when every entity of each named module has its record.
6. Run `sage-inventory coverage` and `sage-inventory reconnaissance`, and confirm with
   `sage-inventory remaining` that the batch's modules have no open entity, before beginning the
   next batch.

The batch order follows computational prerequisites:

| Phase | Batches | Gate before advancing |
| --- | --- | --- |
| R0 | Sage release/index; `categories`; the sections `coercion`, `cpython`, `data_structures`, `databases`, `doctest`, `documentation`, `history_and_license`, `interfaces`, `libs`, `misc`, `parallel`, `plot3d`, `plotting`, `references`, `repl`, `spkg`, `structure`; packages outside the manual that hold no manual module | Every entity of these parts has a reconciled, excluded or category-record state; category rows distinguish catalogue mappings from ownership gaps. |
| R1 | `sets`, `monoids`, `groups` (carrier subset), `semirings`, `rings`, `finite_rings`, `rings_standard`, `modules`, `tensor_free_modules` | Core carriers, maps, constructors, and inherited operations have contracts and reuse owners. |
| R2 | `polynomial_rings`, `power_series`, `noncommutative_polynomial_rings`, `algebras`, `quat_algebras`, `quivers`, `homology`, `resolutions` | Polynomial, quotient, module, algebra, quaternion and chain-complex constructions have source-backed contracts. |
| R3 | `matrices`, `number_fields`, `function_fields`, `padics`, `valuations`, `quadratic_forms` | Exact linear and arithmetic primitives have executable algorithms and independent acceptance sources. |
| R4 | `groups` (higher operations), `combinat`, `graphs`, `matroids`, `coding`, `cryptography`, `logic`, `sat`, `game_theory`, `games`, `oremodules` | Discrete capabilities are grouped by intrinsic operation, not Sage class names; their graph prerequisites remain explicit even when implementation follows later. |
| R5 | `curves`, `arithmetic_curves`, `schemes`, `manifolds`, `topology`, `riemannian_geometry`, `hyperbolic_geometry`, `euclidean_spaces`, `knots`, `discrete_geometry` | Geometric objects retain maps, charts, base fields, and defining data through computation. |
| R6 | `calculus`, `functions`, `numerical`, `rings_numerical`, `stats`, `probability`, `asymptotic`, `dynamics`, `constants` | Approximate and symbolic contracts state precision, error, convergence, and exactness explicitly. |
| R7 | `modfrm`, `modsym`, `modabvar`, `drinfeld_modules`, `drinfeld_modular`, `anderson_motives`, `hecke`, `lfunctions`, `arithgroup`, `diophantine_approximation` | Specialized arithmetic domains identify their mathematical owner, algorithmic source, and prerequisite path. |

This table is the single owner of the phase of a section; the worklog does not store phases.
`groups` is read in two phases: its carrier constructions in R1 and its higher operations in R4.
A module outside the manual is read in the earliest phase of the manual sections whose modules
import it; the module ledger `inventory/reconnaissance.json` names those sections in the field
`imported_by_sections`. When that field is empty, the module is read in the earliest phase of the
manual sections that hold modules of its package (the field `part`, such as `sage.rings`). A
package with no manual module is read in R0.

The R-phase table is a source-reading and reconciliation grouping, not a second dependency
graph. A capability may therefore name a prerequisite whose source batch is in a later R phase;
that edge remains an explicit implementation gate in `inventory/dependency-graph.json` and must
be satisfied before the dependent computation is implemented. Within a phase, batches may run in
parallel only when their source and ownership questions are independent. The live progress
measure is the state count of `inventory/coverage.json`: an entity closes only as `reconciled`,
`excluded` or `category-record`, and the first two require a source-reconciled batch that names
its module. A selector that matches an unread module leaves its entities `scoped`; generated
counts alone never close a batch.

## Architectural validation

Use the three experiments specified in `docs/architecture.md`: runtime quotient and extension
construction, generic matrix/polynomial operations over contrasting coefficient domains, and
composition retaining maps and selected data. Compare with Sage on the same input data.
Publish passing CI evidence before marking any architecture decision accepted.

## Readiness

[Issue 1](https://github.com/dzackgarza/lean-sage-port/issues/1) owns the completion gate and current
work state. The open entities that `sage-inventory remaining` reports for each section and
package define the remaining source survey. Specifications,
probes and dependency issues must undergo independent review and correction before large-scale
implementation. This plan states the derivation method; issue dependencies state the live order.
