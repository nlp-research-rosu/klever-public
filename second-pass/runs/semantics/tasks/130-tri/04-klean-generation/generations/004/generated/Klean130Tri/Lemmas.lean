import Klean130Tri.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean130Tri.Lemmas

def targetStatement
    («_-Int_» : SortInt → SortInt → SortInt)
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>=Int_» : SortInt → SortInt → SortBool)
    («_==Int_» : SortInt → SortInt → SortBool)
    («_%Int_» : SortInt → SortInt → SortInt)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_/Int_» : SortInt → SortInt → SortInt)
    («pyMod(_,_)_MPY-INT_Int_Int_Int» : SortInt → SortInt → SortInt)
    (triAt : SortInt → SortInt)
    : Prop :=
    (∀ (I : SortInt) (h : _andBool_ («_>=Int_» I 2) («_==Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» I 2) 0) = true), («_+Int_» («_/Int_» I 2) 1 : SortInt) = (triAt I : SortInt))
    ∧ (∀ (I : SortInt) (h : _andBool_ («_>=Int_» I 3) («_==Int_» («_%Int_» («_+Int_» («_%Int_» I 2) 2) 2) 1) = true), («_+Int_» («_+Int_» («_+Int_» (triAt («_+Int_» I (-1))) (triAt («_+Int_» I (-2)))) 1) («_/Int_» («_-Int_» («_+Int_» I 1) («_%Int_» («_+Int_» («_%Int_» («_+Int_» I 1) 2) 2) 2)) 2) : SortInt) = (triAt I : SortInt))

end Klean130Tri.Lemmas
