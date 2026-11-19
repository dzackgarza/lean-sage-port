# Contributions

Read the [constitution](.specify/memory/constitution.md), [AGENTS.md](AGENTS.md), the owning
Spec Kit specification and the relevant [capability records](docs/capability-records.md).

| Policy | Required contribution | Example |
| --- | --- | --- |
| SEM001 | Use the upstream mathematical object and operation. | A fast residue representation interprets into the existing quotient; it does not define a second quotient ontology. |
| REUSE001 | Inspect the implementation before classifying reuse. | A package-name search is insufficient; cite its declaration, domain, revision and execution evidence. |
| INV001 | Account only for source entities that the contract covers. | A scalar quadrature record cannot select a vector-valued integration operation. |
| INV002 | The denominator is the whole source, not the reference manual. | An exclusion of "modules outside the documented manual sections" removes source by placement => read each such module and record its entities under the capability or exclusion reason that its source supports. |
| INV003 | Close an entity only by recorded reading of its module. | A `sage.combinat.*:*` selector and a batch that names `sage.combinat` report the package closed => a source-reconciled batch names each module that was read, and the ledger closes only those modules. |
| DEP001 | Distinguish alternative algorithms from mandatory inputs. | A primality algorithm using factorization does not make factorization a prerequisite for trial-division primality. |
| TEST001 | Reuse Sage source tests and compare same-input oracle computations. | Link the selected doctests and compare subgroup membership, rather than require identical printed generators. |
| TEST002 | Test the entire mathematical output through public operations. | Compare a computed integer kernel as a lattice, not merely verify that each returned vector is killed. |
| EVID001 | Record the environment that actually ran. | Sage 10.10.beta8 oracle output is evidence from that version, not from the indexed 11.0.beta5 source. |
| LOOP001 | Get feedback locally in seconds. | Push a probe and wait ten minutes for CI to report a wrong argument order => read the upstream signature, run `just check-lean <file>`, then `just test`, and push code that already passed. |
| LOOP002 | Repair a slow loop at its cause. | Patch one failure and keep a ten-minute check => add the cache, shared environment or incremental target that makes every later check fast. |
| SPEC001 | Finish specification and architecture decisions before deriving implementation issues. | An unresolved kernel-selection interface stays open in its contract rather than becoming an implementer's hidden design task. |

Use `just check-lean <file>` while editing and `just test` before each commit. CI repeats `just test`.
Preserve the committed dependency locks and source provenance. Changes to mathematical behavior
need the corresponding source-oracle acceptance; documentation changes need semantic and diff review.
