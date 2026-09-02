import Klean77Iscube.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean77Iscube.Lemmas

def targetStatement
    (_Map_ : SortMap → SortMap → SortMap)
    («_in_keys(_)_MAP_Bool_KItem_Map» : SortKItem → SortMap → SortBool)
    («_<Int_» : SortInt → SortInt → SortBool)
    («_==Int_» : SortInt → SortInt → SortBool)
    («_[_<-undef]» : SortMap → SortKItem → SortMap)
    («_|->_» : SortKItem → SortKItem → SortMap)
    («_*Int_» : SortInt → SortInt → SortInt)
    («cubeSearch(_,_)_VERIFICATION-SYNTAX_Bool_Int_Int» : SortInt → SortInt → SortBool)
    (notBool_ : SortBool → SortBool)
    : Prop :=
    (∀ (A : SortInt) (I : SortInt) (h : (notBool_ («_<Int_» («_*Int_» («_*Int_» I I) I) A)) = true), («_==Int_» («_*Int_» («_*Int_» I I) I) A : SortBool) = («cubeSearch(_,_)_VERIFICATION-SYNTAX_Bool_Int_Int» A I : SortBool))
    ∧ (∀ (REST : SortMap) (S : SortScope) (h : (notBool_ («_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortInt 1) REST)) = true), («_[_<-undef]» (_Map_ («_|->_» (SortKItem.inj_SortInt 1) (SortKItem.inj_SortScope S)) REST) (SortKItem.inj_SortInt 1) : SortMap) = (REST : SortMap))

end Klean77Iscube.Lemmas
