import Proof

namespace Proof

#check (final :
  Klean105ByLength.Lemmas.targetStatement
    «_==Int_»
    «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    isInt
    «project:Int»)

#print axioms final

end Proof
