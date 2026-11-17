# lean-sage-port Constitution

## Core Principles

### I. Native mathematical computation

The product computes the mathematical operations documented by the Sage reference baseline
through Lean implementations. External engines provide source references and test oracles.
An executable obligation is satisfied by an operation on runtime inputs with its specified
output and failure behavior. A declaration or theorem alone does not satisfy that obligation.

### II. Existing mathematical authority

Mathlib and lean-categories provide mathematical definitions and abstract obligations.
lean-cas-dsl provides the language, kernel and catalogue interface. This repository supplies
computations under those contracts. Missing semantics or catalogue entries go to their owner.
A storage representation MUST NOT become a competing definition of the mathematical object.
No parallel catalogue, registry, or stable-id scheme may be introduced here.

### III. Reuse before new algorithms

Each computational obligation MUST name the inspected Lean implementations and reference
algorithms that could supply it. Record source revisions, declarations, executability evidence,
supported domains and licences. Separate a source-level candidate from a tested reusable package.
A failed name search does not authorize a replacement implementation; it authorizes filing a gap
report with the upstream owner.

### IV. Generality and composition

Specify each operation at its intrinsic mathematical scope. Preserve coefficient domains,
defining maps, chosen generators, embeddings, precision and other selected structure needed
by later computations. Representation changes MUST preserve these data through explicit maps.
A result is not complete when its printed value is correct but subsequent operations cannot use it.
Extensions MUST use the existing mathematical and computational contracts.

### V. Acceptance from existing mathematics and computations

Use baseline Sage doctests and its test suite as the primary acceptance corpus. Compare native
results with the same-input Sage or reference-engine computations. Compare noncanonical outputs
as mathematical objects and maps, not by incidental order or display. Numerical results retain
their error and precision contracts; conditional and heuristic results retain their assumptions.
Add independent identities, published examples or certificates only for an identified comparison
gap. Formal verification is valuable evidence, but a complete proof is not a universal prerequisite.

### VI. Functional scope before optimization

Required operations and compositions determine priority and dependencies. Optimize after they
work, except when the capability itself requires a stated computational bound or a small required
case cannot complete. Construction should retain data cheaply and defer expensive queries.
A timing failure does not redefine the product or license a narrower mathematical domain.

### VII. Growth by extension

New mathematical domains and algorithms MUST integrate through the existing catalogue contracts
and the existing execution architecture. Adding a new domain MUST NOT require rebuilding or
replumbing any already-accepted capability. The architecture probe acceptance (SC-003 of
`specs/001-native-computation`) is the evidence that the extension mechanism works; each new
milestone MUST NOT introduce dependencies that violate it.

## Product scope and specification

The target is complete: every mathematical domain in the Sage 11.0.beta5 reference manual is
in scope. Implementation is partitioned into dependency-ordered milestones. "Complete" means
every public Sage entity has either an implemented native computation or a justified exclusion
(reason: `infrastructure`, `external-interface`, `presentation`, `data`, or `deprecated`) in a
capability record. The ultimate completion condition is that `sage-inventory unaccounted` returns
nothing for every mathematical section.

**Milestones** are defined in `specs/004-milestones/`. Each milestone names the Sage manual
sections in scope, its mathematical prerequisites (prior milestones whose operations it depends
on), the capability records already established, key reuse decisions from `inventory/reuse/`,
and acceptance conditions. No milestone may begin implementation until all its stated
prerequisites have passed their own acceptance. No percentage of full Sage coverage should be
inferred from completing any single milestone.

The master specification identifies the target domains through the reference-manual taxonomy.
Capability records attach intrinsic contracts to baseline entities. Source coverage measures
entity disposition and must remain distinct from native implementation acceptance.

Architecture contracts specify runtime domains, representation maps, operation selection and
language integration. Domain specifications state supported hypotheses and compositions.
Implementation specifications name reusable declarations, actual input dependencies, source
tests and the public computation that closes the work.

The readiness obligation is [issue 1](https://github.com/dzackgarza/lean-sage-port/issues/1).
GitHub issues own current work and dependency state. Repository specifications own stable contracts.
Reconnaissance completes only with full source accounting, justified reuse decisions, successful
general architectural probes, executable acceptance infrastructure and corrected independent review.
Completing reconnaissance is not a measure of CAS implementation coverage.

## Development and evidence

Use the Spec Kit sequence for substantive features: specification, clarification, design,
requirements checklist, dependency tasks and consistency analysis. Resolve questions from sources
before asking for a product decision. Independent review must challenge mathematical assumptions,
reuse claims, representation loss, dependency cycles and acceptance that can pass without the
required computation.

Keep the compatible toolchain and dependency resolution reproducible. Validate Lean in CI.
The workstation gate checks the inventory and source constraints without compiling Lean.

Tier 1 tests exercise small public operations and meaningful branches with feedback in seconds
or minutes. Higher tiers extend domain and input coverage through source tests and oracle runs.
A Tier 1 feedback loop exceeding five minutes requires repair. Preserve test and computation logs,
including revision, environment, inputs, setup and nested timing costs. For optimization, first
record measured costs and their actual multiplicative factors; retain the measured remaining cost.
Logging must expose application failures and computation context without leaking secrets.

CONTRIBUTING.md carries stable policy identifiers and concrete lessons about contributions.
Use mathematical assertions at the operation owner and public application paths for user flows.
Support additional platforms only when explicitly required. Check source licences before translation.

## Governance

The constitution governs product invariants; AGENTS.md supplies operational instructions.
`docs/constitution.md` is a human-readable summary that MUST stay consistent with this file;
this file is authoritative.

**Amendment procedure**: Any change to a Core Principle or to the Product Scope section requires
(1) a Git commit updating this file with rationale in the commit message, (2) a corresponding
update to any specification, capability record, or implementation issue that depends on the
changed text, and (3) a version bump according to the table below. Changes to Development and
Evidence or Governance sections that do not alter principles or scope are patch-level.

| Change type | Version component | Examples |
|---|---|---|
| Remove or redefine a principle; narrow the product scope | MAJOR | Dropping a mathematical domain; changing "MUST NOT" to "SHOULD NOT" |
| Add a new principle or section; materially expand an obligation | MINOR | New principle VII; milestone structure added to Scope |
| Clarify wording; fix typos; non-semantic refinements | PATCH | Rewording a rationale; correcting a link |

Review each feature against the constitution before implementation and again before acceptance.
Complexity violations MUST be justified in writing before the work begins.

**Version**: 1.1.0 | **Ratified**: 2026-11-17 | **Last Amended**: 2026-11-17
