import Klean141FileNameCheck.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean141FileNameCheck.Lemmas

def targetStatement
    («_>Int_» : SortInt → SortInt → SortBool)
    («_<=Int_» : SortInt → SortInt → SortBool)
    : Prop :=
    (∀ (N : SortInt) (h : («_<=Int_» N 3) = true), («_>Int_» N 3 : SortBool) = (false : SortBool))

end Klean141FileNameCheck.Lemmas
