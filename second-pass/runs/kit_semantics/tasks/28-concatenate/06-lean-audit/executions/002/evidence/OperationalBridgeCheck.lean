import Proof

namespace OperationalBridgeCheck

open SortIntSeq SortStr SortVal

private def nilCodes : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

private def oneCode (x : Int) : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x nilCodes

private def twoCodes (x y : Int) : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x (oneCode y)

private def threeCodes (x y z : Int) : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x (twoCodes y z)

private def stringVal (codes : SortIntSeq) : SortVal :=
  SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes)

-- Exact base/step behavior of frozen MPY-STR seqConcat.
example :
    Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» nilCodes (oneCode 98) =
      oneCode 98 := rfl

example :
    Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (twoCodes 97 98) (oneCode 99) =
      threeCodes 97 98 99 := rfl

-- Exact string projection and owise fallback from verification.k.
example :
    Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val» (stringVal (twoCodes 97 98)) =
      twoCodes 97 98 := rfl

example :
    Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val» (SortVal.inj_SortInt 17) =
      nilCodes := rfl

-- The relevant applyBin string branch, including operand order and empties.
example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+"
        (stringVal (twoCodes 97 98)) (stringVal (oneCode 99)) =
      stringVal (threeCodes 97 98 99) := rfl

example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+"
        (stringVal nilCodes) (stringVal (oneCode 120)) =
      stringVal (oneCode 120) := rfl

-- A concrete inhabitant of the generated rule premise: the obligation is not
-- closed only because its equality hypothesis is impossible.
example :
    SortK.kseq ((@inj SortVal SortKItem) (stringVal (oneCode 98))) SortK.dotk =
      SortK.kseq
        (SortKItem.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            (Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val»
              (stringVal (oneCode 98)))))
        SortK.dotk := rfl

-- Additional frozen applyBin rules and floor-sensitive negative cases.
example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+"
        (SortVal.inj_SortInt 2) (SortVal.inj_SortInt 3) =
      SortVal.inj_SortInt 5 := rfl

example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+"
        (SortVal.inj_SortBool true) (SortVal.inj_SortInt 4) =
      SortVal.inj_SortInt 5 := rfl

example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "%"
        (SortVal.inj_SortInt (-7)) (SortVal.inj_SortInt 3) =
      SortVal.inj_SortInt 2 := rfl

example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "//"
        (SortVal.inj_SortInt (-7)) (SortVal.inj_SortInt 3) =
      SortVal.inj_SortInt (-3) := rfl

-- A coordinated, operationally false implementation still proves the raw
-- generated equation. This is the counterfactual that makes the independent
-- bridge checks necessary.
private def badCodes (_ : SortVal) : SortIntSeq := nilCodes
private def badConcat (_ _ : SortIntSeq) : SortIntSeq := nilCodes
private def badApply (_ : SortString) (_ _ : SortVal) : SortVal :=
  stringVal nilCodes

theorem counterfactualConvenienceProvesTarget :
    Klean28Concatenate.Lemmas.targetStatement badApply badConcat badCodes := by
  intro V A h
  rfl

-- The candidate is observably different from each convenient mutation.
example :
    Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val» (stringVal (oneCode 97)) ≠
      badCodes (stringVal (oneCode 97)) := by
  intro h
  cases h

example :
    Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (oneCode 97) (oneCode 98) ≠
      badConcat (oneCode 97) (oneCode 98) := by
  intro h
  cases h

example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+"
        (stringVal (oneCode 97)) (stringVal (oneCode 98)) ≠
      badApply "+" (stringVal (oneCode 97)) (stringVal (oneCode 98)) := by
  intro h
  cases h

#reduce Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq»
  (twoCodes 97 98) (oneCode 99)
#reduce Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val»
  (stringVal (twoCodes 97 98))
#reduce Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+"
  (stringVal (twoCodes 97 98)) (stringVal (oneCode 99))
#reduce badApply "+" (stringVal (twoCodes 97 98)) (stringVal (oneCode 99))

end OperationalBridgeCheck
