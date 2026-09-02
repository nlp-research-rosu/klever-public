import Proof

#check (Proof.final :
  Klean33SortThird.Lemmas.targetStatement
    Proof.«_<=Int_»
    Proof.«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq»
    Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
    Proof.«vsLen(_)_MPY-CORE_Int_ValSeq»)

#print axioms Proof.final
