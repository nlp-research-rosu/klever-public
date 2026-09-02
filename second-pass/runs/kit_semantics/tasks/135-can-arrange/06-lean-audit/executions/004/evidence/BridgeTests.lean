import Proof

namespace AuditBridgeTests

open Proof

def intVal (value : SortInt) : SortVal := .inj_SortInt value
def boolVal (value : SortBool) : SortVal := .inj_SortBool value
def floatVal (value : SortFloat) : SortVal := .inj_SortFloat value

def codes : List SortInt → SortIntSeq
  | [] => SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | head :: tail => SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head (codes tail)

def strVal (value : List SortInt) : SortVal :=
  .inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (codes value))

def posInf : SortFloat := Float.ofBits 0x7ff0000000000000
def negInf : SortFloat := Float.ofBits 0xfff0000000000000
def quietNaN : SortFloat := Float.ofBits 0x7ff8000000000000

#eval ("int 2 >= 1", operationalOrderablePair (intVal 2) (intVal 1),
  operationalApplyCmp ">=" (intVal 2) (intVal 1),
  operationalOrderGe (intVal 2) (intVal 1))
#eval ("int 1 >= 2", operationalOrderablePair (intVal 1) (intVal 2),
  operationalApplyCmp ">=" (intVal 1) (intVal 2),
  operationalOrderGe (intVal 1) (intVal 2))
#eval ("true >= 2", operationalOrderablePair (boolVal true) (intVal 2),
  operationalApplyCmp ">=" (boolVal true) (intVal 2),
  operationalOrderGe (boolVal true) (intVal 2))
#eval ("false >= -1", operationalOrderablePair (boolVal false) (intVal (-1)),
  operationalApplyCmp ">=" (boolVal false) (intVal (-1)),
  operationalOrderGe (boolVal false) (intVal (-1)))
#eval ("2.5 >= 2", operationalOrderablePair (floatVal 2.5) (intVal 2),
  operationalApplyCmp ">=" (floatVal 2.5) (intVal 2),
  operationalOrderGe (floatVal 2.5) (intVal 2))
#eval ("2 >= 2.5", operationalOrderablePair (intVal 2) (floatVal 2.5),
  operationalApplyCmp ">=" (intVal 2) (floatVal 2.5),
  operationalOrderGe (intVal 2) (floatVal 2.5))
#eval ("NaN >= NaN (supplied-K not-lt behavior)",
  operationalOrderablePair (floatVal quietNaN) (floatVal quietNaN),
  operationalApplyCmp ">=" (floatVal quietNaN) (floatVal quietNaN),
  operationalOrderGe (floatVal quietNaN) (floatVal quietNaN))
#eval ("overflow-boundary int >= +inf (supplied-K rounding behavior)",
  operationalApplyCmp ">=" (intVal operationalIntFloatOverflowBoundary) (floatVal posInf),
  operationalOrderGe (intVal operationalIntFloatOverflowBoundary) (floatVal posInf))
#eval ("-inf >= negative overflow-boundary int (supplied-K rounding behavior)",
  operationalApplyCmp ">=" (floatVal negInf) (intVal (-operationalIntFloatOverflowBoundary)),
  operationalOrderGe (floatVal negInf) (intVal (-operationalIntFloatOverflowBoundary)))
#eval ("b >= a", operationalOrderablePair (strVal [98]) (strVal [97]),
  operationalApplyCmp ">=" (strVal [98]) (strVal [97]),
  operationalOrderGe (strVal [98]) (strVal [97]))
#eval ("int/string outside guarded domain",
  operationalOrderablePair (intVal 1) (strVal [97]),
  operationalApplyCmp ">=" (intVal 1) (strVal [97]),
  operationalOrderGe (intVal 1) (strVal [97]))

example : Klean135CanArrange.Lemmas.targetStatement
    «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    «orderGe(_,_)_VERIFICATION-BASE_Bool_Val_Val»
    «orderablePair(_,_)_VERIFICATION-BASE_Bool_Val_Val» := Proof.final

end AuditBridgeTests
