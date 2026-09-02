import Klean12Longest.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean12Longest.Lemmas

def targetStatement
    («isStringValue(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool)
    («project:Str» : SortK → SortStr)
    (projectString : SortVal → SortStr)
    («seqLen(_)_MPY-BUILTINS_Int_Val» : SortVal → SortInt)
    (seqLenString : SortStr → SortInt)
    : Prop :=
    (∀ (V : SortVal), (True) ↔ (((«isStringValue(_)_VERIFICATION-BASE_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : («isStringValue(_)_VERIFICATION-BASE_Bool_Val» V) = true), («seqLen(_)_MPY-BUILTINS_Int_Val» V : SortInt) = (seqLenString (projectString V) : SortInt))

end Klean12Longest.Lemmas
