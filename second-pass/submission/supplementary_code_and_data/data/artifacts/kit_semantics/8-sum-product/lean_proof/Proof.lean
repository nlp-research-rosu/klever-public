import Klean8SumProduct.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0, rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (a b : SortBool) : SortBool := a && b
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (a b : SortInt) : SortInt := a + b
/- KORE symbol: Lbl'UndsStar'Int'Unds'; frozen source obligations: rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_*Int_» (a b : SortInt) : SortInt := a * b

private def boolAsInt : SortBool → SortInt
  | false => 0
  | true => 1

private def pyMod (a b : SortInt) : SortInt :=
  ((a % b) + b) % b

/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0, rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» :
    SortString → SortVal → SortVal → SortVal
  | "+", SortVal.inj_SortInt a, SortVal.inj_SortInt b =>
      SortVal.inj_SortInt (a + b)
  | "+", SortVal.inj_SortInt a, SortVal.inj_SortBool b =>
      SortVal.inj_SortInt (a + boolAsInt b)
  | "+", SortVal.inj_SortBool a, SortVal.inj_SortInt b =>
      SortVal.inj_SortInt (boolAsInt a + b)
  | "-", SortVal.inj_SortInt a, SortVal.inj_SortInt b =>
      SortVal.inj_SortInt (a - b)
  | "*", SortVal.inj_SortInt a, SortVal.inj_SortInt b =>
      SortVal.inj_SortInt (a * b)
  | "%", SortVal.inj_SortInt a, SortVal.inj_SortInt b =>
      SortVal.inj_SortInt (pyMod a b)
  | "//", SortVal.inj_SortInt a, SortVal.inj_SortInt b =>
      SortVal.inj_SortInt ((a - pyMod a b) / b)
  | "**", SortVal.inj_SortInt a, SortVal.inj_SortInt b =>
      if b ≥ 0 then SortVal.inj_SortInt (a ^ b.toNat)
      else SortVal.«noneV_MPY-CORE_Val»
  | "+", SortVal.inj_SortFloat a, SortVal.inj_SortFloat b =>
      SortVal.inj_SortFloat (a + b)
  | "-", SortVal.inj_SortFloat a, SortVal.inj_SortFloat b =>
      SortVal.inj_SortFloat (a - b)
  | "*", SortVal.inj_SortFloat a, SortVal.inj_SortFloat b =>
      SortVal.inj_SortFloat (a * b)
  | "/", SortVal.inj_SortFloat a, SortVal.inj_SortFloat b =>
      SortVal.inj_SortFloat (a / b)
  | "%", SortVal.inj_SortFloat a, SortVal.inj_SortFloat b =>
      SortVal.inj_SortFloat (a - Float.floor (a / b) * b)
  | "**", SortVal.inj_SortFloat a, SortVal.inj_SortFloat b =>
      SortVal.inj_SortFloat (a ^ b)
  | "/", SortVal.inj_SortInt a, SortVal.inj_SortInt b =>
      SortVal.inj_SortFloat (Float.ofInt a / Float.ofInt b)
  | "+", SortVal.inj_SortInt a, SortVal.inj_SortFloat b =>
      SortVal.inj_SortFloat (Float.ofInt a + b)
  | "+", SortVal.inj_SortFloat a, SortVal.inj_SortInt b =>
      SortVal.inj_SortFloat (a + Float.ofInt b)
  | "-", SortVal.inj_SortInt a, SortVal.inj_SortFloat b =>
      SortVal.inj_SortFloat (Float.ofInt a - b)
  | "-", SortVal.inj_SortFloat a, SortVal.inj_SortInt b =>
      SortVal.inj_SortFloat (a - Float.ofInt b)
  | "*", SortVal.inj_SortInt a, SortVal.inj_SortFloat b =>
      SortVal.inj_SortFloat (Float.ofInt a * b)
  | "*", SortVal.inj_SortFloat a, SortVal.inj_SortInt b =>
      SortVal.inj_SortFloat (a * Float.ofInt b)
  | "/", SortVal.inj_SortInt a, SortVal.inj_SortFloat b =>
      SortVal.inj_SortFloat (Float.ofInt a / b)
  | "/", SortVal.inj_SortFloat a, SortVal.inj_SortInt b =>
      SortVal.inj_SortFloat (a / Float.ofInt b)
  | "**", SortVal.inj_SortInt a, SortVal.inj_SortFloat b =>
      SortVal.inj_SortFloat (Float.ofInt a ^ b)
  | "**", SortVal.inj_SortFloat a, SortVal.inj_SortInt b =>
      SortVal.inj_SortFloat (a ^ Float.ofInt b)
  | _, _, _ => SortVal.«noneV_MPY-CORE_Val»

