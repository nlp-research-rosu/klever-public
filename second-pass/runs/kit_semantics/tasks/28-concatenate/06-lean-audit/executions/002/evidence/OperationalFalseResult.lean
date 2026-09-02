import Proof

open SortIntSeq SortStr SortVal

private def nilCodes : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

private def oneCode (x : Int) : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x nilCodes

private def stringVal (codes : SortIntSeq) : SortVal :=
  SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes)

-- Deliberately false: concatenating "a" and "b" does not produce "ba".
example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+"
        (stringVal (oneCode 97)) (stringVal (oneCode 98)) =
      stringVal
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 (oneCode 97)) := by
  rfl
