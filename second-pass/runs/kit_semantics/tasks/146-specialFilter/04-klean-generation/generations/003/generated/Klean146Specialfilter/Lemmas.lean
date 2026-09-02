import Klean146Specialfilter.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean146Specialfilter.Lemmas

def targetStatement
    («_>Int_» : SortInt → SortInt → SortBool)
    («Int2String(_)_STRING-COMMON_String_Int» : SortInt → SortString)
    («applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» : SortString → SortVals → SortVal)
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («definedProjectInt(_)_VERIFICATION_Bool_Val» : SortVal → SortBool)
    («project:Int» : SortK → SortInt)
    (projectIntTotal : SortVal → SortInt)
    («strToCodes(_)_MPY-STR_IntSeq_String» : SortString → SortIntSeq)
    («project:Int?» : SortK → Option SortInt)
    : Prop :=
    (∀ (V : SortVal), ((«project:Int?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((«definedProjectInt(_)_VERIFICATION_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : («definedProjectInt(_)_VERIFICATION_Bool_Val» V) = true), («project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortInt) = (projectIntTotal V : SortInt))
    ∧ (∀ (I : SortInt) (V : SortVal) (h : («definedProjectInt(_)_VERIFICATION_Bool_Val» V) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" V (SortVal.inj_SortInt I) : SortBool) = («_>Int_» (projectIntTotal V) I : SortBool))
    ∧ (∀ (V : SortVal) (h : («definedProjectInt(_)_VERIFICATION_Bool_Val» V) = true), («applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» "str" (SortVals.«_,__MPY-CORE_Vals_Val_Vals» V SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») : SortVal) = (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» («strToCodes(_)_MPY-STR_IntSeq_String» («Int2String(_)_STRING-COMMON_String_Int» (projectIntTotal V)))) : SortVal))

end Klean146Specialfilter.Lemmas
