import Klean74TotalMatch.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean74TotalMatch.Lemmas

def targetStatement
    («isLen(_)_MPY-CORE_Int_IntSeq» : SortIntSeq → SortInt)
    («isStrV(_)_MPY-BUILTINS_Bool_Val» : SortVal → SortBool)
    («seqLen(_)_MPY-BUILTINS_Int_Val» : SortVal → SortInt)
    («stringCodes(_)_VERIFICATION_IntSeq_Val» : SortVal → SortIntSeq)
    : Prop :=
    (∀ (V : SortVal) (h : («isStrV(_)_MPY-BUILTINS_Bool_Val» V) = true), («seqLen(_)_MPY-BUILTINS_Int_Val» V : SortInt) = («isLen(_)_MPY-CORE_Int_IntSeq» («stringCodes(_)_VERIFICATION_IntSeq_Val» V) : SortInt))

end Klean74TotalMatch.Lemmas
