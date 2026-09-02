import Proof

#print Proof.final

example :
    Klean28Concatenate.Lemmas.targetStatement
      Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      Proof.«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq»
      Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val» :=
  Proof.final
