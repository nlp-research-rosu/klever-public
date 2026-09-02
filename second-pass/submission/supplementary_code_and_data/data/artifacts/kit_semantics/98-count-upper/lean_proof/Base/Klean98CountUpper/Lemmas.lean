import Klean98CountUpper.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean98CountUpper.Lemmas

def targetStatement
    («_+Int_» : SortInt → SortInt → SortInt)
    : Prop :=
    (∀ (C : SortInt) (B : SortInt) (A : SortInt), («_+Int_» («_+Int_» A B) C : SortInt) = («_+Int_» A («_+Int_» B C) : SortInt))

end Klean98CountUpper.Lemmas
