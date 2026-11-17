# Tasks: Master product specification

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts/product-spec-schema.md](contracts/product-spec-schema.md)

**Organization**: US1 (scope completeness), US2 (completion condition), and US3 (ownership
boundaries) can proceed in parallel after Phase 2. Each story closes when its independent
test passes.

## Phase 1: Setup

- [x] T001 Spec, research, data model, quickstart, plan, and contract written at
  `specs/005-master-product-spec/`

---

## Phase 2: Foundational

**Purpose**: Verify the input sources are consistent before writing `product-spec.md`.

- [ ] T002 Run quickstart scenario 1 (`python3` scope table completeness check). If any
  sections are missing from `docs/domain-specifications.md`, add them before proceeding.
  Record the result in this task's checklist note.
- [ ] T003 [P] Run quickstart scenario 2 (output-contract category validation). Confirm all
  existing capability records use only the four defined categories. If any use an undefined
  value, file a correction in the relevant capability file.
- [ ] T004 [P] Run quickstart scenario 4 (ownership boundary verification). Confirm every
  `catalogue` field in every capability record references a known component in
  `inventory/reuse/lean-categories.toml`. Record any unknown ids as gaps to file with
  `lean-categories`.

**Checkpoint**: All three scenarios pass before writing `product-spec.md`.

---

## Phase 3: User Story 1 — Know exactly what this product computes (P1)

**Goal**: Write the scope table (§plan.md §"Scope table") into `product-spec.md` as the
definitive statement of what is in scope, excluded, or deferred. Every section must have
a row; every in-scope section must have a milestone.

**Independent test**: Run quickstart scenario 1 against `product-spec.md` after it is
written, substituting `product-spec.md` as the target. Zero missing sections.

- [ ] T005 [US1] Create `specs/005-master-product-spec/product-spec.md` with the Product
  Identity section (name, baseline version, scope statement) and the Scope Table copied from
  `plan.md` §"Scope table".
- [ ] T006 [P] [US1] Add the Output-Contract Taxonomy section to `product-spec.md`, using
  the definitions from `plan.md` §"Output-contract taxonomy" and adding one example per
  category drawn from an existing capability record in `inventory/capabilities/`.
- [ ] T007 [US1] Add the Specification Hierarchy section to `product-spec.md` as a pointer
  table (do not duplicate content — reference only). Confirm every link in the table resolves
  to an existing file.

**Checkpoint**: `product-spec.md` sections 1–3 and 7 complete; scope table has zero missing rows.

---

## Phase 4: User Story 2 — Know what "done" means for the full product (P1)

**Goal**: Write the Completion Condition section with an exact Tier 1 shell command and an
exact Tier 2 oracle specification. Both must be runnable as written.

**Independent test**: Run quickstart scenario 3 (`sage-inventory coverage`) and confirm the
command it runs matches the Tier 1 command in `product-spec.md` word for word.

- [ ] T008 [US2] Add the Completion Condition section to `product-spec.md`. Tier 1: exact
  shell command. Tier 2: exact oracle image SHA and comparison rule. Include the "what does
  not count" list from `plan.md`.
- [ ] T009 [US2] Add the Cross-Product Obligations section to `product-spec.md` by copying
  the four rows from `specs/004-milestones/plan.md` §"Cross-milestone obligations". Do not
  paraphrase; use the same obligation text and owner assignments.

**Checkpoint**: `product-spec.md` sections 4–5 complete; Tier 1 command is runnable.

---

## Phase 5: User Story 3 — Determine the scope boundary for any mathematical operation (P2)

**Goal**: Write the Ownership Boundaries section with the decision-rule table such that any
proposed new capability can be routed to the correct owner by following the rules.

**Independent test**: Apply the decision rules to three test cases: (a) a new matrix operation
type, (b) a new primality certificate format, (c) a new language binding. Each must route
deterministically to one owner.

- [ ] T010 [US3] Add the Ownership Boundaries section to `product-spec.md`. Include the
  component-type-to-owner table from `plan.md` and the five decision rules. Add one worked
  example per rule drawn from existing capability records.
- [ ] T011 [US3] Apply the decision rules to the three test cases in the independent test above
  and record the results in `checklists/mathematical-dependencies.md` as a note.

**Checkpoint**: `product-spec.md` section 5 complete; all three test cases route deterministically.

---

## Phase 6: Polish and cross-cutting

- [ ] T012 Validate `product-spec.md` against `contracts/product-spec-schema.md`: confirm all
  seven required sections are present, the scope table has the right row count (65), no
  output-contract categories beyond the four, Tier 1 command is runnable, and all hierarchy
  links resolve.
- [ ] T013 [P] Run the full quickstart scenario suite (scenarios 1–4) with `product-spec.md`
  as the target where applicable. Document pass/fail for each.
- [ ] T014 Update `AGENTS.md` layout table to include
  `specs/005-master-product-spec/product-spec.md` as the master product specification entry.

---

## Dependencies and execution order

- **Phase 1**: T001 complete.
- **Phase 2**: T002, T003, T004 can run in parallel. All must pass before Phase 3.
- **Phase 3**: T005 first (creates the file); T006, T007 can run in parallel after T005.
- **Phase 4**: T008 and T009 can run in parallel after Phase 2 (they add to an existing file).
- **Phase 5**: T010 after Phase 2. T011 after T010.
- **Phase 6**: T012, T013, T014 can run in parallel after Phases 3–5.

## Completion rule

The master product spec feature closes when T012 validates without failures and quickstart
scenarios 1–3 pass. `product-spec.md` is then the authoritative document at the top of the
specification hierarchy.
