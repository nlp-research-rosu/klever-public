import Klean63Fibfib.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean63Fibfib.Lemmas

def targetStatement
    («_>=Int_» : SortInt → SortInt → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    («fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» : SortInt → SortInt)
    : Prop :=
    (∀ (I : SortInt) (h : («_>=Int_» I 0) = true), («_+Int_» («_+Int_» («fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» I) («fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» («_+Int_» I 1))) («fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» («_+Int_» I 2)) : SortInt) = («fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» («_+Int_» I 3) : SortInt))

end Klean63Fibfib.Lemmas
