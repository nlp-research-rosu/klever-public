import Klean114Minsubarraysum.Lemmas

namespace Proof

/- KORE symbol: LblvalSeqAt'LParUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Val'Unds'ValSeq'Unds'Int; frozen source obligations: rule-7a7edac73364fddfa1ef4bac81d105b3bf56b8eb38bcf5f58c3e0870f8a6ae55. Replace this stub with its honest total meaning from the frozen K semantics. -/
def intValsAt : SortIntSeq → SortInt → SortVal
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ =>
      SortVal.«noneV_MPY-CORE_Val»
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» value rest, index =>
      if index = 0 then
        SortVal.inj_SortInt value
      else if 0 < index then
        intValsAt rest (index - 1)
      else
        SortVal.«noneV_MPY-CORE_Val»

def «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» :
    SortValSeq → SortInt → SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ =>
      SortVal.«noneV_MPY-CORE_Val»
  | SortValSeq.«intVals(_)_VERIFICATION-BASE_ValSeq_IntSeq» values, index =>
      intValsAt values index
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest, index =>
      if index = 0 then
        value
      else if 0 < index then
        «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» rest (index - 1)
      else
        SortVal.«noneV_MPY-CORE_Val»

theorem final :
    Klean114Minsubarraysum.Lemmas.targetStatement «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» := by
  intro _R I
  rfl

end Proof
