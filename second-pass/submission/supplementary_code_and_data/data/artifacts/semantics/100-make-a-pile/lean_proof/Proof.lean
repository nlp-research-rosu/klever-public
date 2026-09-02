import Klean100MakeAPile.Lemmas

namespace Proof

/- KORE symbol: LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq; frozen source obligations: rule-656b75764c3203134f266be9408944fcc82d61f11a51b6ca12049b4e0fddc5cb, rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» :
    SortValSeq → SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», tail => tail
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest, tail =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        head
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» rest tail)

theorem final :
    Klean100MakeAPile.Lemmas.targetStatement «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» := by
  constructor
  · intro VS
    let rec rightIdentity (seq : SortValSeq) :
        «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
            seq SortValSeq.«.ValSeq_MPY-CORE_ValSeq» = seq :=
      match seq with
      | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => rfl
      | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest =>
          congrArg
            (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head)
            (rightIdentity rest)
    exact rightIdentity VS
  · intro C B A
    let rec associative (left middle right : SortValSeq) :
        «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
            («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» left middle)
            right =
          «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
            left
            («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» middle right) :=
      match left with
      | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => rfl
      | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest =>
          congrArg
            (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head)
            (associative rest middle right)
    exact associative A B C

end Proof
