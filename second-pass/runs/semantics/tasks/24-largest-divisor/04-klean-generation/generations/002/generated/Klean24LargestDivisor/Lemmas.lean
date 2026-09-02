import Klean24LargestDivisor.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean24LargestDivisor.Lemmas

def targetStatement
    («_-Int_» : SortInt → SortInt → SortInt)
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>Int_» : SortInt → SortInt → SortBool)
    («_=/=Int_» : SortInt → SortInt → SortBool)
    («firstDivisorAtOrBelow(_,_)_VERIFICATION_Int_Int_Int» : SortInt → SortInt → SortInt)
    («pyMod(_,_)_MPY-INT_Int_Int_Int» : SortInt → SortInt → SortInt)
    : Prop :=
    (∀ (D : SortInt) (N : SortInt) (h : _andBool_ («_>Int_» D 1) («_=/=Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» N D) 0) = true), («firstDivisorAtOrBelow(_,_)_VERIFICATION_Int_Int_Int» N D : SortInt) = («firstDivisorAtOrBelow(_,_)_VERIFICATION_Int_Int_Int» N («_-Int_» D 1) : SortInt))

end Klean24LargestDivisor.Lemmas
