import Proof

#check (
  Proof.final :
    Klean70StrangeSortList.Lemmas.targetStatement
      Proof._Map_
      Proof.«_in_keys(_)_MAP_Bool_KItem_Map»
      Proof.«_[_<-undef]»
      Proof.«_|->_»
      Proof.notBool_)

#print axioms Proof.final
