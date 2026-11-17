import HexPolyFp.Quotient.Ring
import HexMatrix.Basic
import HexPolyFpTheory.Basic
import Mathlib.RingTheory.AdjoinRoot
import Probes.RuntimeGeneric

/-!
An architectural experiment over Hex's existing prime-field polynomial quotient.
The defining polynomial and characteristic are input values. Hex supplies the
executable quotient; the Mathlib map below identifies its intended mathematical
presentation. A correspondence between those two quotient types is still required.
-/

namespace Probes.RuntimeQuotient

open Hex

/-- Construct coefficients at a selected prime characteristic. -/
def polynomial (p : Nat) [ZMod64.Bounds p] (coeffs : Array Nat) : FpPoly p :=
  FpPoly.ofCoeffs (coeffs.map (ZMod64.ofNat p))

/-- The selected constant map into Hex's existing quotient representation. -/
def constantMap {p : Nat} [ZMod64.Bounds p] [ZMod64.PrimeModulus p]
    {g : FpPoly p} {hm : DensePoly.Monic g} {hd : 0 < g.natDegree}
    (c : ZMod64 p) : FpPoly.Quotient g hm hd :=
  FpPoly.Quotient.reduce (FpPoly.C c)

/-- Its selected generator, kept with the defining polynomial. -/
def selectedRoot {p : Nat} [ZMod64.Bounds p] [ZMod64.PrimeModulus p]
    {g : FpPoly p} {hm : DensePoly.Monic g} {hd : 0 < g.natDegree} :
    FpPoly.Quotient g hm hd :=
  FpPoly.Quotient.X

/-- One generic composition of a quotient operation, polynomial evaluation,
and matrix multiplication over the same dynamically chosen quotient ring. -/
def composed {p : Nat} [ZMod64.Bounds p] [ZMod64.PrimeModulus p]
    {g : FpPoly p} {hm : DensePoly.Monic g} {hd : 0 < g.natDegree}
    (a : FpPoly.Quotient g hm hd) : FpPoly.Quotient g hm hd :=
  let x : FpPoly.Quotient g hm hd := selectedRoot
  RuntimeGeneric.composed a x

/-- Runtime construction checks the required primality, word bound, monicity,
and positive degree before opening the dependent quotient type. -/
def run (p : Nat) (modulus input : Array Nat) : Option (Array Nat × Bool) :=
  if hp : Hex.Nat.Prime p then
    if hb : 0 < p ∧ p < 2 ^ 31 then
      letI : ZMod64.Bounds p := ⟨hb.1, hb.2⟩
      letI : ZMod64.PrimeModulus p := ⟨hp⟩
      let g := polynomial p modulus
      if hm : DensePoly.Monic g then
        if hd : 0 < g.natDegree then
          let source := polynomial p input
          let a := FpPoly.Quotient.reduce (g := g) (hmonic := hm) (hg_pos := hd) source
          let output := composed (g := g) (hm := hm) (hd := hd) a
          let root : FpPoly.Quotient g hm hd := selectedRoot
          let mappedCoefficients : DensePoly (FpPoly.Quotient g hm hd) :=
            DensePoly.ofCoeffs (source.toArray.map fun c =>
              constantMap (g := g) (hm := hm) (hd := hd) c)
          let throughMaps := DensePoly.evalImpl mappedCoefficients root
          let quotientMap := FpPoly.Quotient.reduce (g := g) (hmonic := hm) (hg_pos := hd)
          let mapsAgree :=
            decide (throughMaps = a) &&
            decide (quotientMap g = (0 : FpPoly.Quotient g hm hd)) &&
            decide (quotientMap (source + FpPoly.X) = a + root) &&
            decide (quotientMap (source * FpPoly.X) = a * root)
          some (output.val.toArray.map ZMod64.toNat, mapsAgree)
        else none
      else none
    else none
  else none

-- Contrasting runtime characteristics and defining polynomials exercise the
-- same construction and composition. The guards are architectural smoke tests.
#guard run 2 #[1, 1, 1] #[0, 1] == some (#[], true)
#guard run 3 #[2, 0, 1] #[1, 2] == some (#[0, 2], true)
#guard run 3 #[1, 1, 1] #[2, 0, 1] == some (#[2], true)

/-- Mathlib's actual quotient map for the selected defining polynomial.
The source polynomial is identified through HexPolyFpTheory's proved ring equivalence. -/
noncomputable def formalQuotientMap {p : Nat} [ZMod64.Bounds p] (g : FpPoly p) :
    Polynomial (ZMod p) →+* AdjoinRoot (HexPolyFpTheory.fpPolyEquiv g) :=
  AdjoinRoot.mk (HexPolyFpTheory.fpPolyEquiv g)

/-- Candidate interpretation of Hex's canonical representative in the
mathematical quotient. Its preservation of Hex quotient operations and of the
selected constant and root maps is the outstanding bridge obligation. -/
noncomputable def interpret {p : Nat} [ZMod64.Bounds p] [ZMod64.PrimeModulus p]
    {g : FpPoly p} {hm : DensePoly.Monic g} {hd : 0 < g.natDegree}
    (x : FpPoly.Quotient g hm hd) :
    AdjoinRoot (HexPolyFpTheory.fpPolyEquiv g) :=
  formalQuotientMap g (HexPolyFpTheory.fpPolyEquiv x.val)

end Probes.RuntimeQuotient
