# Feature Specification: Native mathematical computation

**Feature Branch**: `main`
**Created**: 2026-11-17
**Status**: Draft; architecture acceptance requires the executable probes.
**Scope**: All the functionality of the baseline Sage source; the reference manual names its domains.

## Current assignment boundary

The user stories below specify the intended CAS product. This assignment delivers the source
inventory, reuse decisions, architectural experiments, specifications and reproducible acceptance
infrastructure from which that product can be implemented. It does not implement every product
operation. Its acceptance is SC-001 through SC-007: the requirements and evidence must be complete
enough for later implementers to proceed under resolved contracts. Runtime probes are executed
experiments; the remaining operation tests are reused source obligations for later implementation.

## User Scenarios & Testing

### User Story 1 — Compute in a chosen mathematical domain (Priority: P1)

A researcher supplies an object, its coefficient domain and operation inputs. The system returns
a mathematically valid result with its selected structure and stated exactness.

**Independent Test**: Run the operation's existing Sage doctests and compare same-input native
and reference computations under the capability record's hypotheses.

**Acceptance Scenarios**:

1. Given a documented exact operation and supported inputs, compute a result equal to the
   reference result as a mathematical object, including defining maps when applicable.
2. Given inputs outside the operation's domain, return its specified failure rather than a
   value in a silently changed ring or weaker mathematical problem.
3. Given an approximate computation, retain the requested precision and distinguish a rigorous
   enclosure from a numerical error estimate.

### User Story 2 — Compose constructions (Priority: P1)

A researcher constructs a coefficient domain at runtime, forms polynomials or matrices over it,
and uses results in later constructions without losing the defining maps.

**Independent Test**: Execute the architectural probes on runtime data, then compare the
resulting operations and composed maps with Sage.

**Acceptance Scenarios**:

1. Construct a quotient from runtime defining data; arithmetic respects the defining relation
   and retains the quotient map.
2. Construct an algebraic extension from a runtime polynomial, preserving the coefficient
   embedding and selected generator. A field-only operation requires evidence of irreducibility.
3. Perform the same generic matrix and polynomial operations over distinct coefficient domains.
   Specialized storage must realize the same intrinsic operation.
4. Compose constructions and maps. The composed map agrees with successive application on
   runtime elements and retains its source and target.

### User Story 3 — Add a computational capability (Priority: P2)

An implementer selects an independently specified operation and can identify its semantic owner,
reusable executable code, inputs, prerequisites, source tests and public completion condition.

**Independent Test**: An independent reviewer can follow the issue's source links and reproduce
its acceptance without inventing definitions, interfaces or expected answers.

**Acceptance Scenarios**:

1. An available executable implementation is reused or its inapplicability is supported by source evidence.
2. A noncomputable mathematical result supplies semantics but leaves the computational obligation open.
3. A new operation integrates through the existing contracts and composes with existing results.
4. An implementation issue closes only after its public operation passes its mathematical acceptance.

### Edge Cases

Zero objects, empty inputs, nonfields, zero divisors, reducible defining polynomials, singular
matrices, incompatible coefficient maps, changed bases, noncanonical generators, insufficient
precision, conditional answers and exhausted heuristic searches retain explicit contracts.
Sage's existing source cases determine the concrete examples for each operation.

## Requirements

### Functional Requirements

- **FR-001**: The target includes all the functionality of the baseline Sage source: algebra,
  number theory, groups, modules, matrices, combinatorics, graphs, geometry, topology,
  homological algebra, symbolic and numerical analysis, probability, optimization, coding,
  cryptography, arithmetic geometry and specialized domains. The reference manual sections name
  these domains. The manual is generated from the source and documents a subset of it (2,400 of
  3,041 modules), so modules outside the manual are in scope and are read with the manual
  sections whose modules import them.
- **FR-002**: Every indexed entity (class, module-level function, `def` or `cpdef` method, public
  or underscore, of a `.py` or `.pyx` module under `src/sage`) has a capability mapping, a
  justified nonmathematical exclusion, or a category record, and a source-reconciled worklog batch
  records the reading of its module. A generic operation may account for multiple specializations
  with explicit hypotheses.
