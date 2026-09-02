import Klean85Add.Lemmas

namespace Proof

/- K's `%Int` is partial at divisor zero.  The generated trust parameter is
   total, so zero is used only to totalize that unreachable/undefined case;
   for every defined divisor this is exactly the frozen pyMod recurrence. -/
private def pyModTotal (x y : SortInt) : SortInt :=
  if y = 0 then 0
  else Int.tmod (Int.tmod x y + y) y

/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x y : SortInt) : SortInt := x + y

/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» :
    SortString → SortVal → SortVal → SortVal
  | "+", SortVal.inj_SortInt x, SortVal.inj_SortInt y =>
      SortVal.inj_SortInt (x + y)
  | "+", SortVal.inj_SortInt x, SortVal.inj_SortBool y =>
      SortVal.inj_SortInt (x + if y then 1 else 0)
  | "+", SortVal.inj_SortBool x, SortVal.inj_SortInt y =>
      SortVal.inj_SortInt ((if x then 1 else 0) + y)
  | "-", SortVal.inj_SortInt x, SortVal.inj_SortInt y =>
      SortVal.inj_SortInt (x - y)
  | "*", SortVal.inj_SortInt x, SortVal.inj_SortInt y =>
      SortVal.inj_SortInt (x * y)
  | "%", SortVal.inj_SortInt x, SortVal.inj_SortInt y =>
      SortVal.inj_SortInt (pyModTotal x y)
  | "//", SortVal.inj_SortInt x, SortVal.inj_SortInt y =>
      if y = 0 then SortVal.«noneV_MPY-CORE_Val»
      else SortVal.inj_SortInt (Int.tdiv (x - pyModTotal x y) y)
  | "**", SortVal.inj_SortInt x, SortVal.inj_SortInt y =>
      if y < 0 then SortVal.«noneV_MPY-CORE_Val»
      else SortVal.inj_SortInt (Int.pow x y.toNat)
  | "/", SortVal.inj_SortInt x, SortVal.inj_SortInt y =>
      SortVal.inj_SortFloat (Float.ofInt x / Float.ofInt y)
  | "%", SortVal.inj_SortFloat x, SortVal.inj_SortFloat y =>
      SortVal.inj_SortFloat (x - Float.floor (x / y) * y)
  | "-", SortVal.inj_SortFloat x, SortVal.inj_SortFloat y =>
      SortVal.inj_SortFloat (x - y)
  | "/", SortVal.inj_SortFloat x, SortVal.inj_SortFloat y =>
      SortVal.inj_SortFloat (x / y)
  | "+", SortVal.inj_SortFloat x, SortVal.inj_SortFloat y =>
      SortVal.inj_SortFloat (x + y)
  | "*", SortVal.inj_SortFloat x, SortVal.inj_SortFloat y =>
      SortVal.inj_SortFloat (x * y)
  | "**", SortVal.inj_SortFloat x, SortVal.inj_SortFloat y =>
      SortVal.inj_SortFloat (x ^ y)
  | "**", SortVal.inj_SortInt x, SortVal.inj_SortFloat y =>
      SortVal.inj_SortFloat (Float.ofInt x ^ y)
  | "**", SortVal.inj_SortFloat x, SortVal.inj_SortInt y =>
      SortVal.inj_SortFloat (x ^ Float.ofInt y)
  | "-", SortVal.inj_SortInt x, SortVal.inj_SortFloat y =>
      SortVal.inj_SortFloat (Float.ofInt x - y)
  | "-", SortVal.inj_SortFloat x, SortVal.inj_SortInt y =>
      SortVal.inj_SortFloat (x - Float.ofInt y)
  | "+", SortVal.inj_SortInt x, SortVal.inj_SortFloat y =>
      SortVal.inj_SortFloat (Float.ofInt x + y)
  | "+", SortVal.inj_SortFloat x, SortVal.inj_SortInt y =>
      SortVal.inj_SortFloat (x + Float.ofInt y)
  | "*", SortVal.inj_SortInt x, SortVal.inj_SortFloat y =>
      SortVal.inj_SortFloat (Float.ofInt x * y)
  | "*", SortVal.inj_SortFloat x, SortVal.inj_SortInt y =>
      SortVal.inj_SortFloat (x * Float.ofInt y)
  | "/", SortVal.inj_SortInt x, SortVal.inj_SortFloat y =>
      SortVal.inj_SortFloat (Float.ofInt x / y)
  | "/", SortVal.inj_SortFloat x, SortVal.inj_SortInt y =>
      SortVal.inj_SortFloat (x / Float.ofInt y)
  | _, _, _ => SortVal.«noneV_MPY-CORE_Val»

/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortInt _ => true
  | _ => false

/- KORE symbol: LblisInt; frozen source obligations: rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false

/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal : SortVal → SortInt
  | SortVal.inj_SortInt i => i
  | _ => 0

/- KORE symbol: LblpyMod'LParUndsCommUndsRParUnds'MPY-INT'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x y : SortInt) : SortInt :=
  pyModTotal x y

/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt i) SortK.dotk => some i
  | _ => none

theorem final :
    Klean85Add.Lemmas.targetStatement «_+Int_» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» isInt projectIntTotal «pyMod(_,_)_MPY-INT_Int_Int_Int» «project:Int?» := by
  constructor
  · intro V
    cases V <;> simp [«project:Int?», «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val», inj]
  constructor
  · intro I V h
    cases V <;> simp [isInt, inj] at h
    rfl
  · intro V I h
    cases V <;> simp [isInt, inj] at h
    rfl

end Proof
