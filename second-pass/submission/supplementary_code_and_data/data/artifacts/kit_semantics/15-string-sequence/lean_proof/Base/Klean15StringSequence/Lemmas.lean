import Klean15StringSequence.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean15StringSequence.Lemmas

def targetStatement
    («_<=Int_» : SortInt → SortInt → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    («Int2String(_)_STRING-COMMON_String_Int» : SortInt → SortString)
    («seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» : SortIntSeq → SortIntSeq → SortIntSeq)
    («sequenceAcc(_,_,_)_VERIFICATION_IntSeq_IntSeq_Int_Int» : SortIntSeq → SortInt → SortInt → SortIntSeq)
    («strToCodes(_)_MPY-STR_IntSeq_String» : SortString → SortIntSeq)
    : Prop :=
    (∀ (N : SortInt) (I : SortInt) (ACC : SortIntSeq) (h : («_<=Int_» I N) = true), («sequenceAcc(_,_,_)_VERIFICATION_IntSeq_IntSeq_Int_Int» («seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» («seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» ACC (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)) («strToCodes(_)_MPY-STR_IntSeq_String» («Int2String(_)_STRING-COMMON_String_Int» I))) («_+Int_» I 1) N : SortIntSeq) = («sequenceAcc(_,_,_)_VERIFICATION_IntSeq_IntSeq_Int_Int» ACC I N : SortIntSeq))

end Klean15StringSequence.Lemmas
