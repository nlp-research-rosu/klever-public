import Klean21RescaleToUnit.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean21RescaleToUnit.Lemmas

def targetStatement
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («definedProjectFloat(_)_VERIFICATION_Bool_Val» : SortVal → SortBool)
    (isFloat : SortK → SortBool)
    (projectFloatTotal : SortVal → SortFloat)
    (subF : SortFloat → SortFloat → SortFloat)
    («project:Float?» : SortK → Option SortFloat)
    : Prop :=
    (∀ (V : SortVal), ((«project:Float?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((«definedProjectFloat(_)_VERIFICATION_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (F : SortFloat) (V : SortVal) (h : (isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "-" V (SortVal.inj_SortFloat F) : SortVal) = (SortVal.inj_SortFloat (subF (projectFloatTotal V) F) : SortVal))

end Klean21RescaleToUnit.Lemmas
