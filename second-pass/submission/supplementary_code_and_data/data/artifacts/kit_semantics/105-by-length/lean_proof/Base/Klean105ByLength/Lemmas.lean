import Klean105ByLength.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean105ByLength.Lemmas

def targetStatement
    («_==Int_» : SortInt → SortInt → SortBool)
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    (isInt : SortK → SortBool)
    («project:Int» : SortK → SortInt)
    : Prop :=
    (∀ (I : SortInt) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "==" V (SortVal.inj_SortInt I) : SortBool) = («_==Int_» («project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) I : SortBool))

end Klean105ByLength.Lemmas
