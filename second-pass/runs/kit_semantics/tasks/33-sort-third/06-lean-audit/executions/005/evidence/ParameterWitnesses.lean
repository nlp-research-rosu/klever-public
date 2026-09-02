import Proof

namespace ParameterWitnesses

def emptyVS : SortValSeq := SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

def intList : List Int → SortValSeq
  | [] => emptyVS
  | value :: rest =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortInt value) (intList rest)

def projectInts : SortValSeq → Option (List Int)
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some []
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortInt value) rest =>
      return value :: (← projectInts rest)
  | _ => none

#eval Proof.«_<=Int_» (-1) 0
#eval Proof.«_<=Int_» 1 0
#eval Proof.«vsLen(_)_MPY-CORE_Int_ValSeq» (intList [10, 20, 30])
#eval projectInts
  (Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
    (intList [1, 2]) (intList [3, 4]))
#eval projectInts
  (Proof.«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq»
    (intList [5, 6, 3, 4, 8, 9, 2]))

end ParameterWitnesses
