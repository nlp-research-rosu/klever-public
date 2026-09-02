import Klean92AnyInt.Lemmas

namespace Proof

/- KORE symbol: LblboolAsInt'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'Bool; frozen source obligations: rule-2337b981dde3e7f5b878ce7ffbb3f2c1c87d9b3c9777edc1dbeab1aeeba99ca5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «boolAsInt(_)_MPY-CORE_Int_Bool» : SortBool → SortInt
  | true => 1
  | false => 0

theorem final :
    Klean92AnyInt.Lemmas.targetStatement «boolAsInt(_)_MPY-CORE_Int_Bool» := by
  intro B
  cases B <;> rfl

end Proof
