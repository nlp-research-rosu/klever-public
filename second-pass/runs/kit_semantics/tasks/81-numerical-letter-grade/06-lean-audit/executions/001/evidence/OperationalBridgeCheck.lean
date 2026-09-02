import Proof

open Klean81NumericalLetterGrade

/- The candidate returns false where the frozen MPY-INT rule says
   applyCmp("==", 7, 7) rewrites to 7 ==Int 7, i.e. true. -/
example :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
      "==" (SortVal.inj_SortInt 7) (SortVal.inj_SortInt 7) = false := by
  rfl

example : ((7 : SortInt) == 7) = true := by
  decide

example : _root_.«_==Int_» 7 7 = some true := by
  rfl

/- Likewise, the candidate returns false for the true MPY-INT comparison 2 > 1. -/
example :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
      ">" (SortVal.inj_SortInt 2) (SortVal.inj_SortInt 1) = false := by
  rfl

example : ((2 : SortInt) > 1) = true := by
  decide

example : _root_.«_>Int_» 2 1 = some true := by
  rfl

/- The intended guard is satisfiable, so the generated conjuncts themselves
   are exercised by concrete numeric values. -/
example :
    Proof.«isGradeNumber(_)_VERIFICATION_Bool_Val»
      (SortVal.inj_SortInt 7) = true := by
  native_decide

/- A counterfactual can change every off-obligation applyCmp result to true
   and still prove the fixed target, demonstrating that the target does not
   constrain the full operational symbol. -/
noncomputable def mutatedApplyCmp
    (op : SortString) (lhs rhs : SortVal) : SortBool :=
  if op = "==" then
    match rhs with
    | SortVal.inj_SortFloat f =>
        if Proof.«isGradeNumber(_)_VERIFICATION_Bool_Val» lhs = true then
          Proof.«gradeEq(_,_)_VERIFICATION_Bool_Val_Float» lhs f
        else true
    | _ => true
  else if op = ">" then
    match rhs with
    | SortVal.inj_SortFloat f =>
        if Proof.«isGradeNumber(_)_VERIFICATION_Bool_Val» lhs = true then
          Proof.«gradeGt(_,_)_VERIFICATION_Bool_Val_Float» lhs f
        else true
    | _ => true
  else true

theorem counterfactualStillProvesTarget :
    Lemmas.targetStatement
      mutatedApplyCmp
      Proof.«gradeEq(_,_)_VERIFICATION_Bool_Val_Float»
      Proof.«gradeGt(_,_)_VERIFICATION_Bool_Val_Float»
      Proof.«isGradeNumber(_)_VERIFICATION_Bool_Val» := by
  constructor
  · intro F V h
    change
      (if Proof.«isGradeNumber(_)_VERIFICATION_Bool_Val» V = true then
        Proof.«gradeEq(_,_)_VERIFICATION_Bool_Val_Float» V F
      else true) =
      Proof.«gradeEq(_,_)_VERIFICATION_Bool_Val_Float» V F
    rw [if_pos h]
  · intro F V h
    change
      (if Proof.«isGradeNumber(_)_VERIFICATION_Bool_Val» V = true then
        Proof.«gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V F
      else true) =
      Proof.«gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V F
    rw [if_pos h]
