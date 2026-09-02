import Klean61CorrectBracketing.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean61CorrectBracketing.Lemmas

def kite {α : Type} (c : SortBool) (t e : α) : α := cond c t e

def targetStatement
    («_==Int_» : SortInt → SortInt → SortBool)
    («_=/=Int_» : SortInt → SortInt → SortBool)
    : Prop :=
    (∀ (Y : SortInt) (_X : SortInt) (C : SortInt) (h : («_=/=Int_» C 40) = true), (kite («_==Int_» C 40) _X Y : SortInt) = (Y : SortInt))

end Klean61CorrectBracketing.Lemmas
