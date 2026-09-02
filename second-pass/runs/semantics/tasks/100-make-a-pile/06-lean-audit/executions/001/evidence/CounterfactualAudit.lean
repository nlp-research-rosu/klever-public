import Proof

namespace CounterfactualAudit

def convenientLeftProjection : SortValSeq → SortValSeq → SortValSeq
  | left, _ => left

theorem convenientStillProvesGeneratedTarget :
    Klean100MakeAPile.Lemmas.targetStatement convenientLeftProjection := by
  constructor <;> intros <;> rfl

theorem convenientViolatesFrozenKBase :
    convenientLeftProjection
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          SortVal.«noneV_MPY-CORE_Val»
          SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      ≠
        SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          SortVal.«noneV_MPY-CORE_Val»
          SortValSeq.«.ValSeq_MPY-CORE_ValSeq» := by
  intro impossible
  cases impossible

def convenientFirstNonempty : SortValSeq → SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», tail => tail
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest, _ =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest

theorem convenientFirstNonemptyStillProvesGeneratedTarget :
    Klean100MakeAPile.Lemmas.targetStatement convenientFirstNonempty := by
  constructor
  · intro sequence
    cases sequence <;> rfl
  · intro C B A
    cases A <;> rfl

theorem convenientFirstNonemptyViolatesFrozenKStep :
    convenientFirstNonempty
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          SortVal.«noneV_MPY-CORE_Val»
          SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          SortVal.«noneV_MPY-CORE_Val»
          SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      ≠
        SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          SortVal.«noneV_MPY-CORE_Val»
          (convenientFirstNonempty
            SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
            (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
              SortVal.«noneV_MPY-CORE_Val»
              SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)) := by
  simp [convenientFirstNonempty]

def rightProjection : SortValSeq → SortValSeq → SortValSeq
  | _, right => right

theorem rightProjectionViolatesFirstConjunct :
    rightProjection
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          SortVal.«noneV_MPY-CORE_Val»
          SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
      ≠
        SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          SortVal.«noneV_MPY-CORE_Val»
          SortValSeq.«.ValSeq_MPY-CORE_ValSeq» := by
  simp [rightProjection]

def rightIdentityButNonAssociative : SortValSeq → SortValSeq → SortValSeq
  | left, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => left
  | _, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ _ =>
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

theorem rightIdentityButNonAssociativeHasRightIdentity (left : SortValSeq) :
    rightIdentityButNonAssociative
        left SortValSeq.«.ValSeq_MPY-CORE_ValSeq» = left := rfl

theorem rightIdentityButNonAssociativeViolatesSecondConjunct :
    let one :=
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        SortVal.«noneV_MPY-CORE_Val»
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    rightIdentityButNonAssociative
        (rightIdentityButNonAssociative one one) one
      ≠
        rightIdentityButNonAssociative
          one (rightIdentityButNonAssociative one one) := by
  simp [rightIdentityButNonAssociative]

theorem candidateMatchesFrozenKBase (tail : SortValSeq) :
    Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq» tail = tail := rfl

theorem candidateMatchesFrozenKStep
    (head : SortVal) (rest tail : SortValSeq) :
    Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest)
        tail
      =
        SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          head
          (Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» rest tail) :=
  rfl

end CounterfactualAudit
