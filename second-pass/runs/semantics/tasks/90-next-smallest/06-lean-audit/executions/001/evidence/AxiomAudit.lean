import Proof

namespace Proof

#check (
  final :
    Klean90NextSmallest.Lemmas.targetStatement
      _List_
      _Map_
      «_in_keys(_)_MAP_Bool_KItem_Map»
      «_[_<-undef]»
      «_|->_»
      ListItem
      notBool_
      «nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int»
)

#print axioms Proof.final

end Proof
