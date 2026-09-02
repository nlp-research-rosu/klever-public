import Klean92AnyInt.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean92AnyInt.Lemmas

def kite {α : Type} (c : SortBool) (t e : α) : α := cond c t e

def targetStatement
    («boolAsInt(_)_MPY-CORE_Int_Bool» : SortBool → SortInt)
    : Prop :=
    (∀ (B : SortBool), («boolAsInt(_)_MPY-CORE_Int_Bool» B : SortInt) = (kite B 1 0 : SortInt))

end Klean92AnyInt.Lemmas
