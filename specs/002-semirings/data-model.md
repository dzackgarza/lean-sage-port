# Retained mathematical data

| Object | Required data and relation | Validity |
| --- | --- | --- |
| Natural-number semiring | Existing `Nat` value and owner-supplied semiring structure. | No negative element. |
| Tropical semiring | Ordered additive commutative base `R`, decidable comparison, and min/max orientation. Mathlib's `MinTropical (WithTop R)` and `MaxTropical (WithBot R)` supply the arithmetic. | The runtime object retains the orientation and base; no second tropical arithmetic type is introduced. |
| Tropical element | A Mathlib tropical value over `WithTop R` or `WithBot R`, associated with its runtime parent. | Finite values may be lifted to `R`; infinity has no finite base value. |
| Tropical transport | Source and target tropical semirings, same orientation, and an order-preserving additive base map. | Maps finite values through the base map and infinity to infinity; identity and composition preserve endpoints. |
| Tropical matrix | Finite row and column index types, coefficient tropical semiring and indexed entries. | Closure and mean require square dimensions; results preserve indices and coefficient parent. |

The table describes data that the native realization must retain. Mathematical definitions and operation obligations come from Mathlib and `lean-categories`; catalogue ids come from `lean-cas-dsl`.
