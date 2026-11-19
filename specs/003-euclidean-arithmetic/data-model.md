# Retained mathematical data

| Object | Required data | Validity |
| --- | --- | --- |
| Euclidean domain | Existing mathematical ring, executable quotient/remainder and well-founded decrease relation. | `b ≠ 0` for public division; equality must be decidable for generic gcd/xgcd recursion. |
| Associate normal form | A domain-selected representative of each associate class and the unit that transports a raw gcd to it. | Nonnegative for integers, monic for nonzero field polynomials; zero stays zero. Rational gcd/lcm uses its source-specific numerator-denominator rule. |
| Division result | `q,r` in the same domain as `a,b`. | `a=qb+r`; remainder zero or smaller than divisor by the chosen Euclidean measure. |
| Gcd/lcm result | Values in the input domain and its selected associate convention. | Divisor/greatestness and common-multiple/leastness laws. |
| Bézout certificate | Gcd and a coefficient for each input, all in the same domain. | Their linear combination equals the result; coefficients are not unique. |

No new mathematical type is prescribed. These are the data and invariants an executable realization must retain under the upstream semantics.
