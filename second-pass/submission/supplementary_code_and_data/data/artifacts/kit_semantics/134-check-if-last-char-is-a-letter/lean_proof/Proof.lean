import Klean134CheckIfLastCharIsALetter.Lemmas

namespace Proof

/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-61ffc6cd69c6bad2d2ff37db34f5511581d591c5239127275c27ebf328e89030. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (x y : SortInt) : SortBool :=
  decide (x = y)
/- KORE symbol: Lbl'UndsEqlsEqls'K'Unds'; frozen source obligations: rule-e0a5c8a793196820ea84731c2d229d364f6fe3e8c376c15bf12d3d2cfb1f31a4, rule-61ffc6cd69c6bad2d2ff37db34f5511581d591c5239127275c27ebf328e89030. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_==K_» (x y : SortK) : SortBool :=
  @decide (x = y) (Classical.propDecidable (x = y))

theorem final :
    Klean134CheckIfLastCharIsALetter.Lemmas.targetStatement «_==Int_» «_==K_» := by
  unfold Klean134CheckIfLastCharIsALetter.Lemmas.targetStatement
  constructor
  · intro _REST _C
    simp [«_==K_»]
  · intro D C
    simp [«_==K_», «_==Int_»]

end Proof
