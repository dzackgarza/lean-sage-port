# Implementation Plan: Native mathematical computation

**Branch**: `main` | **Date**: 2026-11-17 | **Spec**: [spec.md](spec.md)

## Summary

Finish reconnaissance and executable architectural validation before authorizing CAS implementation.
Use the existing source index, capability records and reuse surveys. Domain contracts draw their
acceptance from the selected Sage doctests and same-input reference computations.

## Technical Context

- Language: Lean v4.36.0; Python inventory tooling under the committed uv lock.
- Dependencies: Mathlib 6d97e8ad9c32c778e7000ffda543a29488155467 and Hex
  f4b180cfe51692a4e41587d731c92c08a9a63bc4, with the Lake manifest carrying transitive revisions.
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
