import Proof

namespace OperationalAudit

open Klean28Concatenate.Lemmas

def empty : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def cons (x : SortInt) (xs : SortIntSeq) : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs

def strVal (xs : SortIntSeq) : SortVal :=
  SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» xs)

theorem seqConcatBase (ys : SortIntSeq) :
    Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» empty ys = ys := rfl

theorem seqConcatStep
    (x : SortInt) (xs ys : SortIntSeq) :
    Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (cons x xs) ys
      =
    cons x
      (Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» xs ys) := rfl

theorem stringCodesString (xs : SortIntSeq) :
    Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val» (strVal xs) = xs := rfl

theorem applyBinStringPlus (lhs rhs : SortIntSeq) :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      "+" (strVal lhs) (strVal rhs)
      =
    strVal
      (Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» lhs rhs) := rfl

example :
    Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq»
      (cons 1 (cons 2 empty)) (cons 3 empty)
      = cons 1 (cons 2 (cons 3 empty)) := rfl

example :
    Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val»
      (strVal (cons 7 empty))
      = cons 7 empty := rfl

example :
    Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val»
      (SortVal.inj_SortInt 7)
      = empty := rfl

example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      "+" (strVal (cons 1 empty)) (strVal (cons 2 empty))
      = strVal (cons 1 (cons 2 empty)) := rfl

/- This is an adversarial off-domain witness. The candidate returns `noneV`,
   while frozen MPY-INT says `applyBin("+", I1, I2) => I1 +Int I2`. -/
example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      "+" (SortVal.inj_SortInt 1) (SortVal.inj_SortInt 2)
      = SortVal.«noneV_MPY-CORE_Val» := rfl

def constantNoneApply : SortString → SortVal → SortVal → SortVal :=
  fun _ _ _ => SortVal.«noneV_MPY-CORE_Val»

theorem targetRejectsRelevantApplyMutation :
    ¬ targetStatement constantNoneApply
      Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq»
      Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val» := by
  intro h
  have bad := h (strVal empty) empty rfl
  cases bad

def constantEmptySeq : SortIntSeq → SortIntSeq → SortIntSeq :=
  fun _ _ => empty

theorem targetRejectsRelevantSeqMutation :
    ¬ targetStatement
      Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      constantEmptySeq
      Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val» := by
  intro h
  have bad := h (strVal (cons 2 empty)) (cons 1 empty) rfl
  cases bad

def constantEmptyCodes : SortVal → SortIntSeq :=
  fun _ => empty

/- The fixed proposition alone permits this bad projection because its guard
   becomes unsatisfiable for nonempty strings. Operational bridge checking is
   therefore load-bearing. -/
theorem targetAllowsBadCodes :
    targetStatement
      Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq»
      constantEmptyCodes := by
  intro V A h
  cases V <;>
    simp_all [inj, constantEmptyCodes,
      Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
      Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq»]
  case inj_SortStr x =>
    cases x
    rename_i codes
    change
      SortKItem.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes)
        =
      SortKItem.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» empty)
      at h
    injection h with hcodes
    cases hcodes
    rfl

def constantEmptyApply : SortString → SortVal → SortVal → SortVal :=
  fun _ _ _ => strVal empty

/- Coordinated hard-coded interpretations can also satisfy the target. -/
theorem targetAllowsCoordinatedConstants :
    targetStatement constantEmptyApply constantEmptySeq constantEmptyCodes := by
  intro V A h
  rfl

end OperationalAudit
