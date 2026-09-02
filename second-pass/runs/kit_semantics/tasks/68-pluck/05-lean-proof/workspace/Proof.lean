import Klean68Pluck.Lemmas

namespace Proof

/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-5a57a342f46c274d8d94d5f1c7eda4683981fbe24087e787e4a8ce7782c03167. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (left right : SortInt) : SortInt :=
  left + right

private def operationalBoolAsInt (value : SortBool) : SortInt :=
  if value then 1 else 0

private def operationalPyMod (left right : SortInt) : SortInt :=
  Int.tmod (Int.tmod left right + right) right

private def operationalFloorDiv (left right : SortInt) : SortInt :=
  Int.tdiv (left - operationalPyMod left right) right

private def operationalFloatMod (left right : SortFloat) : SortFloat :=
  left - Float.floor (left / right) * right

/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-5a57a342f46c274d8d94d5f1c7eda4683981fbe24087e787e4a8ce7782c03167. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
    (operator : SortString) (left right : SortVal) : SortVal :=
  match operator, left, right with
  -- MPY-INT
  | "+", .inj_SortInt leftInt, .inj_SortInt rightInt =>
      .inj_SortInt (leftInt + rightInt)
  | "+", .inj_SortInt leftInt, .inj_SortBool rightBool =>
      .inj_SortInt (leftInt + operationalBoolAsInt rightBool)
  | "+", .inj_SortBool leftBool, .inj_SortInt rightInt =>
      .inj_SortInt (operationalBoolAsInt leftBool + rightInt)
  | "-", .inj_SortInt leftInt, .inj_SortInt rightInt =>
      .inj_SortInt (leftInt - rightInt)
  | "*", .inj_SortInt leftInt, .inj_SortInt rightInt =>
      .inj_SortInt (leftInt * rightInt)
  | "%", .inj_SortInt leftInt, .inj_SortInt rightInt =>
      if rightInt = 0 then .«noneV_MPY-CORE_Val»
      else .inj_SortInt (operationalPyMod leftInt rightInt)
  | "//", .inj_SortInt leftInt, .inj_SortInt rightInt =>
      if rightInt = 0 then .«noneV_MPY-CORE_Val»
      else .inj_SortInt (operationalFloorDiv leftInt rightInt)
  | "**", .inj_SortInt leftInt, .inj_SortInt (.ofNat exponent) =>
      .inj_SortInt (Int.pow leftInt exponent)
  -- MPY-FLOAT: true division and homogeneous Float operations.
  | "/", .inj_SortInt leftInt, .inj_SortInt rightInt =>
      .inj_SortFloat (Float.ofInt leftInt / Float.ofInt rightInt)
  | "/", .inj_SortInt leftInt, .inj_SortFloat rightFloat =>
      .inj_SortFloat (Float.ofInt leftInt / rightFloat)
  | "%", .inj_SortFloat leftFloat, .inj_SortFloat rightFloat =>
      .inj_SortFloat (operationalFloatMod leftFloat rightFloat)
  | "-", .inj_SortFloat leftFloat, .inj_SortFloat rightFloat =>
      .inj_SortFloat (leftFloat - rightFloat)
  | "/", .inj_SortFloat leftFloat, .inj_SortFloat rightFloat =>
      .inj_SortFloat (leftFloat / rightFloat)
  | "+", .inj_SortFloat leftFloat, .inj_SortFloat rightFloat =>
      .inj_SortFloat (leftFloat + rightFloat)
  | "*", .inj_SortFloat leftFloat, .inj_SortFloat rightFloat =>
      .inj_SortFloat (leftFloat * rightFloat)
  | "**", .inj_SortFloat leftFloat, .inj_SortFloat rightFloat =>
      .inj_SortFloat (Float.pow leftFloat rightFloat)
  -- MPY-FLOAT: mixed Int/Float coercions.
  | "**", .inj_SortInt leftInt, .inj_SortFloat rightFloat =>
      .inj_SortFloat (Float.pow (Float.ofInt leftInt) rightFloat)
  | "**", .inj_SortFloat leftFloat, .inj_SortInt rightInt =>
      .inj_SortFloat (Float.pow leftFloat (Float.ofInt rightInt))
  | "-", .inj_SortInt leftInt, .inj_SortFloat rightFloat =>
      .inj_SortFloat (Float.ofInt leftInt - rightFloat)
  | "-", .inj_SortFloat leftFloat, .inj_SortInt rightInt =>
      .inj_SortFloat (leftFloat - Float.ofInt rightInt)
  | "+", .inj_SortInt leftInt, .inj_SortFloat rightFloat =>
      .inj_SortFloat (Float.ofInt leftInt + rightFloat)
  | "+", .inj_SortFloat leftFloat, .inj_SortInt rightInt =>
      .inj_SortFloat (leftFloat + Float.ofInt rightInt)
  | "*", .inj_SortInt leftInt, .inj_SortFloat rightFloat =>
      .inj_SortFloat (Float.ofInt leftInt * rightFloat)
  | "*", .inj_SortFloat leftFloat, .inj_SortInt rightInt =>
      .inj_SortFloat (leftFloat * Float.ofInt rightInt)
  | "/", .inj_SortFloat leftFloat, .inj_SortInt rightInt =>
      .inj_SortFloat (leftFloat / Float.ofInt rightInt)
  -- MPY-STR also defines str(IntSeq) + str(IntSeq), but the frozen generated
  -- SortVal/SortIterable in Base contains no constructor for str(IntSeq).
  -- Consequently that source-sort case has no inhabitant in this Lean model.
  | _, _, _ => .«noneV_MPY-CORE_Val»
/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43, rule-5a57a342f46c274d8d94d5f1c7eda4683981fbe24087e787e4a8ce7782c03167. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION_Bool_Val» : SortVal → SortBool
  | .inj_SortInt _ => true
  | _ => false
/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-5a57a342f46c274d8d94d5f1c7eda4683981fbe24087e787e4a8ce7782c03167. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal : SortVal → SortInt
  | .inj_SortInt value => value
  | _ => 0
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» : SortK → Option SortInt
  | .kseq (.inj_SortInt value) .dotk => some value
  | _ => none

theorem final :
    Klean68Pluck.Lemmas.targetStatement «_+Int_» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «definedProjectInt(_)_VERIFICATION_Bool_Val» projectIntTotal «project:Int?» := by
  constructor
  · intro value
    cases value <;>
      exact ⟨(fun isSome => ⟨isSome, True.intro⟩), (fun isDefined => isDefined.1)⟩
  · intro integer value isDefined
    cases value <;> cases isDefined <;> rfl

end Proof
