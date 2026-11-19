# Mathematical requirements review: Euclidean arithmetic

Check the quality of the requirements, not implementation status.

- [ ] CHK001 Do the domain hypotheses guarantee executable quotient/remainder and decidable termination for each claimed coefficient domain? [Completeness, spec.md FR-001]
- [ ] CHK002 Does the division contract distinguish the generic Euclidean decrease law from Sage's signed integer remainder rule? [Clarity, spec.md US1]
- [ ] CHK003 Is division by zero specified at the public boundary despite Mathlib's internal zero convention? [Edge case, contracts/euclidean-operations.md]
- [ ] CHK004 Does each normalized gcd/lcm result state a selected associate convention, including rational and polynomial specializations? [Completeness, spec.md FR-004–005]
- [ ] CHK005 Are empty/singleton list and `(0,0)` outcomes stated without contradicting the source's normalization conventions? [Consistency, spec.md US2–3]
- [ ] CHK006 Does xgcd acceptance require Bézout identity while allowing nonunique coefficients? [Correctness, spec.md FR-006]
- [ ] CHK007 Does every dependency edge identify an operation consumed by the downstream algorithm rather than an equality used only in acceptance? [Dependency, plan.md]
- [ ] CHK008 Are Mathlib, Lean core and Hex reuse claims tied to actual declarations, executable domains and release status? [Traceability, research.md]
- [ ] CHK009 Are missing catalogue and normalization contracts assigned to their upstream owner before the feature is called implementation-ready? [Ownership, spec.md]
