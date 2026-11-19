# Quickstart validation guide: Dependency-ordered milestone roadmap

## Prerequisites

- `uv` installed and `tools/inventory/uv.lock` resolved
- Working directory: repository root

## Scenario 1 — Verify a milestone's section coverage

Checks that every public entity in the sections of a given milestone has a capability record
or justified exclusion. This is the coverage acceptance condition.

```sh
# Example: check M1 sections
cd tools/inventory

uv run sage-inventory unaccounted \
  ../../inventory/sage/index \
  ../../inventory/capabilities \
  rings_standard

uv run sage-inventory unaccounted \
  ../../inventory/sage/index \
  ../../inventory/capabilities \
  finite_rings
```

**Expected output**: Empty (no lines printed) when the milestone's coverage acceptance
condition is met. Any printed lines are entity qualified names that still need a capability
selector or exclusion entry.

## Scenario 2 — Verify the full coverage report

```sh
cd tools/inventory
uv run sage-inventory coverage \
  ../../inventory/sage/index \
  ../../inventory/capabilities \
  ../../inventory/reuse \
  ../../inventory/coverage.json
```

**Expected output**: Exit 0. Reports entity counts per section. Fails on duplicate capability
ids, unknown `depends_on` or `generalizes` ids, unknown reuse component ids, unknown catalogue
ids, or selectors that match no entity.

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

# The capability evidence ledger must show that every polynomial selector resolves
# to public source entities and that the M2/M3 selectors do not rely on an
# unaccounted wildcard remainder.
uv run sage-inventory unaccounted \
  ../../inventory/sage/index \
  ../../inventory/capabilities \
  polynomial_rings \
  | grep "multi_polynomial\|polynomial_ideal\|polynomial_ring_homo" || true
# The command is empty after coverage is complete; the evidence ledger is the
# entity-level audit for the M2/M3 split.
```
