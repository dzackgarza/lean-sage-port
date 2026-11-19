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
| `**Entity count**` | Yes | Indexed entities of the milestone's manual sections at the baseline, from `inventory/reconnaissance.json` |
| `**Acceptance — coverage**` | Yes | The parts for which the `remaining` command form of "Coverage gate" in `plan.md` must print nothing |
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
2. Every section id listed under `**Sections**` MUST appear in `inventory/domains.toml`. A
   section with a non-mathematical disposition appears only in M0 or M14.
3. Split predicates MUST be module-name patterns that partition the section's modules, so the
   side of every entity follows from its module.
4. `**Acceptance — coverage**` MUST name the sections for which the one `remaining` command form
   of "Coverage gate" in `plan.md` must print nothing.
