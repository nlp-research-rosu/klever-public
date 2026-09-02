import Proof

open Proof.BuildIS

theorem changingSliceStartWouldChangeMeaning (rest : SortIntSeq) :
    «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
              (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
                rest))))
        (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 1)
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =
      some
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rest)) := by
  rfl
