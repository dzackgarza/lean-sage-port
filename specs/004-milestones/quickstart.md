# Quickstart validation guide: Dependency-ordered milestone roadmap

## Prerequisites

- `uv` installed and `tools/inventory/uv.lock` resolved
- Working directory: repository root

## Scenario 1 — Verify a milestone's section coverage

Checks that every entity, public and underscore, in the sections of a given milestone is
`reconciled`, `excluded` or `category-record`. This is the coverage acceptance condition.

```sh
# Example: check M1 sections
cd tools/inventory

uv run sage-inventory remaining \
  ../../inventory/sage/index \
  ../../inventory/capabilities \
  ../../inventory/categories/sage-categories.toml \
  ../../inventory/reconnaissance-worklog.toml \
  rings_standard

uv run sage-inventory remaining \
  ../../inventory/sage/index \
  ../../inventory/capabilities \
  ../../inventory/categories/sage-categories.toml \
  ../../inventory/reconnaissance-worklog.toml \
  finite_rings
```

**Expected output**: Empty (no lines printed) when the milestone's coverage acceptance
condition is met. Each printed line is `id<TAB>state<TAB>kind<TAB>doctests` for an entity
that is still `unaccounted` (no record selects it) or `scoped` (no source-reconciled worklog
batch names its module).

The modules outside the manual that belong to the milestone ("Coverage gate" in `plan.md`)
are checked in the module ledger:

```sh
jq -r '.module_rows[] | select(.manual == false and (.unaccounted + .scoped) > 0)
  | select(.imported_by_sections | index("rings_standard") or index("finite_rings"))
  | .module' ../../inventory/reconnaissance.json
```

## Scenario 2 — Verify the full coverage report

```sh
cd tools/inventory
uv run sage-inventory coverage \
  ../../inventory/sage/index \
  ../../inventory/capabilities \
  ../../inventory/reuse \
  ../../inventory/categories/sage-categories.toml \
  ../../inventory/reconnaissance-worklog.toml \
  ../../inventory/coverage.json
```

**Expected output**: Exit 0. Reports state counts per manual section and per package outside
the manual. Fails on duplicate capability ids, unknown `depends_on` or `generalizes` ids,
unknown reuse component ids, unknown catalogue ids, selectors that match no entity, and a worklog
whose commit differs from the index or whose source-reconciled batch names anything other than
an indexed module.

## Scenario 3 — Verify the prerequisite DAG is acyclic

The milestone spec's prerequisite edges must form a DAG. Verify by checking that the
dependency order in `specs/004-milestones/plan.md` can be topologically sorted:

```sh
# The plan.md records each milestone's prerequisites. Manual check:
# M0 → M1 → M2 → M3 → M10
#                M2 → M12
#           M1 → M4 → M5 → (M9)
#                M4 → M6 → M8 → M13
#           M1 → M7 → M11
#      M14 follows M0–M3
# No back-edges exist in this ordering.
```

Automated verification is part of the acceptance suite defined in `tasks.md` (T005).

## Scenario 4 — Verify section-to-milestone assignment in domain-specifications.md

```sh
# Every section in inventory/domains.toml with disposition=mathematical must have
# a Milestone column entry in docs/domain-specifications.md.
python3 -c "
import tomllib, re

with open('inventory/domains.toml', 'rb') as f:
    domains = tomllib.load(f)

with open('docs/domain-specifications.md') as f:
    table = f.read()

math_sections = [s['id'] for s in domains['section']
                 if s.get('disposition') == 'mathematical']
missing = []
for sid in math_sections:
    if not re.search(rf'\b{sid}\b.*M\d+', table):
        missing.append(sid)

if missing:
    print('Missing milestone assignment:', missing)
else:
    print('All mathematical sections have milestone assignments.')
"
```

**Expected output**: `All mathematical sections have milestone assignments.`

## Scenario 5 — Verify the polynomial_rings split

```sh
cd tools/inventory

# List the modules of polynomial_rings that still hold open entities. Assign each to M2 or M3
# with the split predicate in plan.md (M3 entry); the predicate partitions the section.
uv run sage-inventory remaining \
  ../../inventory/sage/index \
  ../../inventory/capabilities \
  ../../inventory/categories/sage-categories.toml \
  ../../inventory/reconnaissance-worklog.toml \
  polynomial_rings \
  | cut -f1 | cut -d: -f1 | sort -u
```

**Expected output**: M2 coverage holds when every listed module matches the M3 predicate. M3
coverage holds when the list is empty.
