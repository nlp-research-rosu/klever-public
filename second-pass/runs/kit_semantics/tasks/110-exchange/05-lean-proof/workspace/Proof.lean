import Klean110Exchange.Lemmas
import Proof.Dispatch

namespace Proof

/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-f297fbc0d836c7026aa18875014896223d568b8e6387f7a05ff3ae9fb97cdc9a. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» :
    SortString → SortVal → SortVal → SortVal :=
  ProofModel.applyBin
/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-f297fbc0d836c7026aa18875014896223d568b8e6387f7a05ff3ae9fb97cdc9a. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» :
    SortString → SortVal → SortVal → SortBool :=
  ProofModel.applyCmp
/- KORE symbol: LbldefinedProjectBool'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val; frozen source obligations: rule-e1f0f7da39177f5e6e65ea0afce67a1341dc2b663fda1ad070a7a09dec8d1a06. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectBool(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool :=
  ProofModel.definedProjectBool
/- KORE symbol: LbldefinedProjectFloat'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val; frozen source obligations: rule-57727b2acd45f64e74f4c2582f643b13345834dfbe7bf3fe97580d59dcd8ba43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectFloat(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool :=
  ProofModel.definedProjectFloat
/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool :=
  ProofModel.definedProjectInt
/- KORE symbol: LblisNumberVal'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val; frozen source obligations: rule-f297fbc0d836c7026aa18875014896223d568b8e6387f7a05ff3ae9fb97cdc9a, rule-4ec80ff33d0e12af220ea89dbd4fcab9751644a447d6e835ae4463ed423b09a0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isNumberVal(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool :=
  ProofModel.isNumberVal
/- KORE symbol: LblnumberEven'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val; frozen source obligations: rule-f297fbc0d836c7026aa18875014896223d568b8e6387f7a05ff3ae9fb97cdc9a. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «numberEven(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool :=
  ProofModel.numberEven
/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-4ec80ff33d0e12af220ea89dbd4fcab9751644a447d6e835ae4463ed423b09a0. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val?» :
    SortString → SortVal → SortVal → Option SortVal :=
  ProofModel.applyBin?
/- KORE symbol: Lblproject'Coln'Bool; frozen source obligations: rule-e1f0f7da39177f5e6e65ea0afce67a1341dc2b663fda1ad070a7a09dec8d1a06. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Bool?» : SortK → Option SortBool := ProofModel.projectBool?
/- KORE symbol: Lblproject'Coln'Float; frozen source obligations: rule-57727b2acd45f64e74f4c2582f643b13345834dfbe7bf3fe97580d59dcd8ba43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Float?» : SortK → Option SortFloat := ProofModel.projectFloat?
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» : SortK → Option SortInt := ProofModel.projectInt?

theorem final :
    Klean110Exchange.Lemmas.targetStatement «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «definedProjectBool(_)_VERIFICATION-BASE_Bool_Val» «definedProjectFloat(_)_VERIFICATION-BASE_Bool_Val» «definedProjectInt(_)_VERIFICATION-BASE_Bool_Val» «isNumberVal(_)_VERIFICATION-BASE_Bool_Val» «numberEven(_)_VERIFICATION-BASE_Bool_Val» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val?» «project:Bool?» «project:Float?» «project:Int?» := by
  unfold Klean110Exchange.Lemmas.targetStatement
  constructor
  · intro value
    cases value <;>
      simp [«project:Int?», «definedProjectInt(_)_VERIFICATION-BASE_Bool_Val»,
        ProofModel.projectInt?, ProofModel.definedProjectInt, inj]
  constructor
  · intro value
    cases value <;>
      simp [«project:Bool?», «definedProjectBool(_)_VERIFICATION-BASE_Bool_Val»,
        ProofModel.projectBool?, ProofModel.definedProjectBool, inj]
  constructor
  · intro value
    cases value <;>
      simp [«project:Float?», «definedProjectFloat(_)_VERIFICATION-BASE_Bool_Val»,
        ProofModel.projectFloat?, ProofModel.definedProjectFloat, inj]
  constructor
  · intro value numeric
    cases value <;>
      simp [«isNumberVal(_)_VERIFICATION-BASE_Bool_Val»,
        «numberEven(_)_VERIFICATION-BASE_Bool_Val»,
        «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
        «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        ProofModel.isNumberVal, ProofModel.numberEven, ProofModel.intEven,
        ProofModel.applyBin, ProofModel.applyBin?, ProofModel.applyCmp,
        ProofModel.applyCmp?, ProofModel.equality?, ProofModel.pyMod] at numeric ⊢
  · intro value numeric
    cases value <;>
      simp [«isNumberVal(_)_VERIFICATION-BASE_Bool_Val»,
        «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val?»,
        ProofModel.isNumberVal, ProofModel.applyBin?, ProofModel.pyMod] at numeric ⊢

end Proof
