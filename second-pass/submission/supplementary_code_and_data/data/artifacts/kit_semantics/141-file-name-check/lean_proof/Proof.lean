import Klean141FileNameCheck.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds-GT-'Int'Unds'; frozen source obligations: rule-62d1bbd5b25d2b70152e85917d8c17ce8f2ed86c82cce542d4527216437bc22c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>Int_» (x0 x1 : SortInt) : SortBool := x0 > x1
/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-62d1bbd5b25d2b70152e85917d8c17ce8f2ed86c82cce542d4527216437bc22c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (x0 x1 : SortInt) : SortBool := x0 <= x1

theorem final :
    Klean141FileNameCheck.Lemmas.targetStatement «_>Int_» «_<=Int_» := by
  intro N h
  apply decide_eq_false_iff_not.mpr
  exact Int.not_lt_of_ge (of_decide_eq_true h)

end Proof
