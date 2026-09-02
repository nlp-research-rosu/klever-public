import Klean86AntiShuffle.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-8035a5d5e2dd908c685b0f3f6b47722aade54582ecf7e781dfd68bc1469d72b1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (left right : SortInt) : SortBool :=
  decide (left < right)
/- KORE symbol: LblstrLt'LParUndsCommUndsRParUnds'MPY-STR'Unds'Bool'Unds'IntSeq'Unds'IntSeq; frozen source obligations: rule-8035a5d5e2dd908c685b0f3f6b47722aade54582ecf7e781dfd68bc1469d72b1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» :
    SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» left leftRest,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» right rightRest =>
      if left < right then true
      else if left > right then false
      else «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» leftRest rightRest

theorem final :
    Klean86AntiShuffle.Lemmas.targetStatement «_<Int_» «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» := by
  unfold Klean86AntiShuffle.Lemmas.targetStatement
  intro D C
  by_cases less : C < D
  · simp [«strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq», «_<Int_», less]
  · simp [«strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq», «_<Int_», less]

end Proof
