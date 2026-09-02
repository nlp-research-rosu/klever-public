import Klean114Minsubarraysum.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean114Minsubarraysum.Lemmas

def targetStatement
    («_+Int_» : SortInt → SortInt → SortInt)
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» : SortString → SortVals → SortVal)
    (isInt : SortK → SortBool)
    («minInt(_,_)_INT-COMMON_Int_Int_Int» : SortInt → SortInt → SortInt)
    («project:Int» : SortK → SortInt)
    : Prop :=
    (∀ (V : SortVal) (I : SortInt) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" (SortVal.inj_SortInt I) V : SortVal) = (SortVal.inj_SortInt («_+Int_» I («project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk))) : SortVal))
    ∧ (∀ (I : SortInt) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» "min" (SortVals.«_,__MPY-CORE_Vals_Val_Vals» V (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»)) : SortVal) = (SortVal.inj_SortInt («minInt(_,_)_INT-COMMON_Int_Int_Int» («project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) I) : SortVal))

end Klean114Minsubarraysum.Lemmas
