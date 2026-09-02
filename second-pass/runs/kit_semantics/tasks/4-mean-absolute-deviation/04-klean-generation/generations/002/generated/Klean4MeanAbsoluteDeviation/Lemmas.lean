import Klean4MeanAbsoluteDeviation.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean4MeanAbsoluteDeviation.Lemmas

def targetStatement
    (addF : SortFloat → SortFloat → SortFloat)
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    (isFloat : SortK → SortBool)
    («project:Float» : SortK → SortFloat)
    (projectFloat : SortVal → SortFloat)
    (subF : SortFloat → SortFloat → SortFloat)
    : Prop :=
    (∀ (V : SortVal), (True) ↔ (((isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (A : SortFloat) (h : (isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" (SortVal.inj_SortFloat A) V : SortVal) = (SortVal.inj_SortFloat (addF A (projectFloat V)) : SortVal))
    ∧ (∀ (M : SortFloat) (V : SortVal) (h : (isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "-" V (SortVal.inj_SortFloat M) : SortVal) = (SortVal.inj_SortFloat (subF (projectFloat V) M) : SortVal))

end Klean4MeanAbsoluteDeviation.Lemmas
