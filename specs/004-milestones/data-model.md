# Data model: Dependency-ordered milestone roadmap

## Entities

### Milestone

A named, numbered grouping of Sage manual sections that can be accepted independently.

| Field | Type | Constraint |
|---|---|---|
| `id` | string | `M0`–`M14`; stable; unique |
| `title` | string | Human-readable name |
| `sections` | list of section-id | Each id from `inventory/domains.toml`; no section appears in two milestones without a split predicate |
| `section_splits` | map section-id → predicate | Present only for `polynomial_rings`; predicate is a list of module-name patterns that partitions the section's modules |
| `prerequisites` | list of milestone-id | Directed edges in the DAG; acyclic |
| `capability_files` | list of path | Existing `inventory/capabilities/*.toml` files that cover this milestone's sections |
| `reuse_files` | list of path | `inventory/reuse/*.toml` files providing evidence for this milestone |
| `acceptance_coverage` | string | The `sage-inventory remaining` invocations ("Coverage gate" in `plan.md`) that must print nothing |
| `acceptance_implementation` | string | The oracle comparison condition that closes the milestone |
| `entity_count` | int | Indexed entities, public and underscore, of the milestone's manual sections at the baseline, summed from `inventory/reconnaissance.json` |

**Validation rules**:
- `prerequisites` entries must all be milestone ids with smaller numbers (enforces no forward edges in numbering, though the acyclicity check is the normative rule)
- Every section in `sections` must appear in `inventory/domains.toml`. A section with a non-mathematical disposition appears only in M0 (reconnaissance) or in M14 (its mathematical content only)
- Every `section_splits` pattern must match at least one module of the section, and every module of the section must fall on exactly one side of the split

### SectionAssignment

The authoritative mapping from a Sage manual section to its milestone. Stored in
`docs/domain-specifications.md` as the Milestone column.

| Field | Type | Constraint |
|---|---|---|
| `section_id` | string | Key from `inventory/domains.toml` |
| `milestone_id` | string | Reference to Milestone.id |
| `split_predicate` | string | Null unless section is split; must match Milestone.section_splits |

### PrerequisiteEdge

A directed edge in the milestone DAG.

| Field | Type | Constraint |
|---|---|---|
| `from_milestone` | string | Milestone.id of the prerequisite |
| `to_milestone` | string | Milestone.id that depends on it |
| `justification` | string | At least one capability.id from `to_milestone` whose `depends_on` contains a capability from `from_milestone` |

**Validation**: The graph formed by all PrerequisiteEdges must be a DAG. A topological sort
must succeed. This is verified by the `acceptance_dag_acyclic` task in `tasks.md`.

### AcceptanceCondition

A machine-checkable criterion attached to a milestone.

| Field | Type | Values |
|---|---|---|
| `milestone_id` | string | Reference to Milestone.id |
| `kind` | enum | `coverage` or `implementation` |
| `command` | string | Exact shell command to run |
| `expected_output` | string | For `coverage`: empty string. For `implementation`: "all oracle comparisons pass" |

## State transitions

A milestone moves through these states:

```
not-started
  → in-progress-coverage  (capability records being written)
  → coverage-complete     (sage-inventory remaining prints nothing for all sections, and the milestone's modules outside the manual have no open entity)
  → in-progress-impl      (native Lean computations being written)
  → accepted              (all oracle comparisons pass AND coverage-complete)
```

A milestone in `coverage-complete` unblocks the next milestone to enter `in-progress-coverage`.
A milestone in `accepted` unblocks the next milestone to enter `in-progress-impl`.
