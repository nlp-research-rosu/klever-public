import Klean57Monotonic.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean57Monotonic.Lemmas

def targetStatement
    (_orBool_ : SortBool → SortBool → SortBool)
    («_==Bool_» : SortBool → SortBool → SortBool)
    (notBool_ : SortBool → SortBool)
    : Prop :=
    (∀ (B : SortBool) (A : SortBool) (h : (A) = true), («_==Bool_» A (_orBool_ A B) : SortBool) = (true : SortBool))
    ∧ (∀ (B : SortBool) (A : SortBool) (h : (notBool_ A) = true), («_==Bool_» B (_orBool_ A B) : SortBool) = (true : SortBool))

end Klean57Monotonic.Lemmas
