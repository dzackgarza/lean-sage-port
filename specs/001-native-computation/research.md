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
- Official Sage `11.0.beta5` is tag object `cdddc7264af0690649227620b9a0d8af66b11237`
  pointing to commit `36e49d91b0568f07ad4373362c15ce8970587e67`. The existing index
  scanned fork commit `c00171e47d6e68d8148d7ee10c4dd77b71a97662`. Tree and file
  comparison in `inventory/sage/release.toml` establishes equivalence of the indexed
  Python/Cython files, manual and package metadata, so the index can be reused for the
  release target without changing its recorded revision. The broader source tree differs
  in one C++ header and two Meson files; runtime equivalence is not established.

Primality has a complete trial-division route independent of full integer factorization
(`Mathlib/Data/Nat/Prime/Defs.lean`, `Nat.minFac`). Factorization can therefore consume primality
without a mandatory cycle. Pocklington and ECPP have additional algorithm-specific inputs;
their use of factorization does not make factorization a prerequisite for every primality route.
