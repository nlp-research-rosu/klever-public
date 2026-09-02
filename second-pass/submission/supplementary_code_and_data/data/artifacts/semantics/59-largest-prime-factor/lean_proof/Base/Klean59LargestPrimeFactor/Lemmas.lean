import Klean59LargestPrimeFactor.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean59LargestPrimeFactor.Lemmas

def targetStatement
    (_Map_ : SortMap → SortMap → SortMap)
    («_in_keys(_)_MAP_Bool_KItem_Map» : SortKItem → SortMap → SortBool)
    («_[_<-undef]» : SortMap → SortKItem → SortMap)
    («_|->_» : SortKItem → SortKItem → SortMap)
    (notBool_ : SortBool → SortBool)
    : Prop :=
    (∀ (L : SortInt) (M : SortMap) (_V : SortScope) (h : notBool_ («_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortInt L) M) = true), («_[_<-undef]» (_Map_ («_|->_» (SortKItem.inj_SortInt L) (SortKItem.inj_SortScope _V)) M) (SortKItem.inj_SortInt L) : SortMap) = (M : SortMap))

end Klean59LargestPrimeFactor.Lemmas
