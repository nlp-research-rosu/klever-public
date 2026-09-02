import Klean43PairsSumToZero.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean43PairsSumToZero.Lemmas

def targetStatement
    («_-Int_» : SortInt → SortInt → SortInt)
    («_==Int_» : SortInt → SortInt → SortBool)
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («applyUn(_,_)_MPY-CORE_Val_String_Val» : SortString → SortVal → SortVal)
    («intProj(_)_INT-PROJECTION_Int_Val» : SortVal → SortInt)
    (isInt : SortK → SortBool)
    : Prop :=
    (∀ (I : SortInt) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "==" V (SortVal.inj_SortInt I) : SortBool) = («_==Int_» («intProj(_)_INT-PROJECTION_Int_Val» V) I : SortBool))
    ∧ (∀ (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyUn(_,_)_MPY-CORE_Val_String_Val» "-" V : SortVal) = (SortVal.inj_SortInt («_-Int_» 0 («intProj(_)_INT-PROJECTION_Int_Val» V)) : SortVal))

end Klean43PairsSumToZero.Lemmas
