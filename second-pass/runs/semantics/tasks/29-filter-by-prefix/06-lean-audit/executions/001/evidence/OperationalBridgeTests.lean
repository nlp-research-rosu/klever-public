import Proof

namespace OperationalBridgeTests

abbrev empty : SortValSeq :=
  SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

abbrev cons : SortVal → SortValSeq → SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»

abbrev concat : SortValSeq → SortValSeq → SortValSeq :=
  Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»

-- Direct transcription of the two frozen MPY-LIST equations.
def frozenKConcat : SortValSeq → SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», suffix => suffix
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail, suffix =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        head
        (frozenKConcat tail suffix)

theorem candidateMatchesFrozenKConcat :
    (a b : SortValSeq) → concat a b = frozenKConcat a b
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ => rfl
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail, suffix =>
      congrArg
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head)
        (candidateMatchesFrozenKConcat tail suffix)

def x : SortVal := SortVal.«noneV_MPY-CORE_Val»
def y : SortVal := SortVal.inj_SortBool false
def z : SortVal := SortVal.inj_SortBool true

example : concat empty (cons x empty) = cons x empty := rfl
example : concat (cons x empty) empty = cons x empty := rfl
example :
    concat (cons x empty) (cons y empty) =
      cons x (cons y empty) := rfl
example :
    concat (cons x (cons y empty)) (cons z empty) =
      cons x (cons y (cons z empty)) := rfl

-- This convenient interpretation satisfies both generated obligations, so the
-- target alone cannot establish the operational bridge.
def leftProjection (a _b : SortValSeq) : SortValSeq := a

theorem leftProjectionPassesGeneratedTarget :
    Klean29FilterByPrefix.Lemmas.targetStatement leftProjection := by
  constructor
  · intro VS
    rfl
  · intro C B A
    rfl

-- The candidate is not that convenient interpretation.
example :
    concat empty (cons x empty) ≠
      leftProjection empty (cons x empty) := by
  intro h
  cases h

-- Mutating the recursive branch to drop every left-hand element also differs
-- on a one-element boundary witness.
def dropLeft : SortValSeq → SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», suffix => suffix
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ tail, suffix =>
      dropLeft tail suffix

example :
    concat (cons x empty) empty ≠
      dropLeft (cons x empty) empty := by
  intro h
  cases h

end OperationalBridgeTests
