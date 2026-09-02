import Klean94Skjkasdkd.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean94Skjkasdkd.Lemmas

def targetStatement
    (_Map_ : SortMap → SortMap → SortMap)
    («_in_keys(_)_MAP_Bool_KItem_Map» : SortKItem → SortMap → SortBool)
    («_[_<-undef]» : SortMap → SortKItem → SortMap)
    («_|->_» : SortKItem → SortKItem → SortMap)
    («Map:update» : SortMap → SortKItem → SortKItem → SortMap)
    (notBool_ : SortBool → SortBool)
    : Prop :=
    (∀ (X : SortKItem) (_Gen0 : SortKItem) (M : SortMap) (h : notBool_ («_in_keys(_)_MAP_Bool_KItem_Map» X M) = true), «_[_<-undef]» (_Map_ («_|->_» X _Gen0) M) X = M)
    ∧ (∀ (M : SortMap) (X : SortKItem) (V : SortKItem) (h : notBool_ («_in_keys(_)_MAP_Bool_KItem_Map» X M) = true), «Map:update» M X V = _Map_ («_|->_» X V) M)

end Klean94Skjkasdkd.Lemmas
