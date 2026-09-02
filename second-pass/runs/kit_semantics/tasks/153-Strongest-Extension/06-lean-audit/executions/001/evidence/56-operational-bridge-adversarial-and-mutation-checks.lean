import Proof

namespace OperationalBridgeAudit

def emptyCodes : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def oneCodes : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 65 emptyCodes

def emptyStr : SortStr :=
  SortStr.«str(_)_MPY-CORE_Str_IntSeq» emptyCodes

def oneStr : SortStr :=
  SortStr.«str(_)_MPY-CORE_Str_IntSeq» oneCodes

def oneVal : SortVal :=
  SortVal.inj_SortStr oneStr

def intVal : SortVal :=
  SortVal.inj_SortInt 7

def singletonOne : SortK :=
  SortK.kseq (SortKItem.inj_SortStr oneStr) SortK.dotk

/- Positive and negative operational witnesses for all six parameters. -/
example :
    Proof.«codesProject(_)_VERIFICATION-BASE_IntSeq_Val» oneVal = oneCodes := by
  rfl

example :
    Proof.«codesProject(_)_VERIFICATION-BASE_IntSeq_Val» intVal = emptyCodes := by
  rfl

example :
    Proof.«definedProjectStr(_)_VERIFICATION-BASE_Bool_Val» oneVal = true := by
  rfl

example :
    Proof.«definedProjectStr(_)_VERIFICATION-BASE_Bool_Val» intVal = false := by
  rfl

example :
    Proof.«isStringVal(_)_VERIFICATION-BASE_Bool_Val» oneVal = true := by
  rfl

example :
    Proof.«isStringVal(_)_VERIFICATION-BASE_Bool_Val» intVal = false := by
  rfl

example : Proof.«project:Str» singletonOne = oneStr := by
  rfl

example : Proof.«project:Str» SortK.dotk = emptyStr := by
  rfl

example : Proof.projectStrTotal oneVal = oneStr := by
  rfl

example : Proof.projectStrTotal intVal = emptyStr := by
  rfl

example : Proof.«project:Str?» singletonOne = some oneStr := by
  rfl

example : Proof.«project:Str?» SortK.dotk = none := by
  rfl

example :
    Proof.«project:Str?»
        (SortK.kseq (SortKItem.inj_SortStr oneStr)
          (SortK.kseq (SortKItem.inj_SortStr emptyStr) SortK.dotk)) =
      none := by
  rfl

/- Counterfactual constant/hard-coded mutations are rejected by the fixed target. -/
def badCodes : SortVal → SortIntSeq := fun _ => emptyCodes

example :
    ¬ Klean153StrongestExtension.Lemmas.targetStatement
        badCodes
        Proof.«definedProjectStr(_)_VERIFICATION-BASE_Bool_Val»
        Proof.«isStringVal(_)_VERIFICATION-BASE_Bool_Val»
        Proof.«project:Str»
        Proof.projectStrTotal
        Proof.«project:Str?» := by
  intro h
  have impossible := (h.2.2.2.2 oneVal).mpr (by rfl)
  simp [oneVal, oneStr, oneCodes, emptyCodes, badCodes] at impossible

def badDefined : SortVal → SortBool := fun _ => false

example :
    ¬ Klean153StrongestExtension.Lemmas.targetStatement
        Proof.«codesProject(_)_VERIFICATION-BASE_IntSeq_Val»
        badDefined
        Proof.«isStringVal(_)_VERIFICATION-BASE_Bool_Val»
        Proof.«project:Str»
        Proof.projectStrTotal
        Proof.«project:Str?» := by
  intro h
  have impossible := (h.1 oneVal).mp (by rfl)
  simp [badDefined] at impossible

def badIsString : SortVal → SortBool := fun _ => false

example :
    ¬ Klean153StrongestExtension.Lemmas.targetStatement
        Proof.«codesProject(_)_VERIFICATION-BASE_IntSeq_Val»
        Proof.«definedProjectStr(_)_VERIFICATION-BASE_Bool_Val»
        badIsString
        Proof.«project:Str»
        Proof.projectStrTotal
        Proof.«project:Str?» := by
  intro h
  have impossible := (h.2.2.2.1 oneVal).mp (by rfl)
  simp [badIsString] at impossible

def badProject : SortK → SortStr := fun _ => emptyStr

example :
    ¬ Klean153StrongestExtension.Lemmas.targetStatement
        Proof.«codesProject(_)_VERIFICATION-BASE_IntSeq_Val»
        Proof.«definedProjectStr(_)_VERIFICATION-BASE_Bool_Val»
        Proof.«isStringVal(_)_VERIFICATION-BASE_Bool_Val»
        badProject
        Proof.projectStrTotal
        Proof.«project:Str?» := by
  intro h
  have impossible := h.2.1 oneVal (by rfl)
  simp [oneVal, oneStr, oneCodes, emptyStr, emptyCodes, badProject,
    Proof.projectStrTotal] at impossible

def badProjectTotal : SortVal → SortStr := fun _ => emptyStr

example :
    ¬ Klean153StrongestExtension.Lemmas.targetStatement
        Proof.«codesProject(_)_VERIFICATION-BASE_IntSeq_Val»
        Proof.«definedProjectStr(_)_VERIFICATION-BASE_Bool_Val»
        Proof.«isStringVal(_)_VERIFICATION-BASE_Bool_Val»
        Proof.«project:Str»
        badProjectTotal
        Proof.«project:Str?» := by
  intro h
  have impossible := (h.2.2.2.1 oneVal).mpr (by rfl)
  simp [oneVal, oneStr, oneCodes, emptyStr, emptyCodes, badProjectTotal] at impossible

def badProjectPartial : SortK → Option SortStr := fun _ => none

example :
    ¬ Klean153StrongestExtension.Lemmas.targetStatement
        Proof.«codesProject(_)_VERIFICATION-BASE_IntSeq_Val»
        Proof.«definedProjectStr(_)_VERIFICATION-BASE_Bool_Val»
        Proof.«isStringVal(_)_VERIFICATION-BASE_Bool_Val»
        Proof.«project:Str»
        Proof.projectStrTotal
        badProjectPartial := by
  intro h
  have impossible := (h.1 oneVal).mpr ⟨by rfl, trivial⟩
  simp [badProjectPartial] at impossible

end OperationalBridgeAudit
