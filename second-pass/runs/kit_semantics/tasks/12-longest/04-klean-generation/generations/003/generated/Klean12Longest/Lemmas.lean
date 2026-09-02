import Klean12Longest.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean12Longest.Lemmas

def targetStatement
    («isStringValue(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool)
    (projectString : SortVal → SortStr)
    («seqLen(_)_MPY-BUILTINS_Int_Val» : SortVal → SortInt)
    (seqLenString : SortStr → SortInt)
    («project:Str?» : SortK → Option SortStr)
    : Prop :=
    (∀ (V : SortVal), ((«project:Str?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((«isStringValue(_)_VERIFICATION-BASE_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : («isStringValue(_)_VERIFICATION-BASE_Bool_Val» V) = true), («seqLen(_)_MPY-BUILTINS_Int_Val» V : SortInt) = (seqLenString (projectString V) : SortInt))

end Klean12Longest.Lemmas
