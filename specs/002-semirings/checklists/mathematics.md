# Mathematical requirements review: Semiring computations

Review the English contracts, not implementation status. A checked item means the reviewer judged the requirement sufficient.

- [ ] CHK001 Are the base hypotheses sufficient for each min-plus and max-plus operation, including order decidability, inverses and power exponents? [Completeness, spec.md FR-002–003]
- [ ] CHK002 Does the specification distinguish the selected infinity from a finite base value and state its additive and multiplicative laws? [Clarity, spec.md US2]
- [ ] CHK003 Is tropical transport restricted to base maps that preserve the selected orientation and semiring laws, with explicit source and target? [Correctness, spec.md FR-005]
- [ ] CHK004 Does closure specify weak versus strong sums and the exact condition that makes a matrix entry unbounded? [Clarity, contracts/semiring-computations.md]
- [ ] CHK005 Does cycle mean define the extremum for each orientation and the no-cycle result without relying on a source label alone? [Clarity, spec.md FR-007]
- [ ] CHK006 Do the acceptance rules compare retained mathematical structure and specified failures, including noncanonical morphism representations? [Coverage, spec.md FR-009]
- [ ] CHK007 Does each prerequisite supply an actual input or operation consumed by the dependent computation? [Dependency, plan.md]
- [ ] CHK008 Are missing catalogue operations routed to their mathematical owner without creating local semantics? [Ownership, plan.md]
- [ ] CHK009 Do source selectors and cited algorithm references support the stated domains and exactness? [Traceability, research.md]
