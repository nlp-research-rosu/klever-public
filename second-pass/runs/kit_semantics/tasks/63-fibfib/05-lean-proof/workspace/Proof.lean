import Proof.FibfibModel

namespace Proof

/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-2c1e06471f4016481e42f60cdb6c9983f09da5b801cc9dc90ba306594047c7a8. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>=Int_» (x0 x1 : SortInt) : SortBool :=
  decide (x0 ≥ x1)
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-2c1e06471f4016481e42f60cdb6c9983f09da5b801cc9dc90ba306594047c7a8. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x0 x1 : SortInt) : SortInt :=
  x0 + x1
/- KORE symbol: LblfibfibSpec'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Int'Unds'Int; frozen source obligations: rule-2c1e06471f4016481e42f60cdb6c9983f09da5b801cc9dc90ba306594047c7a8. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : SortInt :=
  Proof.FibfibModel.fibfibInt x0

theorem final :
    Klean63Fibfib.Lemmas.targetStatement «_>=Int_» «_+Int_» «fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» := by
  intro I h
  have hI : 0 ≤ I := by
    simpa [«_>=Int_»] using h
  simpa [«_+Int_», «fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»] using
    Proof.FibfibModel.fibfibInt_add_three I hI

end Proof
