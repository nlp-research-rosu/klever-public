import Klean142SumSquares.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean142SumSquares.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_*Int_» : SortInt → SortInt → SortInt)
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («definedProjectInt(_)_VERIFICATION_Bool_Val» : SortVal → SortBool)
    (isInt : SortK → SortBool)
    («project:Int» : SortK → SortInt)
    (projectIntTotal : SortVal → SortInt)
    («project:Int?» : SortK → Option SortInt)
    : Prop :=
    (∀ (V : SortVal), ((«project:Int?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((«definedProjectInt(_)_VERIFICATION_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : («definedProjectInt(_)_VERIFICATION_Bool_Val» V) = true), («project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortInt) = (projectIntTotal V : SortInt))
    ∧ (∀ (V : SortVal), (projectIntTotal (SortVal.inj_SortInt (projectIntTotal V)) : SortInt) = (projectIntTotal V : SortInt))
    ∧ (∀ (W : SortVal) (V : SortVal) (h : (_andBool_ (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) (isInt (SortK.kseq ((@inj SortVal SortKItem) W) SortK.dotk))) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "*" V W : SortVal) = (SortVal.inj_SortInt («_*Int_» (projectIntTotal V) (projectIntTotal W)) : SortVal))
    ∧ (∀ (V : SortVal) (I : SortInt) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" (SortVal.inj_SortInt I) V : SortVal) = (SortVal.inj_SortInt («_+Int_» I (projectIntTotal V)) : SortVal))

end Klean142SumSquares.Lemmas
