import Klean12Longest.Lemmas

namespace Proof

/- KORE symbol: LblisStringValue'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val; frozen source obligations: rule-ddffe23dc5c6ffd5ffac0d16bb982569a790626473fe51f3053dbbcfd160d303, rule-a83d2beb46d0d51905977beb804054c3129461bb6f5faf35187591b53b4dc122. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isStringValue(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortStr _ => true
  | _ => false

private def emptyStr : SortStr :=
  SortStr.«str(_)_MPY-CORE_Str_IntSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

/- KORE symbol: LblprojectString; frozen source obligations: rule-a83d2beb46d0d51905977beb804054c3129461bb6f5faf35187591b53b4dc122. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectString : SortVal → SortStr
  | SortVal.inj_SortStr value => value
  -- The K rules call projectString only under isStringValue. This branch is
  -- the total Lean completion of that guarded operation and is unreachable
  -- whenever the frozen operational precondition holds.
  | _ => emptyStr

private def intSeqLength : SortIntSeq → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      1 + intSeqLength rest

private def valSeqLength : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      1 + valSeqLength rest

private def rangeLength (lo hi step : SortInt) : SortInt :=
  if step > 0 then
    if hi > lo then Int.tdiv (hi - lo + step - 1) step else 0
  else if step < 0 then
    if hi < lo then Int.tdiv (lo - hi - step - 1) (0 - step) else 0
  else
    -- Python range construction rejects a zero step, so this merely totalizes
    -- a state that cannot be produced by the frozen execution semantics.
    0

/- KORE symbol: LblseqLen'LParUndsRParUnds'MPY-BUILTINS'Unds'Int'Unds'Val; frozen source obligations: rule-a83d2beb46d0d51905977beb804054c3129461bb6f5faf35187591b53b4dc122. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «seqLen(_)_MPY-BUILTINS_Int_Val» : SortVal → SortInt
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» chars) =>
      intSeqLength chars
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values) =>
      valSeqLength values
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values) =>
      valSeqLength values
  | SortVal.inj_SortIterable
      (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
        lo hi step) =>
      rangeLength lo hi step
  | SortVal.«setV(_)_MPY-SET_Val_IntSeq» values =>
      intSeqLength values
  -- seqLen is partial in MPY-BUILTINS. Zero is the total Lean completion on
  -- values for which the frozen semantics has no seqLen execution rule.
  | _ => 0

/- KORE symbol: LblseqLenString; frozen source obligations: rule-a83d2beb46d0d51905977beb804054c3129461bb6f5faf35187591b53b4dc122. Replace this stub with its honest total meaning from the frozen K semantics. -/
def seqLenString : SortStr → SortInt
  | SortStr.«str(_)_MPY-CORE_Str_IntSeq» chars => intSeqLength chars

/- KORE symbol: Lblproject'Coln'Str; frozen source obligations: rule-ddffe23dc5c6ffd5ffac0d16bb982569a790626473fe51f3053dbbcfd160d303. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Str?» : SortK → Option SortStr
  | SortK.kseq (SortKItem.inj_SortStr value) SortK.dotk => some value
  | _ => none

theorem final :
    Klean12Longest.Lemmas.targetStatement «isStringValue(_)_VERIFICATION-BASE_Bool_Val» projectString «seqLen(_)_MPY-BUILTINS_Int_Val» seqLenString «project:Str?» := by
  constructor
  · intro V
    cases V <;>
      simp [
        «project:Str?»,
        «isStringValue(_)_VERIFICATION-BASE_Bool_Val»,
        inj
      ]
  · intro V h
    cases V <;>
      simp_all [
        «isStringValue(_)_VERIFICATION-BASE_Bool_Val»,
        «seqLen(_)_MPY-BUILTINS_Int_Val»,
        projectString,
        seqLenString
      ]

end Proof
