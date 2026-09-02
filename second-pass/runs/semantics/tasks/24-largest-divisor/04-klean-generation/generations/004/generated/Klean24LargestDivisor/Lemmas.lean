import Klean24LargestDivisor.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean24LargestDivisor.Lemmas

def targetStatement
    (_Map_ : SortMap → SortMap → SortMap)
    («_in_keys(_)_MAP_Bool_KItem_Map» : SortKItem → SortMap → SortBool)
    («_[_<-undef]» : SortMap → SortKItem → SortMap)
    («_|->_» : SortKItem → SortKItem → SortMap)
    (notBool_ : SortBool → SortBool)
    : Prop :=
    (∀ (SC : SortMap) (_S : SortScope) (h : notBool_ («_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortInt 1) SC) = true), («_[_<-undef]» (_Map_ («_|->_» (SortKItem.inj_SortInt 1) (SortKItem.inj_SortScope _S)) SC) (SortKItem.inj_SortInt 1) : SortMap) = (SC : SortMap))

end Klean24LargestDivisor.Lemmas
