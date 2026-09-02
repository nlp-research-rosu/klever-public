import Klean36FizzBuzz.Lemmas

namespace Proof

/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-115fa5a89504e993fee3020685d5cff1b9330768a167593911e0fbe3523b78f7. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x0 x1 : SortInt) : SortInt := x0 + x1

theorem final :
    Klean36FizzBuzz.Lemmas.targetStatement «_+Int_» := by
  intro A B C
  exact Int.add_assoc A B C

end Proof
