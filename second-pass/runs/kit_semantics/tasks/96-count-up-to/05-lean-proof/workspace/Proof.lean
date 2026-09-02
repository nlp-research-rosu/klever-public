import Klean96CountUpTo.Lemmas

namespace Proof

/- KORE symbol: LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq; frozen source obligations: rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97, rule-1bc30aceb4ec6e423c8f79079ea7b1c195de5d88396229aa8ee74794085384fa. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» :
    SortValSeq → SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», tail => tail
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest, tail =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        head
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» rest tail)

private theorem valSeqConcat_assoc (A B C : SortValSeq) :
    «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A B) C =
      «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        A («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» B C) :=
  match A with
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => rfl
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest =>
      congrArg
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head)
        (valSeqConcat_assoc rest B C)

private theorem valSeqConcat_right_id (A : SortValSeq) :
    «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        A SortValSeq.«.ValSeq_MPY-CORE_ValSeq» = A :=
  match A with
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => rfl
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest =>
      congrArg
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head)
        (valSeqConcat_right_id rest)

theorem final :
    Klean96CountUpTo.Lemmas.targetStatement «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» := by
  exact ⟨fun C B A => valSeqConcat_assoc A B C, valSeqConcat_right_id⟩

end Proof
