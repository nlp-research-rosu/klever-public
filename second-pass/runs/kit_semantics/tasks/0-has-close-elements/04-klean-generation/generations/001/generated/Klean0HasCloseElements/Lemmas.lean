import Klean0HasCloseElements.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean0HasCloseElements.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («asFloat(_)_VERIFICATION_Float_Val» : SortVal → SortFloat)
    (isFloat : SortK → SortBool)
    (subF : SortFloat → SortFloat → SortFloat)
    : Prop :=
    (∀ (B : SortVal) (A : SortVal) (h : (_andBool_ (isFloat (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk)) (isFloat (SortK.kseq ((@inj SortVal SortKItem) B) SortK.dotk))) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "-" A B : SortVal) = (SortVal.inj_SortFloat (subF («asFloat(_)_VERIFICATION_Float_Val» A) («asFloat(_)_VERIFICATION_Float_Val» B)) : SortVal))

end Klean0HasCloseElements.Lemmas
