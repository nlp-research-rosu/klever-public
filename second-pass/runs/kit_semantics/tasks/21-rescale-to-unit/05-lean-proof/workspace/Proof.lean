import Klean21RescaleToUnit.Lemmas

namespace Proof

/- `pyMod` in MPY-INT is `((left %Int right) +Int right) %Int right`.
   The K term is stuck at a zero divisor, represented here by `none`. -/
private def operationalPyMod? (left right : SortInt) : Option SortInt :=
  if right == 0 then
    none
  else
    some (Int.emod (Int.emod left right + right) right)

/- Python floor division is defined by MPY-INT from the same remainder. -/
private def operationalFloorDiv? (left right : SortInt) : Option SortInt := do
  let remainder ← operationalPyMod? left right
  pure (Int.tdiv (left - remainder) right)

private def operationalBoolInt (value : SortBool) : SortInt :=
  if value then 1 else 0

/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-dc58f41e482527dda6d5bd7e29f533ee71f5356475fa5bfad6f9142925059957. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» :
    SortString → SortVal → SortVal → SortVal
  -- MPY-INT.
  | "+", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      SortVal.inj_SortInt (left + right)
  | "+", SortVal.inj_SortInt left, SortVal.inj_SortBool right =>
      SortVal.inj_SortInt (left + operationalBoolInt right)
  | "+", SortVal.inj_SortBool left, SortVal.inj_SortInt right =>
      SortVal.inj_SortInt (operationalBoolInt left + right)
  | "-", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      SortVal.inj_SortInt (left - right)
  | "*", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      SortVal.inj_SortInt (left * right)
  | "%", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      match operationalPyMod? left right with
      | some result => SortVal.inj_SortInt result
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "//", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      match operationalFloorDiv? left right with
      | some result => SortVal.inj_SortInt result
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "**", SortVal.inj_SortInt left, SortVal.inj_SortInt (Int.ofNat exponent) =>
      SortVal.inj_SortInt (Int.pow left exponent)

  -- MPY-FLOAT homogeneous arithmetic and Python's floor-based float modulus.
  | "/", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (Float.div (Float.ofInt left) (Float.ofInt right))
  | "%", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat
        (Float.sub left (Float.mul (Float.floor (Float.div left right)) right))
  | "-", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.sub left right)
  | "/", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.div left right)
  | "+", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.add left right)
  | "*", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.mul left right)
  | "**", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.pow left right)

  -- MPY-FLOAT mixed arithmetic; `intToF` is IEEE-754 conversion.
  | "/", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.div (Float.ofInt left) right)
  | "/", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (Float.div left (Float.ofInt right))
  | "**", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.pow (Float.ofInt left) right)
  | "**", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (Float.pow left (Float.ofInt right))
  | "-", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.sub (Float.ofInt left) right)
  | "-", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (Float.sub left (Float.ofInt right))
  | "+", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.add (Float.ofInt left) right)
  | "+", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (Float.add left (Float.ofInt right))
  | "*", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.mul (Float.ofInt left) right)
  | "*", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (Float.mul left (Float.ofInt right))

  -- No frozen applyBin equation matches any remaining representable triple.
  | _, _, _ => SortVal.«noneV_MPY-CORE_Val»
/- KORE symbol: LbldefinedProjectFloat'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-57727b2acd45f64e74f4c2582f643b13345834dfbe7bf3fe97580d59dcd8ba43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectFloat(_)_VERIFICATION_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortFloat _ => true
  | _ => false
/- KORE symbol: LblisFloat; frozen source obligations: rule-dc58f41e482527dda6d5bd7e29f533ee71f5356475fa5bfad6f9142925059957. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isFloat : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortFloat _) SortK.dotk => true
  | _ => false
/- KORE symbol: LblprojectFloatTotal; frozen source obligations: rule-dc58f41e482527dda6d5bd7e29f533ee71f5356475fa5bfad6f9142925059957. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectFloatTotal : SortVal → SortFloat
  | SortVal.inj_SortFloat value => value
  | _ => 0.0
/- KORE symbol: LblsubF; frozen source obligations: rule-dc58f41e482527dda6d5bd7e29f533ee71f5356475fa5bfad6f9142925059957. Replace this stub with its honest total meaning from the frozen K semantics. -/
def subF (left right : SortFloat) : SortFloat := Float.sub left right
/- KORE symbol: Lblproject'Coln'Float; frozen source obligations: rule-57727b2acd45f64e74f4c2582f643b13345834dfbe7bf3fe97580d59dcd8ba43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Float?» : SortK → Option SortFloat
  | SortK.kseq (SortKItem.inj_SortFloat value) SortK.dotk => some value
  | _ => none

theorem final :
    Klean21RescaleToUnit.Lemmas.targetStatement «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «definedProjectFloat(_)_VERIFICATION_Bool_Val» isFloat projectFloatTotal subF «project:Float?» := by
  unfold Klean21RescaleToUnit.Lemmas.targetStatement
  constructor
  · intro V
    cases V <;>
      simp [inj, «project:Float?», «definedProjectFloat(_)_VERIFICATION_Bool_Val»]
  · intro F V h
    cases V <;> simp [inj, isFloat] at h
    rfl

end Proof
