import Klean8SumProduct.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean8SumProduct.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_*Int_» : SortInt → SortInt → SortInt)
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («definedProjectInt(_)_VERIFICATION_Bool_Val» : SortVal → SortBool)
    (isInt : SortK → SortBool)
    («project:Int» : SortK → SortInt)
    (projectIntTotal : SortVal → SortInt)
    : Prop :=
    (∀ (V : SortVal), (True) ↔ (((«definedProjectInt(_)_VERIFICATION_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal), (projectIntTotal (SortVal.inj_SortInt (projectIntTotal V)) : SortInt) = (projectIntTotal V : SortInt))
    ∧ (∀ (W : SortVal) (V : SortVal) (h : (_andBool_ (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) (isInt (SortK.kseq ((@inj SortVal SortKItem) W) SortK.dotk))) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" V W : SortVal) = (SortVal.inj_SortInt («_+Int_» (projectIntTotal V) (projectIntTotal W)) : SortVal))
    ∧ (∀ (W : SortVal) (V : SortVal) (h : (_andBool_ (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) (isInt (SortK.kseq ((@inj SortVal SortKItem) W) SortK.dotk))) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "*" V W : SortVal) = (SortVal.inj_SortInt («_*Int_» (projectIntTotal V) (projectIntTotal W)) : SortVal))

end Klean8SumProduct.Lemmas
