import Klean44ChangeBase.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean44ChangeBase.Lemmas

def targetStatement
    (_Map_ : SortMap → SortMap → SortMap)
    («_in_keys(_)_MAP_Bool_KItem_Map» : SortKItem → SortMap → SortBool)
    («_[_<-undef]» : SortMap → SortKItem → SortMap)
    («_|->_» : SortKItem → SortKItem → SortMap)
    («Map:update» : SortMap → SortKItem → SortKItem → SortMap)
    («freshScopes(_,_)_VERIFICATION_Bool_Int_Map» : SortInt → SortMap → SortBool)
    (notBool_ : SortBool → SortBool)
    : Prop :=
    (∀ (S : SortMap) (L : SortInt) (h : «freshScopes(_,_)_VERIFICATION_Bool_Int_Map» L S = true), («_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortInt L) S : SortBool) = (false : SortBool))
    ∧ (∀ (V : SortScope) (L : SortInt) (S : SortMap) (h : notBool_ («_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortInt L) S) = true), («Map:update» S (SortKItem.inj_SortInt L) (SortKItem.inj_SortScope V) : SortMap) = (_Map_ («_|->_» (SortKItem.inj_SortInt L) (SortKItem.inj_SortScope V)) S : SortMap))
    ∧ (∀ (L : SortInt) (S : SortMap) (V : SortScope) (h : notBool_ («_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortInt L) S) = true), («_[_<-undef]» (_Map_ («_|->_» (SortKItem.inj_SortInt L) (SortKItem.inj_SortScope V)) S) (SortKItem.inj_SortInt L) : SortMap) = (S : SortMap))

end Klean44ChangeBase.Lemmas
