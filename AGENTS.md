# AGENTS.md

`lean-sage-port` implements the mathematical computation of SageMath natively in Lean 4. It reuses
existing Lean implementations, formal mathematics and reference algorithms before it writes new code.

## Who owns what

| Owner | Owns |
| --- | --- |
| `dzackgarza/lean-categories` | The mathematics: categories, objects, and the abstract operations that a computation must satisfy. |
| `dzackgarza/lean-cas-dsl` | The user-facing language, its kernel, and the catalogue of stable ids (`cat.rings`, `obj.rings.integers`, `op.rings.add`). |
| this repository | Native Lean computations for the objects and operations of that catalogue. |

This repository defines no mathematical ontology of its own. A computation attaches to a catalogue
object and operation. When the catalogue lacks one, the gap is reported to its owner.

## Layout

| Path | Content |
| --- | --- |
| `inventory/sage/baseline.yaml` | The Sage checkout that defines the target, and the paths read from it. |
| `inventory/sage/index/` | Generated index of that checkout: modules, entities, manual sections, packages, imports. |
| `inventory/capabilities/` | Capability records: one intrinsic mathematical operation each, with the Sage entities it accounts for. |
| `inventory/reuse/` | Reuse maps: existing Lean components, with declarations, paths and a reuse status. |
| `inventory/references/` | Non-Lean reference engines (FLINT, PARI, GAP, Singular and others) and their licences. |
| `tools/inventory/` | The `sage-inventory` command: builds the index and measures coverage. |
| `Probes/` | Executable Lean probes that test architectural decisions. |

## Existing inventories in `dzackgarza/research`

The research repository (`~/research` on the workstation) already holds curated tables of Sage
functionality. Read them before you write a record for the same subject. Take their judgments and
caveats, keyed by class, axiom or method name. This repository's index stays the list of what exists
at the baseline, because those tables read older Sage versions.

| Path in `research` | Content | Sage version read |
| --- | --- | --- |
| `docs/sage-inventory/` | Sage's category framework: each category class with its role (public, framework helper, wrapper constructor, test-only, example-only), the axiom registry with the meaning of each axiom, the functorial constructions, and the classes generated at run time. | 10.9 source, 10.10.beta0 run time |
| `writing/data/sage-source-audit-10.9/`, `writing/data/sage-runtime-10.10.beta0/` | The same data as CSV and JSON. | 10.9, 10.10.beta0 |
| `references/lattice-engines/method-inventories/` | Method lists for lattices and quadratic forms in Sage, Oscar and Hecke, GAP, PARI/GP, NTL, FLINT, fpylll, g6k and flatter, with the convention that each method uses. `lattice_wrapper_capability_checklist.md` groups the methods of all engines into capabilities. `method_ground_truth_tracker.csv` gives the source and test of each method. | per file |
| `references/lattice-engines/system-references/` | Reference notes for each engine, with the definiteness and discriminant conventions. | per file |

The wiki of `research` is retired. Each wiki page names the file under `docs/` that replaced it.

## Rules

### Lean compiles in CI, not on this machine

Do not run `lake build`, `lake exe cache get` or `just test-ci` on the workstation. The Hex packages
and their dependency TauCeti have no prebuilt cache: a build that imports them compiles thousands
of modules from source. Mathlib alone adds about 7 GB of build products.

- To check Lean code, commit and push. The `CI` workflow runs `just test-ci`. Read the result with
  `gh run watch` or `gh run view --log-failed`.
- Import the smallest Hex library that holds the declaration (`import HexDeterminant`), never the
  aggregate `import Hex`. The aggregate pulls every `*Theory` library and TauCeti.
- `just test` is the local gate. It compiles no Lean.

### Every dependency tracks its newest version

Lean, Mathlib (`master`), Hex (`main`), the CI actions and the Python tools carry no pin to an older
version. `lake-manifest.json` and `uv.lock` are not committed. When two newest versions do not build
together, record the failure in an issue and report it to the owner; do not move this repository to
an older version.

In `lakefile.toml`, Mathlib is the last `[[require]]`. Lake gives the last requirement precedence
for shared dependencies, and Mathlib's build cache is valid only for Mathlib's own versions of them.

### The Sage baseline is the local checkout

The target is the checkout named in `inventory/sage/baseline.yaml`. Do not clone, fetch or modify
Sage. The index refuses a checkout with uncommitted source changes.

### Tests assert mathematics

A test states a true mathematical fact about a public operation and checks it against an
independent oracle: a theorem, a second computation, or a published example. Inputs arrive at run
time. A hard-coded special case is not evidence for a generic operation.

## Commands

| Task | Command |
| --- | --- |
| Local gate | `just test` |
| Rebuild the Sage index | `cd tools/inventory && uv run sage-inventory index ../../inventory/sage/baseline.yaml ../../inventory/sage/index` |
| Print the record schema | `cd tools/inventory && uv run sage-inventory schema` |
| Measure coverage | `cd tools/inventory && uv run sage-inventory coverage --help` |
