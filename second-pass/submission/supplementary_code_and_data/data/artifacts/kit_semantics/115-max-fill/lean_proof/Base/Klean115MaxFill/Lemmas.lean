import Klean115MaxFill.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean115MaxFill.Lemmas

def targetStatement
    («definedProjectInt(_)_MAX-FILL-SUMMARY_Bool_Val» : SortVal → SortBool)
    («project:Int?» : SortK → Option SortInt)
    : Prop :=
    (∀ (V : SortVal), ((«project:Int?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((«definedProjectInt(_)_MAX-FILL-SUMMARY_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))

end Klean115MaxFill.Lemmas
