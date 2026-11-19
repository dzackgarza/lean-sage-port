# Specification Quality Checklist: Euclidean arithmetic

**Purpose**: Check the feature specification before implementation planning.
**Created**: 2026-11-17
**Feature**: [spec.md](../spec.md)

## Content quality

- [x] User stories state public mathematical results and independent acceptance.
- [x] The specification uses existing Euclidean objects and no new representation type.
- [x] Required sections contain domain-specific contracts.

## Requirement completeness

- [x] The generic Euclidean laws and the selected integer remainder sign are distinct.
- [x] Unit normalization is explicit for integers, field polynomials and rationals.
- [x] Pair/list and zero cases are stated for gcd, lcm and xgcd.
- [x] Bézout coefficients are compared by identity without an unsupported minimality bound.
- [x] Source tests and same-input oracles define acceptance.
- [x] Missing upstream catalogue and normalization contracts are named as readiness gaps.

## Feature readiness

- [x] Each capability id maps to a user story, functional requirements and future tasks.
- [x] Actual computational dependencies are separated from comparison assertions.
- [x] The feature does not claim implementation readiness before owner resolution.

The custom mathematical checklist remains reviewer-owned.
