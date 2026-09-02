import Klean29FilterByPrefix.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean29FilterByPrefix.Lemmas

def targetStatement
    («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» : SortValSeq → SortValSeq → SortValSeq)
    : Prop :=
    (∀ (VS : SortValSeq), «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» VS SortValSeq.«.ValSeq_MPY-CORE_ValSeq» = VS)
    ∧ (∀ (A : SortValSeq) (B : SortValSeq) (C : SortValSeq), «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A B) C = «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» B C))

end Klean29FilterByPrefix.Lemmas
