import Klean149SortedListSum.Lemmas

namespace Proof

/- KORE symbol: LblisStrV'LParUndsRParUnds'MPY-BUILTINS'Unds'Bool'Unds'Val; frozen source obligations: rule-1136beadf72d0cbc65d91ccaf863bbe8bdb49cd73e5a05cca27d05c484b771b6. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isStrV(_)_MPY-BUILTINS_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortStr _ => true
  | _ => false

private def intSeqLength : SortIntSeq → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      1 + intSeqLength rest

private def valSeqLength : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      1 + valSeqLength rest

private def rangeLength? (lo hi step : SortInt) : Option SortInt :=
  if 0 < step then
    if lo < hi then
      some ((hi - lo + step - 1) / step)
    else
      some 0
  else if step < 0 then
    if hi < lo then
      some ((lo - hi - step - 1) / (0 - step))
    else
      some 0
  else
    none

/- KORE symbol: LblseqLen'LParUndsRParUnds'MPY-BUILTINS'Unds'Int'Unds'Val; frozen source obligations: rule-1136beadf72d0cbc65d91ccaf863bbe8bdb49cd73e5a05cca27d05c484b771b6. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «seqLen(_)_MPY-BUILTINS_Int_Val?» : SortVal → Option SortInt
  | SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» elements) =>
      some (intSeqLength elements)
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» elements) =>
      some (valSeqLength elements)
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» elements) =>
      some (valSeqLength elements)
  | SortVal.inj_SortIterable
      (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» lo hi step) =>
      rangeLength? lo hi step
  | SortVal.«setV(_)_MPY-SET_Val_IntSeq» elements =>
      some (intSeqLength elements)
  | _ => none

theorem final :
    Klean149SortedListSum.Lemmas.targetStatement «isStrV(_)_MPY-BUILTINS_Bool_Val» «seqLen(_)_MPY-BUILTINS_Int_Val?» := by
  intro value isString
  cases value <;> try { exact Bool.noConfusion isString }
  case inj_SortStr string =>
    cases string
    exact ⟨fun _ => True.intro, fun _ => rfl⟩

end Proof
