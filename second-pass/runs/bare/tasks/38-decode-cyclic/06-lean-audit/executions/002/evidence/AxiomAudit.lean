import Proof

#check (Proof.final :
  Klean38DecodeCyclic.Lemmas.targetStatement
    Proof.«_<=Int_»
    Proof.«Map:update»
    Proof.«lengthString(_)_STRING-COMMON_Int_String»
    Proof.«substrString(_,_,_)_STRING-COMMON_String_String_Int_Int»)

#print axioms Proof.final
