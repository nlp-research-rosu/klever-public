import Proof

namespace AuditCounterfactual

def falseIsFloat (_ : SortK) : SortBool := false

theorem targetStillProvableWithFalseIsFloat :
    Klean21RescaleToUnit.Lemmas.targetStatement
      Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      Proof.«definedProjectFloat(_)_VERIFICATION_Bool_Val»
      falseIsFloat
      Proof.projectFloatTotal
      Proof.subF
      Proof.«project:Float?» := by
  unfold Klean21RescaleToUnit.Lemmas.targetStatement
  constructor
  · exact Proof.final.1
  · intro F V h
    simp [falseIsFloat] at h

def falseDefinedProjectFloat (_ : SortVal) : SortBool := false
def noFloatProjection (_ : SortK) : Option SortFloat := none

theorem targetStillProvableWithFalseDomainBridge :
    Klean21RescaleToUnit.Lemmas.targetStatement
      Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      falseDefinedProjectFloat
      Proof.isFloat
      Proof.projectFloatTotal
      Proof.subF
      noFloatProjection := by
  unfold Klean21RescaleToUnit.Lemmas.targetStatement
  constructor
  · intro V
    simp [falseDefinedProjectFloat, noFloatProjection]
  · exact Proof.final.2

end AuditCounterfactual
