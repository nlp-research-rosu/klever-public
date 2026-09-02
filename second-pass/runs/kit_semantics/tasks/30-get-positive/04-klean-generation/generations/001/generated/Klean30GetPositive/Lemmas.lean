import Klean30GetPositive.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean30GetPositive.Lemmas

def targetStatement
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («numericVal(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool)
    («positiveNumeric(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool)
    : Prop :=
    (∀ (V : SortVal) (h : («numericVal(_)_VERIFICATION-BASE_Bool_Val» V) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" V (SortVal.inj_SortFloat (0.0 : Float)) : SortBool) = («positiveNumeric(_)_VERIFICATION-BASE_Bool_Val» V : SortBool))

end Klean30GetPositive.Lemmas
