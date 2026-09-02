import Klean28Concatenate.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean28Concatenate.Lemmas

def targetStatement
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» : SortIntSeq → SortIntSeq → SortIntSeq)
    («stringCodes(_)_VERIFICATION_IntSeq_Val» : SortVal → SortIntSeq)
    : Prop :=
    (∀ (V : SortVal) (A : SortIntSeq) (h : (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) = (SortK.kseq (SortKItem.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» («stringCodes(_)_VERIFICATION_IntSeq_Val» V))) SortK.dotk)), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A)) V : SortVal) = (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» («seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» A («stringCodes(_)_VERIFICATION_IntSeq_Val» V))) : SortVal))

end Klean28Concatenate.Lemmas
