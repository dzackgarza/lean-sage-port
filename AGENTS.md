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
| `.specify/memory/constitution.md` | The constitution: product scope, principles and amendment procedure. `docs/constitution.md` points to it. |
| `docs/milestones.md` | Pointer to `specs/004-milestones/plan.md`, the authoritative milestone roadmap. |
| `specs/004-milestones/` | Spec Kit feature for the milestone roadmap: spec, research, data model, plan, tasks. |
| `docs/architecture.md` | Source-checked architecture candidate; describes the native dispatch interface and composition mechanism. |
| `docs/capability-records.md` | Rules and schema for capability records. |
| `docs/domain-specifications.md` | Index of manual sections to their capability files. |
| `docs/oracles.md` | Sage oracle image identity and query instructions. |
| `inventory/sage/baseline.yaml` | The checkout and source paths used to build the current index. |
| `inventory/sage/release.toml` | Official release identity and the indexed fork content comparison. |
| `inventory/sage/index/` | Generated index of that checkout: modules, entities, manual sections, packages, imports. |
| `inventory/capabilities/` | Capability records: one intrinsic mathematical operation each, with the Sage entities it accounts for. `docs/capability-records.md` has the rules. |
| `inventory/reconnaissance-worklog.toml` | Source-reading batches. A source-reconciled batch names the modules that were read; only those modules can close entities. |
| `inventory/coverage.json` | Generated coverage report: every indexed entity by reconnaissance state, per manual section and per package outside the manual. |
| `inventory/reconnaissance.json` | Generated module ledger: each module's part, state counts, crediting batches and, outside the manual, the importing manual sections. |
| `inventory/reconnaissance-entities.jsonl.gz` | Generated entity ledger: each indexed entity's state and selecting records. Source facts stay in the index. |
| `inventory/categories/` | Sage's category classes and their methods at the baseline, each joined to its id in the `lean-categories` catalogue. The Sage-side judgments come from the research inventories below. |
| `inventory/categories/reconciliation.json` | Open category reconciliation ledger joining every indexed category entity to an existing record, a research role, or an unmatched state. |
| `inventory/reuse/` | Reuse maps: existing Lean components, with declarations, paths and a reuse status. |
| `inventory/references/` | Non-Lean reference engines (FLINT, PARI, GAP, Singular and others) and their licences. |
| `tools/inventory/` | The `sage-inventory` command: builds the index and measures coverage. |
| `Probes/` | Executable Lean probes that test architectural decisions. |
| `specs/` | Spec Kit documents: reconnaissance master spec (`001`), and per-domain specs as milestones proceed. |
| `specs/004-milestones/plan.md` | Authoritative dependency-ordered milestone roadmap (M0–M14). |
| `specs/005-master-product-spec/product-spec.md` | Master product specification: scope table, output-contract taxonomy, completion condition, ownership boundaries. |

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

### Reproducible dependency set

`lean-toolchain` and `lakefile.toml` name the compatible Lean, Mathlib and Hex revisions.
`lake-manifest.json` locks the full Lake dependency graph; `tools/inventory/uv.lock` locks the
Python inventory environment. Commit both locks when dependencies change. CI builds this resolved
set and runs the inventory tests. Change versions only after CI establishes a compatible set.

In `lakefile.toml`, Mathlib is the last `[[require]]`. Lake gives the last requirement precedence
for shared dependencies, and Mathlib's build cache is valid only for Mathlib's own versions of them.

Hex compiles only against the Lean toolchain and the Mathlib revision of its own release. Because
the Mathlib requirement here overrides the one of Hex, Hex, Mathlib and Lean move together:

| File | Value |
| --- | --- |
| `lakefile.toml`, `hex` | a Hex release tag (`v0.10.0`) |
| `lakefile.toml`, `mathlib` | the `mathlib` `rev` in `lake-manifest.json` of that Hex tag |
| `lean-toolchain` | `lean-toolchain` of that Hex tag |

A newer Mathlib breaks the Hex theory libraries. Hex `v0.10.0` with Mathlib `master` fails with
unsolved goals in `HexPolyTheory/PolynomialEquivalence.lean` and an unknown `Matrix.ofArray` in
`HexMatrixTheory/Literal.lean`.

To relock, copy `lakefile.toml`, `lean-toolchain` and `lake-manifest.json` into a scratch directory
and run `MATHLIB_NO_CACHE_ON_UPDATE=1 lake update` there. The variable stops the Mathlib post-update
hook from downloading the build cache. Do not run `lake update` in the checkout: its
`.lake/packages` can be a link to a package directory that other projects share.

### The Sage release and local index

The target is official Sage `11.0.beta5`, identified in `inventory/sage/release.toml`.
`inventory/sage/baseline.yaml` names the local checkout that produced the existing index.
The release record proves that the indexer's Python/Cython inputs, the manual tree and package
metadata match the official release; it also names three different unindexed build/header files.
Keep the scanned fork revision in the index provenance. Do not claim whole-runtime equivalence.
Do not clone, fetch or modify Sage. The index refuses a checkout with uncommitted source changes.

### Reconnaissance covers the whole source

The task is to index all Sage functionality by reading the pinned checkout, and to produce a
ledger. The denominator is every entity of the index (66,424 at the baseline: classes,
module-level functions, `def` and `cpdef` methods, public and underscore) in all 3,041 modules.
The reference manual is generated from the source; it documents a subset (2,400 modules) and
names the domains. It never bounds the scope, and "outside the manual" is never an exclusion
reason. An entity closes only when a source-reconciled worklog batch names its module, so
wildcard selectors cannot close unread source. `docs/capability-records.md` defines the states.

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
| Write the reconnaissance ledger | `cd tools/inventory && uv run sage-inventory reconnaissance --help` |
| List the open entities of a section or package | `cd tools/inventory && uv run sage-inventory remaining ../../inventory/sage/index ../../inventory/capabilities ../../inventory/categories/sage-categories.toml ../../inventory/reconnaissance-worklog.toml <section-or-package>` |
