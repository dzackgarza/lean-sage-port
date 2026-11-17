# Contract: Master product specification schema

The `product-spec.md` document produced by this feature MUST contain these sections in order.

## Required sections

| Section | Required | Content constraint |
|---|---|---|
| Product identity | Yes | Name, baseline version, one-paragraph scope statement |
| Scope table | Yes | One row per section in `inventory/domains.toml`; columns: section_id, title, disposition, milestone, status |
| Output-contract taxonomy | Yes | Exactly four categories; each with definition and ≥1 example from existing capability records |
| Completion condition | Yes | Tier 1 as an exact shell command; Tier 2 as an exact oracle specification |
| Ownership boundaries | Yes | Table with: component type, owner, example from `inventory/reuse/` |
| Cross-product obligations | Yes | The four obligations from `specs/004-milestones/plan.md` §"Cross-milestone obligations" |
| Specification hierarchy | Yes | Pointer table to all specification levels |

## Invariants

1. The scope table MUST have exactly as many rows as there are sections in `inventory/domains.toml`.
2. The output-contract taxonomy MUST NOT add categories beyond the four established in
   `docs/capability-records.md`. Any proposed addition requires a spec amendment.
3. The completion condition's Tier 1 command MUST be runnable as written (no placeholders).
4. Every ownership boundary row MUST have an example traceable to a specific declaration in
   `inventory/reuse/*.toml`.
5. `product-spec.md` MUST reference but not duplicate content from `specs/004-milestones/plan.md`
   or capability records.
