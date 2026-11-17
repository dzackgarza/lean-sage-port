import HexPoly.Instances
import HexMatrix.Basic
import Mathlib.Data.ZMod.Basic

/-! The same Hex polynomial and matrix computation over distinct coefficient rings. -/

namespace Probes.RuntimeGeneric

def composed {R : Type} [Zero R] [DecidableEq R] [One R] [Add R] [Mul R]
    [OfNat R 0] (a b : R) : R :=
  let q : Hex.DensePoly R := Hex.DensePoly.ofCoeffs #[a, 1, b]
  let value := Hex.DensePoly.evalImpl q b
  let matrix : Hex.Matrix R 2 2 :=
    Hex.Matrix.ofFn fun i j => if i = j then value else (1 : R)
  let product := matrix * matrix
  product[(0, 0)]

#guard composed (2 : Int) 3 == 1025
#guard composed (2 : ZMod 7) 3 == 3
#guard composed
    (Hex.DensePoly.ofCoeffs #[2] : Hex.DensePoly Int)
    (Hex.DensePoly.ofCoeffs #[0, 1]) ==
      Hex.DensePoly.ofCoeffs #[5, 4, 1, 4, 2, 0, 1]

end Probes.RuntimeGeneric
