import Klean43PairsSumToZero.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-23e1a62d70fda3f264b9738a91911fc3875dc654e5e8dbd9c9e70004aee7e7b5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» (left right : SortInt) : SortInt :=
  left - right
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-4f41076b3b0eb2c1c718d3792b1c9158f8ae7d86ca361684ad8670d999140def. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (left right : SortInt) : SortBool :=
  decide (left = right)
/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-4f41076b3b0eb2c1c718d3792b1c9158f8ae7d86ca361684ad8670d999140def. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    (operator : SortString) (left right : SortVal) : SortBool :=
  match left, right with
  | SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      if operator = "==" then «_==Int_» leftInt rightInt
      else if operator = "!=" then decide (leftInt ≠ rightInt)
      else if operator = "<" then decide (leftInt < rightInt)
      else if operator = "<=" then decide (leftInt ≤ rightInt)
      else if operator = ">" then decide (leftInt > rightInt)
      else if operator = ">=" then decide (leftInt ≥ rightInt)
      else false
  | SortVal.inj_SortBool leftBool, SortVal.inj_SortBool rightBool =>
      if operator = "==" then decide (leftBool = rightBool)
      else if operator = "!=" then decide (leftBool ≠ rightBool)
      else false
  | SortVal.«noneV_MPY-CORE_Val», SortVal.«noneV_MPY-CORE_Val» =>
      operator = "==" || operator = "is"
  | _, _ => false
/- KORE symbol: LblapplyUn'LParUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val; frozen source obligations: rule-23e1a62d70fda3f264b9738a91911fc3875dc654e5e8dbd9c9e70004aee7e7b5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyUn(_,_)_MPY-CORE_Val_String_Val»
    (operator : SortString) (value : SortVal) : SortVal :=
  match value with
  | SortVal.inj_SortInt intValue =>
      if operator = "-" then SortVal.inj_SortInt («_-Int_» 0 intValue)
      else if operator = "not" then SortVal.inj_SortBool (decide (intValue = 0))
      else SortVal.«noneV_MPY-CORE_Val»
  | SortVal.inj_SortBool boolValue =>
      if operator = "not" then SortVal.inj_SortBool (!boolValue)
      else SortVal.«noneV_MPY-CORE_Val»
  | SortVal.«noneV_MPY-CORE_Val» =>
      if operator = "not" then SortVal.inj_SortBool true
      else SortVal.«noneV_MPY-CORE_Val»
  | _ => SortVal.«noneV_MPY-CORE_Val»
/- KORE symbol: LblintProj'LParUndsRParUnds'INT-PROJECTION'Unds'Int'Unds'Val; frozen source obligations: rule-4f41076b3b0eb2c1c718d3792b1c9158f8ae7d86ca361684ad8670d999140def, rule-23e1a62d70fda3f264b9738a91911fc3875dc654e5e8dbd9c9e70004aee7e7b5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «intProj(_)_INT-PROJECTION_Int_Val» (value : SortVal) : SortInt :=
  match value with
  | SortVal.inj_SortInt intValue => intValue
  | _ => 0
/- KORE symbol: LblisInt; frozen source obligations: rule-4f41076b3b0eb2c1c718d3792b1c9158f8ae7d86ca361684ad8670d999140def, rule-23e1a62d70fda3f264b9738a91911fc3875dc654e5e8dbd9c9e70004aee7e7b5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt (term : SortK) : SortBool :=
  match term with
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false

theorem final :
    Klean43PairsSumToZero.Lemmas.targetStatement «_-Int_» «_==Int_» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «applyUn(_,_)_MPY-CORE_Val_String_Val» «intProj(_)_INT-PROJECTION_Int_Val» isInt := by
  constructor
  · intro I V h
    cases V <;>
      simp_all [inj, isInt, «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        «intProj(_)_INT-PROJECTION_Int_Val», «_==Int_»]
  · intro V h
    cases V <;>
      simp_all [inj, isInt, «applyUn(_,_)_MPY-CORE_Val_String_Val»,
        «intProj(_)_INT-PROJECTION_Int_Val», «_-Int_»]

end Proof
