import Klean63Fibfib.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean63Fibfib.Lemmas

def targetStatement
    («_-Int_» : SortInt → SortInt → SortInt)
    («_+Int_» : SortInt → SortInt → SortInt)
    : Prop :=
    (∀ (N : SortInt) (I : SortInt), «_-Int_» N («_+Int_» I 1) = «_+Int_» («_-Int_» N I) (-1))

end Klean63Fibfib.Lemmas
