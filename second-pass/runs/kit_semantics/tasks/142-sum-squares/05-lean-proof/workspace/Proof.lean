import Klean142SumSquares.Lemmas

namespace Proof

/- The generated target represents a K value in a singleton K sequence.  The
   frozen `Val :> Int` projection succeeds exactly for the Int subsort. -/
def projectIntOption : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt value) SortK.dotk => some value
  | _ => none

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (left right : SortBool) : SortBool :=
  left && right

/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (left right : SortInt) : SortInt :=
  left + right

/- KORE symbol: Lbl'UndsStar'Int'Unds'; frozen source obligations: rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_*Int_» (left right : SortInt) : SortInt :=
  left * right

/- K's `pyMod` and `//` rules are undefined at a zero divisor.  Lean's
   `Int.fmod` and `Int.fdiv` use the same floor convention as those rules. -/
def intModResult (left right : SortInt) : Option SortVal :=
  if right = 0 then none
  else some (SortVal.inj_SortInt (Int.fmod left right))

def intFloorDivResult (left right : SortInt) : Option SortVal :=
  if right = 0 then none
  else some (SortVal.inj_SortInt (Int.fdiv left right))

/- The frozen integer-power rule is guarded by a nonnegative exponent. -/
def intPowResult (base exponent : SortInt) : Option SortVal :=
  if exponent < 0 then none
  else some (SortVal.inj_SortInt (base ^ exponent.toNat))

/- `Int2Float(_, 53, 11)` in the frozen semantics is IEEE-754 binary64
   conversion, which is exactly Lean's `Float.ofInt`. -/
def intToFloat (value : SortInt) : SortFloat :=
  Float.ofInt value

/- Python/K floating remainder is floor-based, not IEEE remainder. -/
def floatMod (left right : SortFloat) : SortFloat :=
  left - Float.floor (left / right) * right

/- This partial helper is the complete frozen `applyBin` result table over the
   value constructors present in the generated Klean `SortVal`: Int arithmetic,
   Bool-to-Int addition, Float arithmetic, true division, and all mixed
   Int/Float coercions.  `none` denotes precisely a K term with no applicable
   rule (including guarded Int operations outside their rule domain). -/
def applyBinResult
    (operator : SortString) (left right : SortVal) : Option SortVal :=
  match operator, left, right with
  | "+", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      some (SortVal.inj_SortInt (leftInt + rightInt))
  | "+", SortVal.inj_SortInt leftInt, SortVal.inj_SortBool rightBool =>
      some (SortVal.inj_SortInt (leftInt + if rightBool then 1 else 0))
  | "+", SortVal.inj_SortBool leftBool, SortVal.inj_SortInt rightInt =>
      some (SortVal.inj_SortInt ((if leftBool then 1 else 0) + rightInt))
  | "-", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      some (SortVal.inj_SortInt (leftInt - rightInt))
  | "*", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      some (SortVal.inj_SortInt (leftInt * rightInt))
  | "%", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      intModResult leftInt rightInt
  | "//", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      intFloorDivResult leftInt rightInt
  | "**", SortVal.inj_SortInt base, SortVal.inj_SortInt exponent =>
      intPowResult base exponent
  | "/", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      some (SortVal.inj_SortFloat (intToFloat leftInt / intToFloat rightInt))
  | "-", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      some (SortVal.inj_SortFloat (leftFloat - rightFloat))
  | "/", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      some (SortVal.inj_SortFloat (leftFloat / rightFloat))
  | "+", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      some (SortVal.inj_SortFloat (leftFloat + rightFloat))
  | "*", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      some (SortVal.inj_SortFloat (leftFloat * rightFloat))
  | "%", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      some (SortVal.inj_SortFloat (floatMod leftFloat rightFloat))
  | "**", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      some (SortVal.inj_SortFloat (Float.pow leftFloat rightFloat))
  | "**", SortVal.inj_SortInt leftInt, SortVal.inj_SortFloat rightFloat =>
      some (SortVal.inj_SortFloat (Float.pow (intToFloat leftInt) rightFloat))
  | "**", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortInt rightInt =>
      some (SortVal.inj_SortFloat (Float.pow leftFloat (intToFloat rightInt)))
  | "-", SortVal.inj_SortInt leftInt, SortVal.inj_SortFloat rightFloat =>
      some (SortVal.inj_SortFloat (intToFloat leftInt - rightFloat))
  | "-", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortInt rightInt =>
      some (SortVal.inj_SortFloat (leftFloat - intToFloat rightInt))
  | "+", SortVal.inj_SortInt leftInt, SortVal.inj_SortFloat rightFloat =>
      some (SortVal.inj_SortFloat (intToFloat leftInt + rightFloat))
  | "+", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortInt rightInt =>
      some (SortVal.inj_SortFloat (leftFloat + intToFloat rightInt))
  | "*", SortVal.inj_SortInt leftInt, SortVal.inj_SortFloat rightFloat =>
      some (SortVal.inj_SortFloat (intToFloat leftInt * rightFloat))
  | "*", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortInt rightInt =>
      some (SortVal.inj_SortFloat (leftFloat * intToFloat rightInt))
  | "/", SortVal.inj_SortInt leftInt, SortVal.inj_SortFloat rightFloat =>
      some (SortVal.inj_SortFloat (intToFloat leftInt / rightFloat))
  | "/", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortInt rightInt =>
      some (SortVal.inj_SortFloat (leftFloat / intToFloat rightInt))
  | _, _, _ => none

