import Klean135CanArrange.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean135CanArrange.Lemmas

def targetStatement
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («orderGe(_,_)_VERIFICATION-BASE_Bool_Val_Val» : SortVal → SortVal → SortBool)
    («orderablePair(_,_)_VERIFICATION-BASE_Bool_Val_Val» : SortVal → SortVal → SortBool)
    : Prop :=
    (∀ (W : SortVal) (V : SortVal) (h : («orderablePair(_,_)_VERIFICATION-BASE_Bool_Val_Val» V W) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">=" V W : SortBool) = («orderGe(_,_)_VERIFICATION-BASE_Bool_Val_Val» V W : SortBool))

end Klean135CanArrange.Lemmas
