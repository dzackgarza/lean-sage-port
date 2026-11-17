# Semiring source and reuse decisions

The source revision is `c00171e47d6e68d8148d7ee10c4dd77b71a97662` (Sage 11.0.beta5). Source paths are relative to that checkout.

| Decision | Evidence and rationale | Alternative considered |
| --- | --- | --- |
| Use Lean's `Nat` for the natural-number semiring | `inventory/reuse/mathlib-core.toml:lean-core.int.bignum-arithmetic` records executable natural-number arithmetic; `src/sage/rings/semirings/non_negative_integer_semiring.py` gives a Sage facade over nonnegative integers. | A new natural-number representation has no mathematical or computational need. |
| Represent tropical finite values with a selected infinity and retained orientation | `src/sage/rings/semirings/tropical_semiring.pyx:TropicalSemiringElement` stores a finite base value or `None`, and the parent stores `use_min`. The semiring operations inspect both. | A raw numeric value loses infinity and min/max convention. |
| Require an explicit admissible base map for tropical transport | `TropicalToTropical._call_` maps finite values through target construction and maps infinity to infinity; the source doctest demonstrates integer-to-rational transport. | Inferring a map solely from source and target types does not justify preservation of order or composition. |
| Use source algorithms for tropical matrix closure and mean | `src/sage/rings/semirings/tropical_matrix.py:Matrix_tropical_dense` cites Butkovič [But2010] Algorithm 1.6.21 for closure and §1.6.1 for Karp cycle mean; source doctests cover unbounded cycles and empty matrices. | A graph shortest-path routine does not by itself provide the matrix-valued closure contract or cycle-mean result. |
| State exact cycle means over rational bases | Sage checks a base subring of `RR` and divides by positive path lengths; exact rational inputs allow exact comparisons. | Floating point inputs need a precision/error contract that the current exact capability does not supply. |
| Place missing semantics at their owner | `inventory/capabilities/semirings.toml` records catalogue ids for natural and basic semiring operations; order, transport, closure and mean list no current id. `AGENTS.md` assigns mathematical semantics and catalogue ids upstream. | Local ids or new semantics would create a competing authority. |

Reuse status and exact selectors remain in `inventory/capabilities/semirings.toml` and `inventory/reuse/*.toml`. Source doctests are selected by those records. This file records choices, not another coverage count.
