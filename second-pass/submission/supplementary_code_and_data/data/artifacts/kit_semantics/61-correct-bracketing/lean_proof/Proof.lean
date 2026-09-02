import Klean61CorrectBracketing.Lemmas

namespace Proof

/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-d9b0adbebf1e3f908a9944544102b6bcd8aee7d5a41871e3719cd38e5470aaa0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (x y : SortInt) : SortBool := x == y
/- KORE symbol: Lbl'UndsEqlsSlshEqls'Int'Unds'; frozen source obligations: rule-d9b0adbebf1e3f908a9944544102b6bcd8aee7d5a41871e3719cd38e5470aaa0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_=/=Int_» (x y : SortInt) : SortBool := x != y

theorem final :
    Klean61CorrectBracketing.Lemmas.targetStatement «_==Int_» «_=/=Int_» := by
  intro Y _X C h
  have hne : C ≠ 40 := by
    simpa [«_=/=Int_»] using h
  have heq : (C == (40 : SortInt)) = false :=
    beq_eq_false_iff_ne.mpr hne
  simp [«_==Int_», Klean61CorrectBracketing.Lemmas.kite, heq]

end Proof
