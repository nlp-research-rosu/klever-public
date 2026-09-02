import Klean68Pluck.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean68Pluck.Lemmas

def targetStatement
    («_+Int_» : SortInt → SortInt → SortInt)
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («definedProjectInt(_)_VERIFICATION_Bool_Val» : SortVal → SortBool)
    (projectIntTotal : SortVal → SortInt)
    («project:Int?» : SortK → Option SortInt)
    : Prop :=
    (∀ (V : SortVal), ((«project:Int?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((«definedProjectInt(_)_VERIFICATION_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (I : SortInt) (V : SortVal) (h : («definedProjectInt(_)_VERIFICATION_Bool_Val» V) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" V (SortVal.inj_SortInt I) : SortVal) = (SortVal.inj_SortInt («_+Int_» (projectIntTotal V) I) : SortVal))

end Klean68Pluck.Lemmas
