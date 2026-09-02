import Klean32FindZero.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean32FindZero.Lemmas

def targetStatement
    («numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» : SortNumSeq → SortValSeq)
    : Prop :=
    (∀ (NS : SortNumSeq), ((«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» NS : SortValSeq) = (SortValSeq.«.ValSeq_MPY-CORE_ValSeq» : SortValSeq)) ↔ ((NS : SortNumSeq) = (SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq» : SortNumSeq)))
    ∧ (∀ (NS2 : SortNumSeq) (NS1 : SortNumSeq), ((«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» NS1 : SortValSeq) = («numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» NS2 : SortValSeq)) ↔ ((NS1 : SortNumSeq) = (NS2 : SortNumSeq)))
    ∧ (∀ (R : SortNumSeq) (I : SortInt) (NS : SortNumSeq), ((«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» NS : SortValSeq) = (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) («numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» R) : SortValSeq)) ↔ ((NS : SortNumSeq) = (SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq» I R : SortNumSeq)))
    ∧ (∀ (R : SortNumSeq) (F : SortFloat) (NS : SortNumSeq), ((«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» NS : SortValSeq) = (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortFloat F) («numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» R) : SortValSeq)) ↔ ((NS : SortNumSeq) = (SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq» F R : SortNumSeq)))

end Klean32FindZero.Lemmas
