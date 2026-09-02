import Klean70StrangeSortList.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean70StrangeSortList.Lemmas

def targetStatement
    (_Map_ : SortMap → SortMap → SortMap)
    («_in_keys(_)_MAP_Bool_KItem_Map» : SortKItem → SortMap → SortBool)
    («_[_<-undef]» : SortMap → SortKItem → SortMap)
    («_|->_» : SortKItem → SortKItem → SortMap)
    (notBool_ : SortBool → SortBool)
    : Prop :=
    (∀ (K : SortInt) (_V : SortScope) (M : SortMap) (h : (notBool_ («_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortInt K) M)) = true), («_[_<-undef]» (_Map_ M («_|->_» (SortKItem.inj_SortInt K) (SortKItem.inj_SortScope _V))) (SortKItem.inj_SortInt K) : SortMap) = (M : SortMap))

end Klean70StrangeSortList.Lemmas
