import Klean131Digits.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean131Digits.Lemmas

def targetStatement
    («_-Int_» : SortInt → SortInt → SortInt)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_*Int_» : SortInt → SortInt → SortInt)
    : Prop :=
    (∀ (X : SortInt), («_*Int_» 1 X : SortInt) = (X : SortInt))
    ∧ (∀ (X : SortInt), («_*Int_» X 1 : SortInt) = (X : SortInt))
    ∧ (∀ (X : SortInt), («_-Int_» («_+Int_» X 1) X : SortInt) = (1 : SortInt))
    ∧ (∀ (Z : SortInt) (Y : SortInt) (X : SortInt), («_*Int_» («_*Int_» X Y) Z : SortInt) = («_*Int_» X («_*Int_» Y Z) : SortInt))

end Klean131Digits.Lemmas
