import Klean127Intersection.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean127Intersection.Lemmas

def targetStatement
    (_Map_ : SortMap → SortMap → SortMap)
    («_in_keys(_)_MAP_Bool_KItem_Map» : SortKItem → SortMap → SortBool)
    («_[_<-undef]» : SortMap → SortKItem → SortMap)
    («_|->_» : SortKItem → SortKItem → SortMap)
    (notBool_ : SortBool → SortBool)
    : Prop :=
    (∀ (REST : SortMap) (_FRAME : SortScope) (_Gen1 : SortKItem) (h : notBool_ («_in_keys(_)_MAP_Bool_KItem_Map» _Gen1 REST) = true), («_[_<-undef]» (_Map_ («_|->_» (SortKItem.inj_SortInt 1) (SortKItem.inj_SortScope _FRAME)) REST) (SortKItem.inj_SortInt 1) : SortMap) = (REST : SortMap))

end Klean127Intersection.Lemmas
