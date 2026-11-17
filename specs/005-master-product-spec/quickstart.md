# Quickstart validation guide: Master product specification

## Prerequisites

- `uv` installed; `tools/inventory/uv.lock` resolved
- Working directory: repository root

## Scenario 1 — Verify the scope table is complete

Every section in `inventory/domains.toml` must appear in `docs/domain-specifications.md`.

```sh
python3 -c "
import tomllib, re
with open('inventory/domains.toml', 'rb') as f:
    domains = tomllib.load(f)
with open('docs/domain-specifications.md') as f:
    table = f.read()
all_sections = [s['id'] for s in domains['section']]
missing = [sid for sid in all_sections if sid not in table]
print('Missing from domain-specifications:', missing if missing else 'none')
"
```

**Expected**: `Missing from domain-specifications: none`

## Scenario 2 — Verify output-contract categories are consistent

Every `exactness` value in every capability file must be one of the four defined categories.

```sh
python3 -c "
import pathlib, tomllib
valid = {'exact', 'approximate', 'heuristic', 'conditional'}
bad = []
for p in pathlib.Path('inventory/capabilities').glob('*.toml'):
    with open(p, 'rb') as f:
        data = tomllib.load(f)
    for cap in data.get('capability', []):
        ex = cap.get('exactness', '')
        if ex and ex not in valid:
            bad.append((p.name, cap.get('id','?'), ex))
if bad:
    for b in bad: print('Invalid exactness:', b)
else:
    print('All exactness values valid.')
"
```

**Expected**: `All exactness values valid.`

## Scenario 3 — Verify the completion condition is reachable from the current baseline

Run the coverage check to confirm the measurement schema works:

```sh
cd tools/inventory
uv run sage-inventory coverage \
  ../../inventory/sage/index \
  ../../inventory/capabilities \
  ../../inventory/reuse \
  ../../inventory/coverage.json
echo "Coverage report updated: inventory/coverage.json"
```

**Expected**: Exit 0. The `coverage.json` unaccounted count is the distance to completion tier 1.

## Scenario 4 — Verify no capability record introduces a new mathematical object

A capability record must not define a new mathematical object (class, structure, or axiom)
that is not already in `lean-categories`. Check that every `catalogue` field references an
existing catalogue component:

```sh
python3 -c "
import pathlib, tomllib, re
# Load all known catalogue ids from the lean-categories reuse map
with open('inventory/reuse/lean-categories.toml', 'rb') as f:
    cats = tomllib.load(f)
known = {c['id'] for c in cats.get('component', [])}
unknown = []
for p in pathlib.Path('inventory/capabilities').glob('*.toml'):
    with open(p, 'rb') as f:
        data = tomllib.load(f)
    for cap in data.get('capability', []):
        for cid in cap.get('catalogue', []):
            # strip 'catalogue.' prefix if present
            cid_full = 'catalogue.' + cid if not cid.startswith('catalogue.') else cid
            if cid_full not in known:
                unknown.append((p.name, cap.get('id','?'), cid))
if unknown:
    print('Unknown catalogue ids (gaps to report to lean-categories):')
    for u in unknown: print(' ', u)
else:
    print('All catalogue ids are known.')
"
```

**Expected**: May list gaps (these are known open items), but should not list ids that are
*invented* by capability records (e.g., `cat.my_new_thing`).
