# Source and reuse decisions for Euclidean arithmetic

The official target is Sage `11.0.beta5`; `inventory/sage/release.toml` records why the existing Python/Cython source index represents its scanned contents. Its index commit remains `c00171e47d6e68d8148d7ee10c4dd77b71a97662`.

| Decision | Source evidence | Alternative considered |
| --- | --- | --- |
| Use Mathlib's generic Euclidean definitions | `Mathlib/Algebra/EuclideanDomain/Defs.lean:68-99` defines quotient/remainder with a well-founded relation; `:180` and `:201-231` define computable generic gcd and xgcd under decidable equality. The map is `mathlib.euclidean.generic-algorithms`. | Separate Euclidean loops for every coefficient type would duplicate a generic producer. |
| Select integer quotient convention explicitly | `src/sage/rings/integer.pyx:Integer.quo_rem` states that nonzero remainder has the divisor's sign and gives `231.quo_rem(-2) = (-116,-1)`; zero divisor fails. | A raw `Int.emod` or truncating quotient cannot be assumed to have that convention. |
| Normalize gcd by domain | Mathlib's generic `EuclideanDomain.gcd` returns a non-unique associate. Sage's polynomial `gcd` docstring says field-polynomial results are monic; integer gcd is nonnegative. Rational `arith.misc:gcd` uses a distinct numerator-denominator convention. | One arbitrary associate is not the selected public answer in each domain. |
| Keep xgcd coefficients noncanonical | `src/sage/rings/integer.pyx:Integer.xgcd` and `src/sage/arith/misc.py:xgcd` both deny a minimality guarantee; the latter supplies finite-list certificates and empty/singleton source cases. | A minimal-coefficient contract would reject valid source results and impose an unsupported algorithm. |
| Reuse domain algorithms | `inventory/reuse/mathlib-core.toml` records `Nat.gcd`, `Int.gcd`, `Nat.xgcd` and generic Euclidean definitions; `inventory/reuse/hex.toml` records HexArith exact division/extended gcd and HexPoly field-polynomial divMod/gcd/xgcd. | A new local algorithm is not justified while these implementations cover the selected domains. |

The generic Euclidean result is an associate class until a unit-normal form is selected. The source selectors and test pointers remain in `inventory/capabilities/integers-and-rationals.toml`; they are not copied into this document. Missing catalogue ids for division, lcm and xgcd remain with their upstream owners.
