import Klean131Digits.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean131Digits.Lemmas

def targetStatement
    («_-Int_» : SortInt → SortInt → SortInt)
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>Int_» : SortInt → SortInt → SortBool)
    («_==Int_» : SortInt → SortInt → SortBool)
    («_=/=Int_» : SortInt → SortInt → SortBool)
    («_%Int_» : SortInt → SortInt → SortInt)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_/Int_» : SortInt → SortInt → SortInt)
    («_*Int_» : SortInt → SortInt → SortInt)
    («oddDigitProduct(_,_)_DIGITS-VERIFICATION_Int_Int_Int» : SortInt → SortInt → SortInt)
    («pyMod(_,_)_MPY-INT_Int_Int_Int» : SortInt → SortInt → SortInt)
    : Prop :=
    (∀ (A : SortInt) (N : SortInt) (h : _andBool_ («_>Int_» N 0) («_=/=Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» N 2) 1) = true), («oddDigitProduct(_,_)_DIGITS-VERIFICATION_Int_Int_Int» («_/Int_» («_-Int_» N («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10)) 10) A : SortInt) = («oddDigitProduct(_,_)_DIGITS-VERIFICATION_Int_Int_Int» N A : SortInt))
    ∧ (∀ (N : SortInt) (h : _andBool_ («_>Int_» N 0) («_==Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» N 2) 1) = true), («oddDigitProduct(_,_)_DIGITS-VERIFICATION_Int_Int_Int» («_/Int_» («_-Int_» N («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10)) 10) («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10) : SortInt) = («oddDigitProduct(_,_)_DIGITS-VERIFICATION_Int_Int_Int» N 0 : SortInt))
    ∧ (∀ (A : SortInt) (N : SortInt) (h : _andBool_ (_andBool_ («_>Int_» N 0) («_=/=Int_» A 0)) («_==Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» N 2) 1) = true), («oddDigitProduct(_,_)_DIGITS-VERIFICATION_Int_Int_Int» («_/Int_» («_-Int_» N («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10)) 10) («_*Int_» A («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10)) : SortInt) = («oddDigitProduct(_,_)_DIGITS-VERIFICATION_Int_Int_Int» N A : SortInt))

end Klean131Digits.Lemmas
