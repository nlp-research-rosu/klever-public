import Klean7FilterBySubstring.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean7FilterBySubstring.Lemmas

def targetStatement
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («strCodes(_)_VERIFICATION_IntSeq_Val» : SortVal → SortIntSeq)
    : Prop :=
    (∀ (V : SortVal) (P : SortIntSeq) (h : (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) = (SortK.kseq (SortKItem.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» («strCodes(_)_VERIFICATION_IntSeq_Val» V))) SortK.dotk)), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "in" (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» P)) V : SortBool) = («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "in" (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» P)) (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» («strCodes(_)_VERIFICATION_IntSeq_Val» V))) : SortBool))

end Klean7FilterBySubstring.Lemmas
