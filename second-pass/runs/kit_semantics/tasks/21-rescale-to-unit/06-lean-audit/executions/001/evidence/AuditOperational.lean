import Proof

open Proof

def isNoneV : SortVal → Bool
  | SortVal.«noneV_MPY-CORE_Val» => true
  | _ => false

def isIntVal : SortVal → Bool
  | SortVal.inj_SortInt _ => true
  | _ => false

def isFloatVal : SortVal → Bool
  | SortVal.inj_SortFloat _ => true
  | _ => false

def isSomeFloat : Option SortFloat → Bool
  | some _ => true
  | none => false

-- Source-rule domain witnesses.
#eval «definedProjectFloat(_)_VERIFICATION_Bool_Val»
  (SortVal.inj_SortFloat 3.5)
#eval «definedProjectFloat(_)_VERIFICATION_Bool_Val»
  (SortVal.inj_SortInt 3)
#eval isFloat
  (SortK.kseq (SortKItem.inj_SortFloat 3.5) SortK.dotk)
#eval isFloat
  (SortK.kseq (SortKItem.inj_SortInt 3) SortK.dotk)
#eval isSomeFloat
  («project:Float?»
    (SortK.kseq (SortKItem.inj_SortFloat 3.5) SortK.dotk))
#eval isSomeFloat
  («project:Float?»
    (SortK.kseq (SortKItem.inj_SortInt 3) SortK.dotk))
#eval isFloatVal
  («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
    "-"
    (SortVal.inj_SortFloat 7.0)
    (SortVal.inj_SortFloat 2.0))

-- Adversarial defined cases of the same frozen KORE applyBin symbol.
-- Fixed semantics has applyBin("+", 2, 3) => 2 +Int 3 and
-- applyBin("-", 2, 3) => 2 -Int 3.
#eval isNoneV
  («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
    "+"
    (SortVal.inj_SortInt 2)
    (SortVal.inj_SortInt 3))
#eval isIntVal
  («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
    "+"
    (SortVal.inj_SortInt 2)
    (SortVal.inj_SortInt 3))
#eval isNoneV
  («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
    "-"
    (SortVal.inj_SortInt 2)
    (SortVal.inj_SortInt 3))
