import Klean55Fib.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-3937e2183350f860b8052e715b9784df8e149714f99e2077f426b8adaae07193. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» (x y : SortInt) : SortInt := x - y
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-3937e2183350f860b8052e715b9784df8e149714f99e2077f426b8adaae07193. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x y : SortInt) : SortInt := x + y

theorem final :
    Klean55Fib.Lemmas.targetStatement «_-Int_» «_+Int_» := by
  unfold Klean55Fib.Lemmas.targetStatement
  intro A B
  change A + B - A = B
  rw [Int.add_comm A B, Int.add_sub_cancel]

end Proof
