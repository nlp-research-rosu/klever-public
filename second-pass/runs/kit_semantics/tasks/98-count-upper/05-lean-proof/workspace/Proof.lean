import Klean98CountUpper.Lemmas

namespace Proof

/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-53698f5d4516a68cfad0b5d035a1d78bc9b46c118a3c2e541a4a6ef1be0683a4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x0 x1 : SortInt) : SortInt := x0 + x1

theorem final :
    Klean98CountUpper.Lemmas.targetStatement «_+Int_» := by
  intro C B A
  exact Int.add_assoc A B C

end Proof
