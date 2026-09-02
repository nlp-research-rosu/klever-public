import Klean74TotalMatch.Lemmas

namespace Proof

/- KORE symbol: LblisLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'IntSeq; frozen source obligations: rule-b3f45b5d74172f8b06aeed730c933057ce5ded1254eac17997dee1565ec954d1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isLen(_)_MPY-CORE_Int_IntSeq» : SortIntSeq → SortInt
  | .«.IntSeq_MPY-CORE_IntSeq» => 0
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ tail =>
      1 + «isLen(_)_MPY-CORE_Int_IntSeq» tail

/- KORE symbol: LblisStrV'LParUndsRParUnds'MPY-BUILTINS'Unds'Bool'Unds'Val; frozen source obligations: rule-b3f45b5d74172f8b06aeed730c933057ce5ded1254eac17997dee1565ec954d1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isStrV(_)_MPY-BUILTINS_Bool_Val» : SortVal → SortBool
  | .inj_SortStr _ => true
  | _ => false

/- MPY-CORE's vsLen equations, used by the list and tuple seqLen rules. -/
private def valSeqLength : SortValSeq → SortInt
  | .«.ValSeq_MPY-CORE_ValSeq» => 0
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ tail =>
      1 + valSeqLength tail

/- MPY-RANGE's three rangeLen rules. The final branch totalizes the invalid
   zero-step representation, which no fixed-semantics range constructor emits. -/
private def rangeLength (lower upper step : SortInt) : SortInt :=
  if step > 0 then
    if upper > lower then
      Int.tdiv (upper - lower + step - 1) step
    else
      0
  else if step < 0 then
    if upper < lower then
      Int.tdiv (lower - upper - step - 1) (0 - step)
    else
      0
  else
    0

/- KORE symbol: LblseqLen'LParUndsRParUnds'MPY-BUILTINS'Unds'Int'Unds'Val; frozen source obligations: rule-b3f45b5d74172f8b06aeed730c933057ce5ded1254eac17997dee1565ec954d1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «seqLen(_)_MPY-BUILTINS_Int_Val» : SortVal → SortInt
  | .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» values) =>
      valSeqLength values
  | .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» values) =>
      valSeqLength values
  | .inj_SortIterable
      (.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» lower upper step) =>
      rangeLength lower upper step
  | .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» codes) =>
      «isLen(_)_MPY-CORE_Int_IntSeq» codes
  | .«setV(_)_MPY-SET_Val_IntSeq» values =>
      «isLen(_)_MPY-CORE_Int_IntSeq» values
  /- seqLen is partial in K. This total extension is used only outside the five
     fixed-semantics rule domains; the theorem's isStrV guard excludes it. -/
  | _ => 0

/- KORE symbol: LblstringCodes'LParUndsRParUnds'VERIFICATION'Unds'IntSeq'Unds'Val; frozen source obligations: rule-b3f45b5d74172f8b06aeed730c933057ce5ded1254eac17997dee1565ec954d1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «stringCodes(_)_VERIFICATION_IntSeq_Val» : SortVal → SortIntSeq
  | .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» codes) => codes
  | _ => .«.IntSeq_MPY-CORE_IntSeq»

theorem final :
    Klean74TotalMatch.Lemmas.targetStatement «isLen(_)_MPY-CORE_Int_IntSeq» «isStrV(_)_MPY-BUILTINS_Bool_Val» «seqLen(_)_MPY-BUILTINS_Int_Val» «stringCodes(_)_VERIFICATION_IntSeq_Val» := by
  unfold Klean74TotalMatch.Lemmas.targetStatement
  intro value isString
  cases value <;> cases isString <;> rfl

end Proof
