import Klean153StrongestExtension.Lemmas

namespace Proof

/- The frozen K functions `codesProject` and `projectStrTotal` have evaluators
   only on `Str` values.  The empty payload below is therefore used solely to
   totalize their Lean codomains off that guarded domain; every `Str` input is
   projected to its original constructor payload.  Likewise, `project:Str?`
   is the actual partial singleton-K projection, while `project:Str` uses the
   same off-domain totalization required by its generated Lean type. -/

/- KORE symbol: LblcodesProject'LParUndsRParUnds'VERIFICATION-BASE'Unds'IntSeq'Unds'Val; frozen source obligations: rule-10e1728036a93b9cdbc0c9743281a9e89436ffbf8433c0b87d6741769b463133. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «codesProject(_)_VERIFICATION-BASE_IntSeq_Val» : SortVal → SortIntSeq
  | SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes) => codes
  | _ => SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
/- KORE symbol: LbldefinedProjectStr'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val; frozen source obligations: rule-5d8f9b167e5284a82cd2a8ee7541fd69dfe8a2bfa3b401b3e610658fe9b05de3, rule-db9d27e9548a05d29d1ed50dae5699e3007e66b4be241553668c21d60b3a10ae. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectStr(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortStr _ => true
  | _ => false
/- KORE symbol: LblisStringVal'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val; frozen source obligations: rule-334fd615c749b4780fa187ec0618b959d5589b042350fb2e8ff133c457d4d2f1, rule-10e1728036a93b9cdbc0c9743281a9e89436ffbf8433c0b87d6741769b463133. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isStringVal(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortStr _ => true
  | _ => false
/- KORE symbol: Lblproject'Coln'Str; frozen source obligations: rule-db9d27e9548a05d29d1ed50dae5699e3007e66b4be241553668c21d60b3a10ae. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Str» : SortK → SortStr
  | SortK.kseq (SortKItem.inj_SortStr value) SortK.dotk => value
  | _ =>
      SortStr.«str(_)_MPY-CORE_Str_IntSeq»
        SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
/- KORE symbol: LblprojectStrTotal; frozen source obligations: rule-db9d27e9548a05d29d1ed50dae5699e3007e66b4be241553668c21d60b3a10ae, rule-f85e27b93f985712e161e1d9f93c9edc4bb9b998f80b67e076ae37e57255f5e0, rule-334fd615c749b4780fa187ec0618b959d5589b042350fb2e8ff133c457d4d2f1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectStrTotal : SortVal → SortStr
  | SortVal.inj_SortStr value => value
  | _ =>
      SortStr.«str(_)_MPY-CORE_Str_IntSeq»
        SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
/- KORE symbol: Lblproject'Coln'Str; frozen source obligations: rule-5d8f9b167e5284a82cd2a8ee7541fd69dfe8a2bfa3b401b3e610658fe9b05de3. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Str?» : SortK → Option SortStr
  | SortK.kseq (SortKItem.inj_SortStr value) SortK.dotk => some value
  | _ => none

theorem final :
    Klean153StrongestExtension.Lemmas.targetStatement «codesProject(_)_VERIFICATION-BASE_IntSeq_Val» «definedProjectStr(_)_VERIFICATION-BASE_Bool_Val» «isStringVal(_)_VERIFICATION-BASE_Bool_Val» «project:Str» projectStrTotal «project:Str?» := by
  unfold Klean153StrongestExtension.Lemmas.targetStatement
  constructor
  · intro V
    cases V <;>
      simp [
        inj,
        «project:Str?»,
        «definedProjectStr(_)_VERIFICATION-BASE_Bool_Val»
      ]
  constructor
  · intro V h
    cases V <;>
      simp_all [
        inj,
        «project:Str»,
        projectStrTotal,
        «definedProjectStr(_)_VERIFICATION-BASE_Bool_Val»
      ]
  constructor
  · intro V
    cases V <;> rfl
  constructor
  · intro V
    cases V <;>
      simp [
        projectStrTotal,
        «isStringVal(_)_VERIFICATION-BASE_Bool_Val»
      ]
  · intro V
    cases V <;>
      simp [
        «codesProject(_)_VERIFICATION-BASE_IntSeq_Val»,
        «isStringVal(_)_VERIFICATION-BASE_Bool_Val»
      ]

end Proof
