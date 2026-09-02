import Klean33SortThird.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean33SortThird.Lemmas

def targetStatement
    («_<=Int_» : SortInt → SortInt → SortBool)
    («sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» : SortValSeq → SortValSeq)
    («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» : SortValSeq → SortValSeq → SortValSeq)
    («vsLen(_)_MPY-CORE_Int_ValSeq» : SortValSeq → SortInt)
    : Prop :=
    (∀ (VS : SortValSeq) (h : («_<=Int_» («vsLen(_)_MPY-CORE_Int_ValSeq» VS) 0) = true), («sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» VS : SortValSeq) = (SortValSeq.«.ValSeq_MPY-CORE_ValSeq» : SortValSeq))
    ∧ (∀ (C : SortValSeq) (B : SortValSeq) (A : SortValSeq), («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A B) C : SortValSeq) = («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» B C) : SortValSeq))
    ∧ (∀ (A : SortValSeq), («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A SortValSeq.«.ValSeq_MPY-CORE_ValSeq» : SortValSeq) = (A : SortValSeq))

end Klean33SortThird.Lemmas
