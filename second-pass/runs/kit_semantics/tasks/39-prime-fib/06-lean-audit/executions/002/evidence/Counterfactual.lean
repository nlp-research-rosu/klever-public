import Proof

namespace Counterfactual

def hardCodedSearch (_target _count _a b : SortInt) : SortInt := b

theorem hardCodedStillProvesTarget :
    Klean39PrimeFib.Lemmas.targetStatement
      Proof._andBool_
      Proof.«_>=Int_»
      Proof.«_<Int_»
      Proof.«_+Int_»
      Proof.notBool_
      hardCodedSearch
      Proof.«primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool» := by
  constructor
  · intro _d _a _h
    rfl
  · intro _b _a _count _target _h
    rfl

#print axioms Counterfactual.hardCodedStillProvesTarget

end Counterfactual
