import Proof

#check (Proof.final :
  Klean63Fibfib.Lemmas.targetStatement
    Proof.«_>=Int_»
    Proof.«_+Int_»
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»)
#print axioms Proof.final