- **FR-003**: Each operation records mathematical inputs and outputs, retained structure,
  exactness, algorithms, prerequisites, source references, reuse decisions and acceptance sources.
- **FR-004**: Native computations consume the semantics and language contracts at their upstream
  owners. The representation layer does not introduce a separate mathematical authority.
- **FR-005**: Runtime-created domains and their maps remain usable by generic operations and
  further constructions. Architecture acceptance requires executable evidence for this behavior.
- **FR-006**: Reference engines supply test oracles independently of the native runtime.
- **FR-007**: Reuse evidence distinguishes released and development packages, formal definitions,
  executable candidates, compiled results, adaptation work and unresolved searches.
- **FR-008**: The implementation graph distinguishes semantic prerequisites already supplied
  upstream from executable computations still required. Every edge identifies a consumed input.
- **FR-009**: Domain and cross-domain specifications derive from the capability inventory.
  GitHub issues hold the dependency graph and work state; source documents hold the contracts.
- **FR-010**: Builds and oracle environments record immutable dependency identities and run
  through reproducible commands. CI validates the architectural probes and acceptance infrastructure.
- **FR-011**: A capability may be accepted through source tests and independent oracle comparisons
  without a complete Lean correctness proof. Representation comparisons must still preserve the
  mathematical object, defining maps and selected structure named in the contract.
- **FR-012**: Native algorithms are exposed as a Lean library for formal-side use. The DSL's
  external-leaf protocol does not define the native library interface. Kernel integration must
  use the existing catalogue and owner-controlled operation-selection interface.

### Key Entities

- A **capability** is an intrinsic operation with domain hypotheses and mathematical output.
- A **source entity** is an indexed Sage class, function or method at the baseline revision,
  public or underscore. Its reconnaissance state is `unaccounted`, `scoped`, `reconciled`,
  `excluded` or `category-record` (`docs/capability-records.md`).
- A **reading batch** is a worklog entry that names the modules read; only a source-reconciled
  batch lets a record close the entities of a module.
- A **reuse component** identifies upstream declarations and their supported semantics or computation.
- A **realization** relates a computational representation to an upstream mathematical object.
- An **acceptance source** is an existing test or oracle operation and its comparison rule.
- An **implementation obligation** is an owning issue with required public behavior and input dependencies.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every indexed entity of the baseline source is `reconciled`, `excluded` or
  `category-record`: `sage-inventory remaining` prints nothing for every manual section and every
  package outside the manual.
- **SC-002**: Every foundational obligation has a source-backed reuse decision and licence disposition.
- **SC-003**: All required runtime-construction and composition probes pass on runtime inputs.
- **SC-004**: Every implementation issue has sufficient source, contract, dependency and acceptance
  information for an implementer to proceed without a fresh foundations investigation.
- **SC-005**: The dependency graph is acyclic and each edge represents an actual consumed prerequisite.
- **SC-006**: The pinned environment builds in CI and the independent acceptance path executes.
- **SC-007**: Independent review leaves no unresolved foundational decision hidden in implementation work.

## Assumptions

The target release is official Sage tag `11.0.beta5` (commit
`36e49d91b0568f07ad4373362c15ce8970587e67`). The existing index truthfully records
the fork commit it scanned, `c00171e47d6e68d8148d7ee10c4dd77b71a97662`.
`inventory/sage/release.toml` establishes that all Python/Cython source files read by the
indexer, the reference-manual tree and the package tree match the official release. The
broader `src/sage` tree differs in three unindexed build/header files; no compiled-runtime
equivalence follows. Existing source records retain their scanned-commit provenance.
Current readiness and unresolved obligations are owned by
[issue 1](https://github.com/dzackgarza/lean-sage-port/issues/1).

The source index, capability records and reuse maps are reusable evidence. Their presence does
not assert completion of the inventory or success of the architecture probes.
