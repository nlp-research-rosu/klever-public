import Proof

namespace OperationalBridgeAudit

abbrev empty : SortValSeq :=
  SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

def consInt (value : Int) (tail : SortValSeq) : SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
    (SortVal.inj_SortInt value)
    tail

theorem candidate_base (tail : SortValSeq) :
    Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» empty tail =
      tail := by
  rfl

theorem candidate_step
    (head : SortVal) (rest tail : SortValSeq) :
    Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest)
        tail =
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        head
        (Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» rest tail) := by
  rfl

example :
    Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        empty (consInt 3 empty) =
      consInt 3 empty := by
  rfl

example :
    Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        (consInt 1 (consInt 2 empty))
        (consInt 3 empty) =
      consInt 1 (consInt 2 (consInt 3 empty)) := by
  rfl

/- This convenient but operationally false implementation demonstrates that
   the target equations alone do not determine the frozen K operation. -/
def fakeLeft (left _right : SortValSeq) : SortValSeq := left

theorem fakeLeft_still_proves_target :
    Klean96CountUpTo.Lemmas.targetStatement fakeLeft := by
  exact ⟨by intros; rfl, by intros; rfl⟩

theorem fakeLeft_violates_K_base :
    fakeLeft empty (consInt 3 empty) ≠
      Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        empty (consInt 3 empty) := by
  simp [
    fakeLeft,
    consInt,
    Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
  ]

def fakeConstant (_left _right : SortValSeq) : SortValSeq := empty

theorem fakeConstant_is_rejected :
    ¬ Klean96CountUpTo.Lemmas.targetStatement fakeConstant := by
  intro assumed
  have impossible := assumed.2 (consInt 7 empty)
  simp [fakeConstant, consInt] at impossible

end OperationalBridgeAudit
