import Proof

open Klean4MeanAbsoluteDeviation

private def kOfVal (value : SortVal) : SortK :=
  SortK.kseq ((@inj SortVal SortKItem) value) SortK.dotk

private def floatValMatches (value : SortVal) (expected : SortFloat) : Bool :=
  match value with
  | SortVal.inj_SortFloat actual => actual == expected
  | _ => false

private def intValMatches (value : SortVal) (expected : SortInt) : Bool :=
  match value with
  | SortVal.inj_SortInt actual => actual == expected
  | _ => false

private def noneValMatches (value : SortVal) : Bool :=
  match value with
  | SortVal.«noneV_MPY-CORE_Val» => true
  | _ => false

private def twoCodeStringMatches (value : SortVal) : Bool :=
  match value with
  | SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 65
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 66
            SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) => true
  | _ => false

private def plusEquation
    (app : SortString → SortVal → SortVal → SortVal)
    (add : SortFloat → SortFloat → SortFloat)
    (project : SortVal → SortFloat)
    (accumulator : SortFloat)
    (value : SortVal) : Bool :=
  floatValMatches
    (app "+" (SortVal.inj_SortFloat accumulator) value)
    (add accumulator (project value))

private def subEquation
    (app : SortString → SortVal → SortVal → SortVal)
    (sub : SortFloat → SortFloat → SortFloat)
    (project : SortVal → SortFloat)
    (mean : SortFloat)
    (value : SortVal) : Bool :=
  floatValMatches
    (app "-" value (SortVal.inj_SortFloat mean))
    (sub (project value) mean)

private def badAddF (_ _ : SortFloat) : SortFloat := 0.0
private def badApplyBin (_ : SortString) (_ _ : SortVal) : SortVal :=
  SortVal.«noneV_MPY-CORE_Val»
private def badIsFloat (_ : SortK) : SortBool := true
private def badProjectFloat (_ : SortVal) : SortFloat := 0.0
private def badSubF (_ _ : SortFloat) : SortFloat := 0.0
private def badProject (_ : SortK) : Option SortFloat := none

private def value125 : SortVal := SortVal.inj_SortFloat 1.25
private def value225 : SortVal := SortVal.inj_SortFloat 2.25
private def value7 : SortVal := SortVal.inj_SortFloat 7.0
private def valueInt7 : SortVal := SortVal.inj_SortInt 7
private def kTwoItems : SortK :=
  SortK.kseq (SortKItem.inj_SortFloat 1.0)
    (SortK.kseq (SortKItem.inj_SortFloat 2.0) SortK.dotk)

private def codeA : SortVal :=
  SortVal.inj_SortStr
    (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 65
        SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))

private def codeB : SortVal :=
  SortVal.inj_SortStr
    (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 66
        SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))

#eval Proof.addF 1.5 2.25 == 3.75
#eval Proof.subF 3.5 1.25 == 2.25
#eval plusEquation Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» Proof.addF Proof.projectFloat 1.5 value225
#eval subEquation Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» Proof.subF Proof.projectFloat 1.25 value225
#eval intValMatches (Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" (SortVal.inj_SortInt 4) (SortVal.inj_SortInt 5)) 9
#eval intValMatches (Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "%" (SortVal.inj_SortInt (-7)) (SortVal.inj_SortInt 3)) 2
#eval twoCodeStringMatches (Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" codeA codeB)
#eval noneValMatches (Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "?" value125 value225)
#eval Proof.isFloat (kOfVal value7)
#eval !(Proof.isFloat (kOfVal valueInt7))
#eval !(Proof.isFloat kTwoItems)
#eval Proof.projectFloat value7 == 7.0
#eval Proof.projectFloat valueInt7 == 0.0
#eval (Proof.«project:Float?» (kOfVal value7)).isSome
#eval !(Proof.«project:Float?» (kOfVal valueInt7)).isSome
#eval !(Proof.«project:Float?» kTwoItems).isSome

#eval plusEquation Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» badAddF Proof.projectFloat 1.5 value225
#eval plusEquation badApplyBin Proof.addF Proof.projectFloat 1.5 value225
#eval (Proof.«project:Float?» (kOfVal valueInt7)).isSome == badIsFloat (kOfVal valueInt7)
#eval plusEquation Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» Proof.addF badProjectFloat 1.5 value225
#eval subEquation Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» badSubF Proof.projectFloat 1.25 value225
#eval (badProject (kOfVal value7)).isSome == Proof.isFloat (kOfVal value7)
