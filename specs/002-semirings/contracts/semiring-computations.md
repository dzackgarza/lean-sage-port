# Public mathematical contracts

The signatures below name intrinsic inputs and outputs, not a new Lean ontology. The implementation uses the owner-supplied semantics and catalogue operations.

| Capability id | Input | Output and failure |
| --- | --- | --- |
| `semirings.natural-numbers` | `a,b,n : Nat` | `a+b`, `a*b`, `a^n` in the existing natural-number semiring; selected additive semigroup generator family `(0,1)`. |
| `semirings.tropical-construction` | Ordered additive commutative group `R`, decidable order, orientation, finite values or selected infinity | Tropical semiring with `min/max` addition, base addition multiplication, additive zero infinity, multiplicative one base zero; finite inverse, and an explicit failure on division by infinity. |
| `semirings.tropical-multiplicative-order` | Tropical element | `1` for tropical one, infinity otherwise. |
| `semirings.tropical-base-change` | Same-orientation tropical semirings and order-preserving additive map `f : R → S` | Semiring map with explicit source/target, finite action `r ↦ f(r)`, infinity action `∞ ↦ ∞`, composable with another such map. |
| `semirings.tropical-matrix-closure` | Square tropical matrix `A` | Weak `A ⊕ A² ⊕ …` or strong `I ⊕ A ⊕ A² ⊕ …` matrix over the same semiring and indices; source-defined error for an unbounded improving cycle. |
| `semirings.tropical-cycle-mean` | Square tropical matrix over an exact rational base | Minimum mean for min-plus and maximum mean for max-plus among finite directed cycles, or tropical infinity when no finite cycle exists; nonsquare input fails. |

The source selectors in `inventory/capabilities/semirings.toml` select the baseline doctests and precise source lines. `matrices.arithmetic` supplies generic semiring matrix operations to both matrix computations. Native results must be usable as inputs to later public operations, with no external CAS runtime dependency.
