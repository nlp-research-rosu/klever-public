import Proof

namespace OperationalBridgeExpectedSemantics

def emptyCodes : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def emptyString : SortVal :=
  SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» emptyCodes)

def noneValue : SortVal :=
  SortVal.«noneV_MPY-CORE_Val»

-- These expected results are direct instances of the frozen rules in
-- bool.k:10, str.k:25, and float.k:154.
example :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
      "==" (SortVal.inj_SortBool true) (SortVal.inj_SortBool true) =
      true := by
  rfl

example :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
      "==" emptyString emptyString = true := by
  rfl

example :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
      "==" noneValue noneValue = true := by
  rfl

end OperationalBridgeExpectedSemantics
