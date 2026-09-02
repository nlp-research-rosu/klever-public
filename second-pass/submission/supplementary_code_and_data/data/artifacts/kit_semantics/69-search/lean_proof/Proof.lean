import Proof.Operational

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-884f162b67149e88e7eecc28af46f50766a05e73cff70c9f7e167c33b1409e7d, rule-ffcf407de56764af73a323c60852665b87709ae760e0a275c8dacf75d96c5f02, rule-3e1ce8e4b12d8d2bae33238dc22c1575ab618c72afa918828d490765e79c8c2c, rule-45c3bb147f4e28b3f60623a84ce2306b2a8b697607e4388f59b32c4585d29c66. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (left right : SortBool) : SortBool := left && right
/- KORE symbol: Lbl'Unds-GT-'Int'Unds'; frozen source obligations: rule-3e1ce8e4b12d8d2bae33238dc22c1575ab618c72afa918828d490765e79c8c2c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>Int_» (left right : SortInt) : SortBool := decide (left > right)
/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-ffcf407de56764af73a323c60852665b87709ae760e0a275c8dacf75d96c5f02. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>=Int_» (left right : SortInt) : SortBool := decide (left ≥ right)
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-884f162b67149e88e7eecc28af46f50766a05e73cff70c9f7e167c33b1409e7d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (left right : SortInt) : SortBool := decide (left = right)
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-45c3bb147f4e28b3f60623a84ce2306b2a8b697607e4388f59b32c4585d29c66. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (left right : SortInt) : SortInt := left + right
/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-45c3bb147f4e28b3f60623a84ce2306b2a8b697607e4388f59b32c4585d29c66. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
    (operator : SortString) (left right : SortVal) : SortVal :=
  match left, right with
  | SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      (Operational.frozenIntIntBin operator leftInt rightInt).getD
        SortVal.«noneV_MPY-CORE_Val»
  | SortVal.inj_SortInt leftInt, SortVal.inj_SortBool rightBool =>
      if operator = "+" then
        SortVal.inj_SortInt (leftInt + if rightBool then 1 else 0)
      else
        SortVal.«noneV_MPY-CORE_Val»
  | SortVal.inj_SortBool leftBool, SortVal.inj_SortInt rightInt =>
      if operator = "+" then
        SortVal.inj_SortInt ((if leftBool then 1 else 0) + rightInt)
      else
        SortVal.«noneV_MPY-CORE_Val»
  | SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      (Operational.frozenFloatFloatBin operator leftFloat rightFloat).getD
        SortVal.«noneV_MPY-CORE_Val»
  | SortVal.inj_SortInt leftInt, SortVal.inj_SortFloat rightFloat =>
      (Operational.frozenIntFloatBin operator leftInt rightFloat).getD
        SortVal.«noneV_MPY-CORE_Val»
  | SortVal.inj_SortFloat leftFloat, SortVal.inj_SortInt rightInt =>
      (Operational.frozenFloatIntBin operator leftFloat rightInt).getD
        SortVal.«noneV_MPY-CORE_Val»
  | _, _ => SortVal.«noneV_MPY-CORE_Val»
