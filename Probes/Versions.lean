import Mathlib
import HexDeterminant
import HexMatrix.Notation

/-! A Hex release with its own Lean and Mathlib in one environment: a Mathlib theorem and a Hex
computation. -/

example : (2 : ZMod 7) * 4 = 1 := by decide

#guard (#m[2, 1, 1; 1, 2, 1; 1, 1, 2] : Hex.Matrix Int 3 3).det == 4