/- The final branch totalizes K's otherwise stuck operator applications.  The
   integer, Boolean-integer, float, and mixed numeric rules available in the
   generated value universe are represented above. -/

/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt i) SortK.dotk => some i
  | _ => none
/- KORE symbol: LblisInt; frozen source obligations: rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0, rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt (k : SortK) : SortBool := («project:Int?» k).isSome
/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION_Bool_Val» (v : SortVal) : SortBool :=
  isInt (SortK.kseq ((@inj SortVal SortKItem) v) SortK.dotk)
/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081, rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0, rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal (v : SortVal) : SortInt :=
  («project:Int?» (SortK.kseq ((@inj SortVal SortKItem) v) SortK.dotk)).getD 0

/- `getD` supplies Lean's required total value only where K's cast is stuck.
   Every verification rule that observes this function is guarded by `isInt`. -/

private def valIsInt : SortVal → SortBool
  | SortVal.inj_SortInt _ => true
  | _ => false

private theorem projectInt_of_injected_val (v : SortVal) :
    «project:Int?» (SortK.kseq ((@inj SortVal SortKItem) v) SortK.dotk) =
      match v with
      | SortVal.inj_SortInt i => some i
      | _ => none := by
  cases v <;> rfl

private theorem isInt_of_injected_val (v : SortVal) :
    isInt (SortK.kseq ((@inj SortVal SortKItem) v) SortK.dotk) =
      valIsInt v := by
  rw [isInt, projectInt_of_injected_val]
  cases v <;> rfl

private theorem valIsInt_eq_true_iff (v : SortVal) :
    valIsInt v = true ↔ ∃ i, v = SortVal.inj_SortInt i := by
  cases v <;> simp [valIsInt]

theorem final :
    Klean8SumProduct.Lemmas.targetStatement _andBool_ «_+Int_» «_*Int_» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «definedProjectInt(_)_VERIFICATION_Bool_Val» isInt projectIntTotal «project:Int?» := by
  unfold Klean8SumProduct.Lemmas.targetStatement
  constructor
  · intro V
    simp [«definedProjectInt(_)_VERIFICATION_Bool_Val», isInt]
  constructor
  · intro V
    unfold projectIntTotal
    rw [projectInt_of_injected_val]
    rfl
  constructor
  · intro W V h
    rw [isInt_of_injected_val V, isInt_of_injected_val W] at h
    have hvw := Bool.and_eq_true_iff.mp h
    obtain ⟨i, rfl⟩ := (valIsInt_eq_true_iff V).mp hvw.1
    obtain ⟨j, rfl⟩ := (valIsInt_eq_true_iff W).mp hvw.2
    rfl
  · intro W V h
    rw [isInt_of_injected_val V, isInt_of_injected_val W] at h
    have hvw := Bool.and_eq_true_iff.mp h
    obtain ⟨i, rfl⟩ := (valIsInt_eq_true_iff V).mp hvw.1
    obtain ⟨j, rfl⟩ := (valIsInt_eq_true_iff W).mp hvw.2
    rfl

end Proof
