import Klean29FilterByPrefix.Lemmas

namespace Proof

/- KORE symbol: LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq; frozen source obligations: rule-656b75764c3203134f266be9408944fcc82d61f11a51b6ca12049b4e0fddc5cb, rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» :
    SortValSeq → SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», tail => tail
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail, suffix =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        head
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» tail suffix)

theorem final :
    Klean29FilterByPrefix.Lemmas.targetStatement «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» := by
  let rec rightIdentity :
      (VS : SortValSeq) →
        «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
            VS
            SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =
          VS
    | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => rfl
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail =>
        congrArg
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head)
          (rightIdentity tail)
  let rec associativity :
      (A B C : SortValSeq) →
        «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
            («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A B)
            C =
          «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
            A
            («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» B C)
    | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => rfl
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail, B, C =>
        congrArg
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head)
          (associativity tail B C)
  exact ⟨rightIdentity, fun C B A => associativity A B C⟩

end Proof
