import Klean108CountNums.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean108CountNums.Lemmas

def targetStatement
    («_-Int_» : SortInt → SortInt → SortInt)
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>=Int_» : SortInt → SortInt → SortBool)
    («_<Int_» : SortInt → SortInt → SortBool)
    («allDigitCodes(_)_VERIFICATION_Bool_IntSeq» : SortIntSeq → SortBool)
    («applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» : SortString → SortVals → SortVal)
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («applyUn(_,_)_MPY-CORE_Val_String_Val» : SortString → SortVal → SortVal)
    («decimalCodes(_)_VERIFICATION_IntSeq_Int» : SortInt → SortIntSeq)
    («definedProjectInt(_)_VERIFICATION_Bool_Val» : SortVal → SortBool)
    (isInt : SortK → SortBool)
    (projectIntTotal : SortVal → SortInt)
    («project:Int?» : SortK → Option SortInt)
    : Prop :=
    (∀ (V : SortVal), ((«project:Int?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((«definedProjectInt(_)_VERIFICATION_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (J : SortInt) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "<" V (SortVal.inj_SortInt J) : SortBool) = («_<Int_» (projectIntTotal V) J : SortBool))
    ∧ (∀ (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyUn(_,_)_MPY-CORE_Val_String_Val» "-" V : SortVal) = (SortVal.inj_SortInt («_-Int_» 0 (projectIntTotal V)) : SortVal))
    ∧ (∀ (V : SortVal) (h : (_andBool_ (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) («_>=Int_» (projectIntTotal V) 0)) = true), («applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» "str" (SortVals.«_,__MPY-CORE_Vals_Val_Vals» V SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») : SortVal) = (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» («decimalCodes(_)_VERIFICATION_IntSeq_Int» (projectIntTotal V))) : SortVal))
    ∧ (∀ (N : SortInt) (h : («_>=Int_» N 0) = true), («allDigitCodes(_)_VERIFICATION_Bool_IntSeq» («decimalCodes(_)_VERIFICATION_IntSeq_Int» N) : SortBool) = (true : SortBool))

end Klean108CountNums.Lemmas
