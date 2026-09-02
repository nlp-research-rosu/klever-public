import Klean127Intersection.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean127Intersection.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>=Int_» : SortInt → SortInt → SortBool)
    («_<Int_» : SortInt → SortInt → SortBool)
    («_=/=Int_» : SortInt → SortInt → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    («pyMod(_,_)_MPY-INT_Int_Int_Int» : SortInt → SortInt → SortInt)
    («scanHasDivisor(_,_,_)_VERIFICATION-SYNTAX_Bool_Bool_Int_Int» : SortBool → SortInt → SortInt → SortBool)
    : Prop :=
    (∀ (D : SortInt) (N : SortInt) (h : (_andBool_ (_andBool_ («_>=Int_» D 2) («_<Int_» D N)) («_=/=Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» N D) 0)) = true), («scanHasDivisor(_,_,_)_VERIFICATION-SYNTAX_Bool_Bool_Int_Int» false N («_+Int_» D 1) : SortBool) = («scanHasDivisor(_,_,_)_VERIFICATION-SYNTAX_Bool_Bool_Int_Int» false N D : SortBool))

end Klean127Intersection.Lemmas
