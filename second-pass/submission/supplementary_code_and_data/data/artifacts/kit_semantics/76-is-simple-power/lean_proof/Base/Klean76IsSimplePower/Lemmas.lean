import Klean76IsSimplePower.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean76IsSimplePower.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    (_orBool_ : SortBool → SortBool → SortBool)
    («_>=Int_» : SortInt → SortInt → SortBool)
    («_<=Int_» : SortInt → SortInt → SortBool)
    («_==Bool_» : SortBool → SortBool → SortBool)
    («_==Int_» : SortInt → SortInt → SortBool)
    («_=/=Int_» : SortInt → SortInt → SortBool)
    («_/Int_» : SortInt → SortInt → SortInt)
    («pyMod(_,_)_MPY-INT_Int_Int_Int» : SortInt → SortInt → SortInt)
    («simplePower(_,_)_VERIFICATION_Bool_Int_Int» : SortInt → SortInt → SortBool)
    : Prop :=
    (∀ (N : SortInt) (X : SortInt) (h : (_andBool_ (_orBool_ («_<=Int_» N (-2)) («_>=Int_» N 2)) («_=/=Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» X N) 0)) = true), («_==Bool_» («_==Int_» X 1) («simplePower(_,_)_VERIFICATION_Bool_Int_Int» X N) : SortBool) = (true : SortBool))
    ∧ (∀ (N : SortInt) (X : SortInt) (h : (_andBool_ (_andBool_ («_=/=Int_» X 0) (_orBool_ («_<=Int_» N (-2)) («_>=Int_» N 2))) («_==Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» X N) 0)) = true), («simplePower(_,_)_VERIFICATION_Bool_Int_Int» X N : SortBool) = («simplePower(_,_)_VERIFICATION_Bool_Int_Int» («_/Int_» X N) N : SortBool))

end Klean76IsSimplePower.Lemmas
