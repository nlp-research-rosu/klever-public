import Klean51RemoveVowels.Lemmas

namespace Proof

/- KORE symbol: LblisVowelCode'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Int; frozen source obligations: rule-94d2fdc35d3fdf3c396f6195fb860162747c2dc403f48fae46276855a3075f93. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isVowelCode(_)_VERIFICATION_Bool_Int» (C : SortInt) : SortBool :=
  C == 65 || C == 69 || C == 73 || C == 79 || C == 85 ||
  C == 97 || C == 101 || C == 105 || C == 111 || C == 117

private def strPrefix : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      a == b && strPrefix as bs

/- KORE symbol: LblstrContains'LParUndsCommUndsRParUnds'MPY-STR'Unds'Bool'Unds'IntSeq'Unds'IntSeq; frozen source obligations: rule-94d2fdc35d3fdf3c396f6195fb860162747c2dc403f48fae46276855a3075f93. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq»
    (needle : SortIntSeq) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      strPrefix needle SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest =>
      if strPrefix needle
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest) then
        true
      else
        «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» needle rest

theorem final :
    Klean51RemoveVowels.Lemmas.targetStatement «isVowelCode(_)_VERIFICATION_Bool_Int» «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» := by
  intro C
  simp [
    «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq»,
    strPrefix,
    «isVowelCode(_)_VERIFICATION_Bool_Int»
  ]
  apply Bool.eq_iff_iff.mpr
  simp only [Bool.or_eq_true, decide_eq_true_eq, beq_iff_eq]
  simp only [or_comm, or_left_comm, or_assoc]

end Proof
