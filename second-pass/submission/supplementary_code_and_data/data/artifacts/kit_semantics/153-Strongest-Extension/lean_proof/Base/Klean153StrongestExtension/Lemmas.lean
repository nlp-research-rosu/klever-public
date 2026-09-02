import Klean153StrongestExtension.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean153StrongestExtension.Lemmas

def targetStatement
    («codesProject(_)_VERIFICATION-BASE_IntSeq_Val» : SortVal → SortIntSeq)
    («definedProjectStr(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool)
    («isStringVal(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool)
    («project:Str» : SortK → SortStr)
    (projectStrTotal : SortVal → SortStr)
    («project:Str?» : SortK → Option SortStr)
    : Prop :=
    (∀ (V : SortVal), ((«project:Str?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((«definedProjectStr(_)_VERIFICATION-BASE_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : («definedProjectStr(_)_VERIFICATION-BASE_Bool_Val» V) = true), («project:Str» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortStr) = (projectStrTotal V : SortStr))
    ∧ (∀ (V : SortVal), (projectStrTotal (SortVal.inj_SortStr (projectStrTotal V)) : SortStr) = (projectStrTotal V : SortStr))
    ∧ (∀ (V : SortVal), ((V : SortVal) = (SortVal.inj_SortStr (projectStrTotal V) : SortVal)) ↔ ((«isStringVal(_)_VERIFICATION-BASE_Bool_Val» V : SortBool) = (true : SortBool)))
    ∧ (∀ (V : SortVal), ((V : SortVal) = (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» («codesProject(_)_VERIFICATION-BASE_IntSeq_Val» V)) : SortVal)) ↔ ((«isStringVal(_)_VERIFICATION-BASE_Bool_Val» V : SortBool) = (true : SortBool)))

end Klean153StrongestExtension.Lemmas