/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4, rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
    (operator : SortString) (left right : SortVal) : SortVal :=
  (applyBinResult operator left right).getD SortVal.«noneV_MPY-CORE_Val»

/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43, rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortInt _ => true
  | _ => false

/- KORE symbol: LblisInt; frozen source obligations: rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4, rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false

/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int» (term : SortK) : SortInt :=
  (projectIntOption term).getD 0

/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d, rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081, rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4, rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal : SortVal → SortInt
  | SortVal.inj_SortInt value => value
  | _ => 0

/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» (term : SortK) : Option SortInt :=
  projectIntOption term

theorem isInt_injected (value : SortVal) :
    isInt (SortK.kseq ((@inj SortVal SortKItem) value) SortK.dotk) =
      «definedProjectInt(_)_VERIFICATION_Bool_Val» value := by
  cases value <;> rfl

theorem exists_int_of_defined
    (value : SortVal)
    (defined :
      «definedProjectInt(_)_VERIFICATION_Bool_Val» value = true) :
    ∃ integer, value = SortVal.inj_SortInt integer := by
  cases value <;>
    simp [«definedProjectInt(_)_VERIFICATION_Bool_Val»] at defined
  exact ⟨_, rfl⟩

theorem final :
    Klean142SumSquares.Lemmas.targetStatement _andBool_ «_+Int_» «_*Int_» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «definedProjectInt(_)_VERIFICATION_Bool_Val» isInt «project:Int» projectIntTotal «project:Int?» := by
  unfold Klean142SumSquares.Lemmas.targetStatement
  constructor
  · intro V
    cases V <;>
      simp [«project:Int?», projectIntOption,
        «definedProjectInt(_)_VERIFICATION_Bool_Val», inj]
  constructor
  · intro V h
    cases V <;>
      simp [«definedProjectInt(_)_VERIFICATION_Bool_Val», «project:Int»,
        projectIntOption, projectIntTotal, inj] at h ⊢
  constructor
  · intro V
    cases V <;> simp [projectIntTotal]
  constructor
  · intro W V h
    simp only [isInt_injected] at h
    change
      («definedProjectInt(_)_VERIFICATION_Bool_Val» V &&
        «definedProjectInt(_)_VERIFICATION_Bool_Val» W) = true at h
    rw [Bool.and_eq_true] at h
    obtain ⟨VInt, rfl⟩ := exists_int_of_defined V h.1
    obtain ⟨WInt, rfl⟩ := exists_int_of_defined W h.2
    rfl
  · intro V I h
    simp only [isInt_injected] at h
    obtain ⟨VInt, rfl⟩ := exists_int_of_defined V h
    rfl

end Proof
