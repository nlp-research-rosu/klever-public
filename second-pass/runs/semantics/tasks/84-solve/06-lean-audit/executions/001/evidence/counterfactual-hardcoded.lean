import Proof

open Proof.BuildIS

theorem hardCodedEmptySuffixWouldBeWrong (rest : SortIntSeq) :
    «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
              (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
                rest))))
        (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2)
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =
      some
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)) := by
  exact doSlice_drop_binary_prefix rest