/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-884f162b67149e88e7eecc28af46f50766a05e73cff70c9f7e167c33b1409e7d, rule-ffcf407de56764af73a323c60852665b87709ae760e0a275c8dacf75d96c5f02, rule-3e1ce8e4b12d8d2bae33238dc22c1575ab618c72afa918828d490765e79c8c2c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    (operator : SortString) (left right : SortVal) : SortBool :=
  match left, right with
  | SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      (Operational.frozenIntIntCmp operator leftInt rightInt).getD false
  | SortVal.inj_SortBool leftBool, SortVal.inj_SortBool rightBool =>
      if operator = "==" then leftBool == rightBool
      else if operator = "!=" then leftBool != rightBool
      else false
  | SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      (Operational.frozenFloatFloatCmp operator leftFloat rightFloat).getD false
  | SortVal.inj_SortInt leftInt, SortVal.inj_SortFloat rightFloat =>
      (Operational.frozenIntFloatCmp operator leftInt rightFloat).getD false
  | SortVal.inj_SortFloat leftFloat, SortVal.inj_SortInt rightInt =>
      (Operational.frozenFloatIntCmp operator leftFloat rightInt).getD false
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» leftValues),
      SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
      if operator = "==" then Operational.frozenTermEq leftValues rightValues
      else if operator = "!=" then !Operational.frozenTermEq leftValues rightValues
      else false
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» leftValues),
      SortVal.inj_SortIterable
        (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
      if operator = "==" then Operational.frozenTermEq leftValues rightValues
      else if operator = "!=" then !Operational.frozenTermEq leftValues rightValues
      else false
  | SortVal.«setV(_)_MPY-SET_Val_IntSeq» leftCodes,
      SortVal.«setV(_)_MPY-SET_Val_IntSeq» rightCodes =>
      if operator = "==" then Operational.frozenSetEq leftCodes rightCodes
      else false
  | SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» leftKeys leftValues,
      SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» rightKeys rightValues =>
      if operator = "==" then
        Operational.frozenDictEq leftKeys leftValues rightKeys rightValues
      else
        false
  | _, SortVal.«noneV_MPY-CORE_Val» =>
      if operator = "==" || operator = "is" then
        Operational.frozenTermEq left SortVal.«noneV_MPY-CORE_Val»
      else if operator = "!=" || operator = "is not" then
        !Operational.frozenTermEq left SortVal.«noneV_MPY-CORE_Val»
      else
        false
  | _, _ => false
/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION_Bool_Val» (value : SortVal) : SortBool :=
  match value with
  | SortVal.inj_SortInt _ => true
  | _ => false
/- KORE symbol: LblisIntVal'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-884f162b67149e88e7eecc28af46f50766a05e73cff70c9f7e167c33b1409e7d, rule-ffcf407de56764af73a323c60852665b87709ae760e0a275c8dacf75d96c5f02, rule-3e1ce8e4b12d8d2bae33238dc22c1575ab618c72afa918828d490765e79c8c2c, rule-45c3bb147f4e28b3f60623a84ce2306b2a8b697607e4388f59b32c4585d29c66. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isIntVal(_)_VERIFICATION_Bool_Val» (value : SortVal) : SortBool :=
  match value with
  | SortVal.inj_SortInt _ => true
  | _ => false
/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-884f162b67149e88e7eecc28af46f50766a05e73cff70c9f7e167c33b1409e7d, rule-ffcf407de56764af73a323c60852665b87709ae760e0a275c8dacf75d96c5f02, rule-3e1ce8e4b12d8d2bae33238dc22c1575ab618c72afa918828d490765e79c8c2c, rule-45c3bb147f4e28b3f60623a84ce2306b2a8b697607e4388f59b32c4585d29c66. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal (value : SortVal) : SortInt :=
  match value with
  | SortVal.inj_SortInt integer => integer
  | _ => 0
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt integer) SortK.dotk => some integer
  | _ => none

theorem final :
    Klean69Search.Lemmas.targetStatement _andBool_ «_>Int_» «_>=Int_» «_==Int_» «_+Int_» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «definedProjectInt(_)_VERIFICATION_Bool_Val» «isIntVal(_)_VERIFICATION_Bool_Val» projectIntTotal «project:Int?» := by
  unfold Klean69Search.Lemmas.targetStatement
  constructor
  · intro value
    cases value <;>
      simp [
        «project:Int?»,
        «definedProjectInt(_)_VERIFICATION_Bool_Val»,
        inj
      ]
  constructor
  · intro right left guard
    cases left <;> cases right <;>
      simp [
        _andBool_,
        «isIntVal(_)_VERIFICATION_Bool_Val»,
        «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        Operational.frozenIntIntCmp,
        «_==Int_»,
        projectIntTotal
      ] at guard ⊢
  constructor
  · intro right left guard
    cases left <;> cases right <;>
      simp [
        _andBool_,
        «isIntVal(_)_VERIFICATION_Bool_Val»,
        «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        Operational.frozenIntIntCmp,
        «_>=Int_»,
        projectIntTotal
      ] at guard ⊢
  constructor
  · intro right left guard
    cases left <;> cases right <;>
      simp [
        _andBool_,
        «isIntVal(_)_VERIFICATION_Bool_Val»,
        «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        Operational.frozenIntIntCmp,
        «_>Int_»,
        projectIntTotal
      ] at guard ⊢
  · intro right left guard
    cases left <;> cases right <;>
      simp [
        _andBool_,
        «isIntVal(_)_VERIFICATION_Bool_Val»,
        «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
        Operational.frozenIntIntBin,
        «_+Int_»,
        projectIntTotal
      ] at guard ⊢

end Proof
