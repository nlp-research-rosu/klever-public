import Proof

open Proof.BuildIS

def oddTail : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» (-7)
    (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 100000
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)

example :
    «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
              (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
                oddTail))))
        (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =
      some
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» oddTail)) := by
  exact doSlice_drop_binary_prefix oddTail
