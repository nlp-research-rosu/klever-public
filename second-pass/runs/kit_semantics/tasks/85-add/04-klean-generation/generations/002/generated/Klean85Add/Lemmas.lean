import Klean85Add.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean85Add.Lemmas

def targetStatement
    («_+Int_» : SortInt → SortInt → SortInt)
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» : SortVal → SortBool)
    (isInt : SortK → SortBool)
    («project:Int» : SortK → SortInt)
    (projectIntTotal : SortVal → SortInt)
    («pyMod(_,_)_MPY-INT_Int_Int_Int» : SortInt → SortInt → SortInt)
    : Prop :=
    (∀ (V : SortVal), (True) ↔ (((«definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (I : SortInt) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "%" V (SortVal.inj_SortInt I) : SortVal) = (SortVal.inj_SortInt («pyMod(_,_)_MPY-INT_Int_Int_Int» (projectIntTotal V) I) : SortVal))
    ∧ (∀ (V : SortVal) (I : SortInt) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" (SortVal.inj_SortInt I) V : SortVal) = (SortVal.inj_SortInt («_+Int_» I (projectIntTotal V)) : SortVal))

end Klean85Add.Lemmas
