import Mathlib
import HexDeterminant

/-! The newest Lean, Mathlib and Hex in one environment: a Mathlib theorem and a Hex computation. -/

example : (2 : ZMod 7) * 4 = 1 := by decide

open Hex in
#eval (#m[2, 1, 1; 1, 2, 1; 1, 1, 2] : Matrix Int 3 3).det
