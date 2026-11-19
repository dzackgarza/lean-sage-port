# Data model: Master product specification

## Entities

### SectionDisposition

The assignment of a Sage manual section to a treatment category.

| Field | Type | Values |
|---|---|---|
| `section_id` | string | Key from `inventory/domains.toml` |
| `disposition` | enum | `mathematical`, `implementation-support`, `presentation`, `reference-data` |
| `status` | enum | `in-scope`; every section of the source is in scope |
| `milestone_id` | string | Reference to Milestone.id; `M0` for the reconnaissance of a non-mathematical section |

**Source of truth**: `inventory/domains.toml` (disposition) and `docs/domain-specifications.md` (milestone). The master spec assembles these; it does not own them.

### OutputContractCategory

The taxonomy of guarantees a native computation can make about its result.

| Category | Meaning | Required fields in capability record |
|---|---|---|
| `exact` | The result is mathematically correct with no error | `contract` |
| `approximate` | The result has a stated error bound | `contract`, `exactness_notes` (the bound) |
| `heuristic` | The result may be wrong; no bound stated | `exactness_notes` (the failure mode) |
| `conditional` | Correct under a named mathematical hypothesis | `exactness_notes` (the hypothesis, e.g., GRH) |

**Source of truth**: `docs/capability-records.md` §Fields. The master spec formalizes these definitions; it does not add new categories.

### OwnershipBoundary

The assignment of a capability's components to their upstream owners.

| Component type | Owner | What it means |
|---|---|---|
| Object/operation identity (catalogue id) | `lean-categories` | The mathematical type, its axioms, and its abstract computational obligation |
| Language/kernel protocol | `lean-cas-dsl` | Admission, realization, wire types, and backend dispatch |
| Executable algorithm | Hex (if present) or this repository | The compiled Lean function that computes the result |
| Formal proof (noncomputable) | Mathlib | The correctness theorem; does not discharge computational obligation |
| Native computation under DSL contract | This repository | The `NativeCompute` provider for catalogue operations |

**Validation**: A capability record that introduces a new mathematical object definition (not
a computational representation) violates the `lean-categories` ownership boundary. A
capability record that creates a parallel stable-id scheme violates the `lean-cas-dsl`
ownership boundary.

### CompletionCondition

The machine-checkable criterion for the full product being done.

```
complete ⟺
  (∀ manual section or package s outside the manual:
    sage-inventory remaining <index> <capabilities> <categories> <worklog> s = ∅)
  ∧
  (∀ capability c with selectors:
    ∀ entity e selected by c:
      native-result(e) = oracle-result(e))
```

**Coverage tier** (necessary but not sufficient): `sage-inventory remaining` prints nothing
for every section. Measured by `inventory/coverage.json`. Updated by `sage-inventory coverage`.

**Implementation tier** (necessary and sufficient with coverage): Every selected entity passes
same-input oracle comparison against the Sage image in `docs/oracles.md`.

These two tiers are independent. Coverage-complete does not imply implementation-accepted.
