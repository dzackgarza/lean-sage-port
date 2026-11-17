import Probes.RuntimeQuotient

/-! Run the runtime quotient experiment with external input.

Usage: `runtime-quotient PRIME MODULUS-COEFFS INPUT-COEFFS`.
Coefficients are comma-separated natural numbers in ascending degree order.
The result uses the same order and contains canonical residues modulo PRIME.
For example, `runtime-quotient 3 2,0,1 1,2` prints `0,2`.
-/

namespace Probes.Main

def parseCoefficients (source : String) : Except String (Array Nat) := do
  let entries := source.splitOn ","
  let values ← entries.mapM fun entry =>
    match entry.toNat? with
    | some n => .ok n
    | none => .error s!"invalid coefficient: {entry}"
  return values.toArray

def parseArguments (args : List String) : Except String (Nat × Array Nat × Array Nat) := do
  match args with
  | [prime, modulus, input] =>
      let p ← match prime.toNat? with
        | some p => .ok p
        | none => .error s!"invalid characteristic: {prime}"
      let g ← parseCoefficients modulus
      let a ← parseCoefficients input
      return (p, g, a)
  | _ => .error "usage: runtime-quotient PRIME MODULUS-COEFFS INPUT-COEFFS"

def printCoefficients (coefficients : Array Nat) : String :=
  String.intercalate "," (coefficients.toList.map toString)

end Probes.Main

def main (args : List String) : IO UInt32 := do
  let stderr ← IO.getStderr
  match Probes.Main.parseArguments args with
  | .error message =>
      stderr.putStrLn message
      return 2
  | .ok (p, modulus, input) =>
      match Probes.RuntimeQuotient.run p modulus input with
      | none =>
          stderr.putStrLn "invalid domain: characteristic must be prime below 2^31; defining polynomial must be monic and nonconstant"
          return 2
      | some (result, mapsAgree) =>
          IO.println (Probes.Main.printCoefficients result)
          IO.println s!"maps={mapsAgree}"
          return if mapsAgree then 0 else 1
