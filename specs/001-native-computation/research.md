# Architectural sources and resolved choices

The reusable evidence is maintained in `inventory/reuse/`, `inventory/references/` and
`docs/architecture.md`; these files own revisions and declaration paths.

- Native algorithms form a Lean library consumed on the formal side. The DSL external-leaf
  restrictions do not prohibit this library. The operation-selection hook still needs concrete
  source-level resolution before DSL integration is specified as ready.
- Hex supplies executable polynomial, matrix and prime-field quotient representations. Reuse
  these for the runtime experiments rather than construct a parallel arithmetic hierarchy.
- Sage's selected source doctests and reference computations determine acceptance. Noncanonical
  results require mathematical comparison; optional formal correspondence proofs strengthen
  evidence but do not universally gate acceptance.
- Runtime quotient parameters must carry checked coefficient-domain and polynomial hypotheses.
  Invalid input must fail explicitly. Reducible polynomials define quotient rings, not fields.
- The existing source index is a development snapshot. Release-baseline reconciliation remains
  an explicit source-provenance obligation rather than a silent change to recorded references.

The current capability dependency declarations contain a cycle between primality proving and
integer factorization. Some algorithm families use each other, but that does not establish a
mandatory implementation dependency in both directions. Resolve the algorithm-specific inputs
from sources before deriving the implementation DAG.
