import Proof

namespace OperationalBridgeAudit

def emptyCodes : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def emptyString : SortVal :=
  SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» emptyCodes)

def noneValue : SortVal :=
  SortVal.«noneV_MPY-CORE_Val»

#eval Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
  "==" (SortVal.inj_SortBool true) (SortVal.inj_SortBool true)

#eval Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
  "==" emptyString emptyString

#eval Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
  "==" noneValue noneValue

example :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
      "==" (SortVal.inj_SortBool true) (SortVal.inj_SortBool true) =
      false := by
  rfl

example :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
      "==" emptyString emptyString = false := by
  rfl

example :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
      "==" noneValue noneValue = false := by
  rfl

end OperationalBridgeAudit
