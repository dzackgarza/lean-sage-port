# Public mathematical contracts

| Capability | Input | Output and acceptance |
| --- | --- | --- |
| `euclidean.division` | `a,b : R`, `b ≠ 0`, executable Euclidean structure | `(q,r) : R × R` with `a=qb+r` and Euclidean decrease. Divisibility iff `r=0`; exact quotient when divisible. Integer output additionally uses Sage's divisor-sign remainder. Zero divisor fails publicly. |
| `euclidean.gcd` | `a,b : R` or finite list, executable division and selected unit normal form | Normalized gcd and lcm in `R`; gcd is a greatest common divisor, lcm a least common multiple. Empty list gcd is `0`, lcm is `1`. Polynomial gcd over a field is monic when nonzero. Rational gcd/lcm uses the source's separate reduced-fraction rule. |
| `euclidean.xgcd` | `a,b : R` or finite list, executable division and selected normalization | `(g,s,t)` or `(g,s₁,…,sₙ)` with `g=sa+tb` or `g=Σsᵢaᵢ`. The gcd follows the stated associate convention; source list empty/singleton cases have their documented outputs. No coefficient minimality claim. |

Public operations take runtime inputs in the selected coefficient domain. Mathematical equality of outputs and certificates is the acceptance criterion; a particular internal Euclidean trace or Bézout coefficient tuple is not. The source-selected doctests are in `inventory/capabilities/integers-and-rationals.toml`, with further polynomial examples at the paths in `plan.md`.
