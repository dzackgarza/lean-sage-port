---
description: "Task list for the master product specification"
---

# Tasks: Master product specification

**Input**: Design documents from `specs/005-master-product-spec/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`,
`contracts/product-spec-schema.md`, `quickstart.md`

**Scope**: This feature writes the master product contract. The reconnaissance program is
owned by `specs/001-native-computation/`; the dependency-ordered implementation roadmap is
owned by `specs/004-milestones/`. This task list must not duplicate either program.

## Phase 1: Setup

- [x] T001 Confirm the master-product design documents and active feature directory in `specs/005-master-product-spec/`.

## Phase 2: Foundational validation

**Purpose**: Verify the source views used by the master document before assembling it.

- [x] T002 Run the scope-table completeness check from `specs/005-master-product-spec/quickstart.md`
  against `inventory/domains.toml` and `docs/domain-specifications.md`; repair missing section
  assignments in the owning roadmap before continuing.
- [x] T003 [P] Run the output-contract validation from
  `specs/005-master-product-spec/quickstart.md`; repair any capability record using an
  undefined exactness category.
- [x] T004 [P] Run the ownership-boundary validation from
  `specs/005-master-product-spec/quickstart.md`; record unknown catalogue ids as upstream
  gaps rather than inventing local mathematical objects.

**Checkpoint**: The master document can assemble existing scope, taxonomy, completion, and
ownership views without becoming a second capability or milestone ledger.

## Phase 3: Master product document (P1)

**Goal**: Produce `product-spec.md` as the stable product-level contract above domain specs,
capability records, and the milestone roadmap.

**Independent Test**: The schema contract and all quickstart scenarios pass against
`specs/005-master-product-spec/product-spec.md`.

- [x] T005 Create `specs/005-master-product-spec/product-spec.md` with product identity,
  fixed Sage baseline, and the complete 80-section scope table assembled from
  `inventory/domains.toml` and `docs/domain-specifications.md`.
- [x] T006 [P] Add the four output-contract categories, definitions, and representative
  examples to `specs/005-master-product-spec/product-spec.md`.
- [x] T007 [P] Add the two-tier completion condition and explicitly distinguish source
  accounting from native implementation acceptance in `specs/005-master-product-spec/product-spec.md`.
- [x] T008 [P] Add ownership boundaries and routing rules for `lean-categories`,
  `lean-cas-dsl`, Mathlib, Hex, reference engines, and this repository in
  `specs/005-master-product-spec/product-spec.md`.
- [x] T009 Add the four cross-product obligations from
  `specs/004-milestones/plan.md` and the specification hierarchy links to
  `specs/005-master-product-spec/product-spec.md`.

**Checkpoint**: The master product document is complete and references, rather than duplicates,
the reconnaissance ledger, capability records, and milestone roadmap.

## Phase 4: Validation and polish

- [x] T010 Validate `product-spec.md` against
  `specs/005-master-product-spec/contracts/product-spec-schema.md`.
- [x] T011 [P] Run all scenarios in `specs/005-master-product-spec/quickstart.md` and record
  their results in `specs/005-master-product-spec/checklists/requirements.md`.
- [x] T012 [P] Verify every link in `product-spec.md` resolves to an existing repository
  document or the named upstream owner.
- [x] T013 Update `AGENTS.md` only if the master-product document's canonical path is missing
  from the repository layout table.
- [x] T014 Run `speckit-analyze` on `spec.md`, `plan.md`, and this `tasks.md`; resolve any
  contradiction before marking the feature ready.

## Dependencies and execution order

- **Phase 1** has no dependencies.
- **Phase 2** depends on Phase 1; T003 and T004 can run in parallel with T002.
- **Phase 3** depends on Phase 2; T006–T008 can run in parallel after T005 creates the file,
  while T009 follows the assembled sections.
- **Phase 4** depends on Phase 3; T010–T013 can run in parallel, and T014 is last.

## Completion rule

This feature closes when `product-spec.md` passes its schema and quickstart checks, all links
resolve, and `speckit-analyze` reports no unresolved contradiction between this feature's
specification, plan, and tasks. Completion of reconnaissance or any CAS implementation is
tracked by `specs/001-native-computation/` and `specs/004-milestones/`, not here.
