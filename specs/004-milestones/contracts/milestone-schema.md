# Contract: Milestone record schema

Each milestone in `specs/004-milestones/plan.md` MUST contain these fields in order.
This contract is the normative definition; the plan.md records are instances.

## Required fields

| Field | Required | Constraint |
|---|---|---|
| `### Mx — Title` | Yes | Heading with milestone id and human title |
| `**Sections**` | Yes | Comma-separated section ids from `inventory/domains.toml`; note splits |
| `**Prerequisites**` | Yes | Comma-separated milestone ids, or `None` |
| `**Capability files**` | Yes | Existing `inventory/capabilities/*.toml` files; "new file needed" for gaps |
| `**Reuse files**` | Yes | Existing `inventory/reuse/*.toml` and research paths |
| `**Entity count**` | Yes | Approximate integer from `inventory/coverage.json` |
| `**Acceptance — coverage**` | Yes | Exact `sage-inventory unaccounted` invocation |
| `**Acceptance — implementation**` | Yes | Oracle comparison description, or `N/A` for infrastructure milestones |
| `**Current state**` | For M0 only | Status note |

## Optional fields

| Field | When present |
|---|---|
| `**Open obligation**` | When a known unresolved technical debt affects this milestone |
| `**Note**` | Supplemental guidance for implementers |
| `**Licence constraint**` | When a GPL or other licence review is required |

## Invariants

1. The prerequisite field for milestone Mx MUST NOT list any milestone My where `y > x`
   (prerequisite numbering must be strictly smaller — this is a consequence of the DAG
   requirement, not a definition of it).
2. Every section id listed under `**Sections**` MUST appear in `inventory/domains.toml`
   with `disposition = "mathematical"`.
3. Split predicates MUST name an entity subset that can be verified by
   `sage-inventory unaccounted` output inspection.
4. `**Acceptance — coverage**` MUST be a runnable shell command, not a description.
