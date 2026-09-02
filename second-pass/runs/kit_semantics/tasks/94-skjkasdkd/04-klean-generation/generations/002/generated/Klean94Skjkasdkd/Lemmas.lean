import Klean94Skjkasdkd.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean94Skjkasdkd.Lemmas

def targetStatement
    («_-Int_» : SortInt → SortInt → SortInt)
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>Int_» : SortInt → SortInt → SortBool)
    («_>=Int_» : SortInt → SortInt → SortBool)
    («_<Int_» : SortInt → SortInt → SortBool)
    («_<=Int_» : SortInt → SortInt → SortBool)
    («_==Int_» : SortInt → SortInt → SortBool)
    («_=/=Int_» : SortInt → SortInt → SortBool)
    («_%Int_» : SortInt → SortInt → SortInt)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_/Int_» : SortInt → SortInt → SortInt)
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («definedProjectInt(_)_VERIFICATION_Bool_Val» : SortVal → SortBool)
    («digitSum(_)_VERIFICATION_Int_Int» : SortInt → SortInt)
    (isInt : SortK → SortBool)
    («primeTail(_,_)_VERIFICATION_Bool_Int_Int» : SortInt → SortInt → SortBool)
    («project:Int» : SortK → SortInt)
    (projectIntTotal : SortVal → SortInt)
    («pyMod(_,_)_MPY-INT_Int_Int_Int» : SortInt → SortInt → SortInt)
    : Prop :=
    (∀ (V : SortVal), (True) ↔ (((«definedProjectInt(_)_VERIFICATION_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : («definedProjectInt(_)_VERIFICATION_Bool_Val» V) = true), («project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortInt) = (projectIntTotal V : SortInt))
    ∧ (∀ (V : SortVal), (projectIntTotal (SortVal.inj_SortInt (projectIntTotal V)) : SortInt) = (projectIntTotal V : SortInt))
    ∧ (∀ (I : SortInt) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" V (SortVal.inj_SortInt I) : SortBool) = («_>Int_» (projectIntTotal V) I : SortBool))
    ∧ (∀ (I : SortInt) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">=" V (SortVal.inj_SortInt I) : SortBool) = («_>=Int_» (projectIntTotal V) I : SortBool))
    ∧ (∀ (V : SortVal) (I : SortInt) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "<" (SortVal.inj_SortInt I) V : SortBool) = («_<Int_» I (projectIntTotal V) : SortBool))
    ∧ (∀ (I : SortInt) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "%" V (SortVal.inj_SortInt I) : SortVal) = (SortVal.inj_SortInt («pyMod(_,_)_MPY-INT_Int_Int_Int» (projectIntTotal V) I) : SortVal))
    ∧ (∀ (I : SortInt) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" V (SortVal.inj_SortInt I) : SortVal) = (SortVal.inj_SortInt («_+Int_» (projectIntTotal V) I) : SortVal))
    ∧ (∀ (D : SortInt) (N : SortInt) (h : (_andBool_ (_andBool_ («_>=Int_» D 2) («_<Int_» D N)) («_==Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» N D) 0)) = true), («primeTail(_,_)_VERIFICATION_Bool_Int_Int» N D : SortBool) = (false : SortBool))
    ∧ (∀ (D : SortInt) (N : SortInt) (h : (_andBool_ (_andBool_ («_>Int_» D 2) («_<=Int_» D N)) («_=/=Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» N («_-Int_» D 1)) 0)) = true), («primeTail(_,_)_VERIFICATION_Bool_Int_Int» N D : SortBool) = («primeTail(_,_)_VERIFICATION_Bool_Int_Int» N («_-Int_» D 1) : SortBool))
    ∧ (∀ (N : SortInt) (h : («_>Int_» N 0) = true), («_+Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» N 10) («digitSum(_)_VERIFICATION_Int_Int» («_/Int_» («_-Int_» N («pyMod(_,_)_MPY-INT_Int_Int_Int» N 10)) 10)) : SortInt) = («digitSum(_)_VERIFICATION_Int_Int» N : SortInt))
    ∧ (∀ (N : SortInt) (h : («_>Int_» N 0) = true), («_+Int_» («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10) («digitSum(_)_VERIFICATION_Int_Int» («_/Int_» («_-Int_» N («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10)) 10)) : SortInt) = («digitSum(_)_VERIFICATION_Int_Int» N : SortInt))
    ∧ (∀ (N : SortInt) (T : SortInt) (h : («_>Int_» N 0) = true), («_+Int_» («_+Int_» T («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10)) («digitSum(_)_VERIFICATION_Int_Int» («_/Int_» («_-Int_» N («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10)) 10)) : SortInt) = («_+Int_» T («digitSum(_)_VERIFICATION_Int_Int» N) : SortInt))

end Klean94Skjkasdkd.Lemmas
