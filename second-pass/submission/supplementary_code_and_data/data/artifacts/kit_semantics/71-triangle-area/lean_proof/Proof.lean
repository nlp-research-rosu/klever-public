import Klean71TriangleArea.Lemmas

namespace Proof

/- KORE symbol: LblintToF; frozen source obligations: rule-4118d893fdb23a03019d470e2b1c6fcba5249000dd31f5eede7a49b9bb496c57. Replace this stub with its honest total meaning from the frozen K semantics. -/
def intToF (value : SortInt) : SortFloat :=
  Float.ofInt value
/- KORE symbol: LblproofIntToF; frozen source obligations: rule-4118d893fdb23a03019d470e2b1c6fcba5249000dd31f5eede7a49b9bb496c57. Replace this stub with its honest total meaning from the frozen K semantics. -/
def proofIntToF (value : SortInt) : SortFloat :=
  Float.ofInt value

theorem final :
    Klean71TriangleArea.Lemmas.targetStatement intToF proofIntToF := by
  intro value
  rfl

end Proof
