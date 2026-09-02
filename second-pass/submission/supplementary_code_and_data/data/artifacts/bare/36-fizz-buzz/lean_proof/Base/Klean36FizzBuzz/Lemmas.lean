import Klean36FizzBuzz.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean36FizzBuzz.Lemmas

def targetStatement
    («_+Int_» : SortInt → SortInt → SortInt)
    : Prop :=
    (∀ (A : SortInt) (B : SortInt) (C : SortInt), «_+Int_» («_+Int_» A B) C = «_+Int_» A («_+Int_» B C))

end Klean36FizzBuzz.Lemmas
