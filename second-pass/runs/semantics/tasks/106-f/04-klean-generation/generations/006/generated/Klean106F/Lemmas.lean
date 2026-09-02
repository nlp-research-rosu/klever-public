import Klean106F.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean106F.Lemmas

def targetStatement
    («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» : SortValSeq → SortValSeq → SortValSeq)
    : Prop :=
    (∀ (C : SortValSeq) (B : SortValSeq) (A : SortValSeq), («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A B) C : SortValSeq) = («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» B C) : SortValSeq))
    ∧ (∀ (A : SortValSeq), («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A SortValSeq.«.ValSeq_MPY-CORE_ValSeq» : SortValSeq) = (A : SortValSeq))
    ∧ (∀ (B : SortValSeq) (P : SortValSeq) (A : SortValSeq), ((«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» P A : SortValSeq) = («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» P B : SortValSeq)) ↔ ((A : SortValSeq) = (B : SortValSeq)))
    ∧ (∀ (A : SortValSeq) (P : SortValSeq), ((P : SortValSeq) = («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» P A : SortValSeq)) ↔ ((SortValSeq.«.ValSeq_MPY-CORE_ValSeq» : SortValSeq) = (A : SortValSeq)))

end Klean106F.Lemmas
