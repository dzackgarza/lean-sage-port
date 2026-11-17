# Architectural sources and resolved choices

The reusable evidence is maintained in `inventory/reuse/`, `inventory/references/` and
`docs/architecture.md`; these files own revisions and declaration paths.

- Native algorithms form a Lean library consumed on the formal side. The DSL external-leaf
  restrictions do not prohibit this library. The surveyed kernel sends general values through
  `Realize.send` to external registrations; its native discharge handles propositions only.
  `docs/architecture.md` specifies the required DSL-owned native port using the existing
  `Operation`, `Wire`, elaborator and result types. That owner addition must precede DSL
  integration; native-library probes do not establish that the addition is implemented.
- Hex supplies executable polynomial, matrix and prime-field quotient representations. Reuse
  these for the runtime experiments rather than construct a parallel arithmetic hierarchy.
- Sage's selected source doctests and reference computations determine acceptance. Noncanonical
  results require mathematical comparison; optional formal correspondence proofs strengthen
  evidence but do not universally gate acceptance.
- Runtime quotient parameters must carry checked coefficient-domain and polynomial hypotheses.
  Invalid input must fail explicitly. Reducible polynomials define quotient rings, not fields.
- The existing source index is a development snapshot. Release-baseline reconciliation remains
  an explicit source-provenance obligation rather than a silent change to recorded references.

Primality has a complete trial-division route independent of full integer factorization
(`Mathlib/Data/Nat/Prime/Defs.lean`, `Nat.minFac`). Factorization can therefore consume primality
without a mandatory cycle. Pocklington and ECPP have additional algorithm-specific inputs;
their use of factorization does not make factorization a prerequisite for every primality route.
