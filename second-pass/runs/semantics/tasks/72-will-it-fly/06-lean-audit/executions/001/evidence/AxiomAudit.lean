import Proof

namespace Proof

#check (final :
  Klean72WillItFly.Lemmas.targetStatement
    «allInts(_)_VERIFICATION_Bool_ValSeq»
    «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»
    «reverseVS(_)_VERIFICATION_ValSeq_ValSeq»
    «sumIntVS(_)_VERIFICATION_Int_ValSeq»)
#print axioms Proof.final

end Proof
