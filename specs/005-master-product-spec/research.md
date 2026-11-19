# Research: Master product specification

## Decision: What belongs in the master spec vs. in domain specs

**Decision**: The master spec contains: scope table (all sections with dispositions), output-
contract category definitions, completion condition, ownership boundaries, and cross-reference
to the milestone roadmap. It does not contain: capability records, reuse decisions, algorithm
choices, or per-operation acceptance examples. Those belong in domain specs.

**Rationale**: A master spec that duplicates capability content becomes stale immediately and
creates two locations that can contradict. The master spec's value is in defining the framework
— the taxonomy, the measurement schema, the ownership rules — that makes individual capability
records composable and consistent.

**Alternatives considered**: One enormous spec covering everything — rejected because
`specs/001-native-computation/spec.md` already shows this creates an unmaintainable document.
The plan brief explicitly states "A Sage-scale CAS should not have one enormous `spec.md`."

---

## Decision: Output-contract category definitions

**Decision**: Adopt the four categories already in `docs/capability-records.md` §Fields:
`exact`, `approximate` (result has an error bound), `heuristic` (result can be wrong),
`conditional` (correct under a named hypothesis such as GRH). These are already the vocabulary
used in existing capability records; the master spec formalizes them.

**Rationale**: Inventing new categories would invalidate existing capability records. The
existing vocabulary is used consistently across `integers-and-rationals.toml`,
`polynomials.toml`, `arithmetic-geometry.toml`, etc.

**Alternatives considered**: Adding a fifth category `certified` for results with a formal
Lean proof — rejected because this conflates the execution guarantee (what the computation
returns) with the verification method (how we know it's correct). A `certified` exact result
is still `exact`; certification is an attribute of the reuse status, not the output contract.

---

## Decision: Completion condition

**Decision**: The product is complete when:
1. `sage-inventory remaining` prints nothing for every manual section in
   `inventory/domains.toml` and every package outside the manual, AND
2. Every entity that has a capability selector passes same-input oracle comparison
   against the Sage image in `docs/oracles.md`.

These are the same two tiers defined in `specs/004-milestones/plan.md`. The master spec
references them, it does not redefine them.

**Rationale**: A single definition of "done" in one place prevents drift. The milestone
roadmap owns the per-milestone acceptance; the master spec owns the global completion.

---

## Decision: Ownership boundary specificity

**Decision**: The ownership boundary in the master spec is stated at the level of:
- Object/operation *identities* → `lean-categories` (the catalogue)
- Language/kernel *protocols* → `lean-cas-dsl`
- Executable *algorithm implementations* → Hex (released) for included components;
  this repository for native computations not in Hex
- Mathematical *proofs* (noncomputable) → Mathlib

This is more specific than the AGENTS.md table, which says only "who owns what" at a coarse
level. The master spec names the specific contract type that determines ownership.

**Alternatives considered**: Ownership by repository name only (as in AGENTS.md) — rejected
because it doesn't answer the question "where does this specific thing go?" for a new
capability. A new matrix operation's mathematical type goes to `lean-categories`, its proof
goes to Mathlib, its algorithm goes to Hex or here, and its language contract goes to
`lean-cas-dsl`.

---

## Decision: Scope table format

**Decision**: The scope table is a copy of `inventory/domains.toml`'s section list with:
- `section_id` — the Sage section identifier
- `disposition` — from `inventory/domains.toml`
- `milestone` — from `docs/domain-specifications.md`
- `status` — `in-scope` for every section

This is derivable from existing files; the master spec does not introduce new data, it
assembles existing data into a single readable location. The source of truth remains
`inventory/domains.toml` and `docs/domain-specifications.md`.

**Rationale**: Duplicating the data would create inconsistency. The master spec's scope table
is a view, not an authoritative source. Changes to scope go to `inventory/domains.toml`.
