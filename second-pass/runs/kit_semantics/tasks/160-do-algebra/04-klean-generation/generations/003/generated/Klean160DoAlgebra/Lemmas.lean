import Klean160DoAlgebra.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean160DoAlgebra.Lemmas

def targetStatement
    («Int2String(_)_STRING-COMMON_String_Int» : SortInt → SortString)
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» : SortString → SortVals → SortVal)
    («codesProject(_)_VERIFICATION-SYNTAX_IntSeq_Val» : SortVal → SortIntSeq)
    («definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» : SortVal → SortBool)
    («definedProjectStr(_)_VERIFICATION-SYNTAX_Bool_Val» : SortVal → SortBool)
    («project:Int» : SortK → SortInt)
    («project:Str» : SortK → SortStr)
    (projectIntTotal : SortVal → SortInt)
    («seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» : SortIntSeq → SortIntSeq → SortIntSeq)
    («strToCodes(_)_MPY-STR_IntSeq_String» : SortString → SortIntSeq)
    : Prop :=
    (∀ (V : SortVal), (True) ↔ (((«definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal), (True) ↔ (((«definedProjectStr(_)_VERIFICATION-SYNTAX_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : («definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» V) = true), («applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» "str" (SortVals.«_,__MPY-CORE_Vals_Val_Vals» V SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») : SortVal) = (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» («strToCodes(_)_MPY-STR_IntSeq_String» («Int2String(_)_STRING-COMMON_String_Int» (projectIntTotal V)))) : SortVal))
    ∧ (∀ (V : SortVal) (A : SortIntSeq) (h : («definedProjectStr(_)_VERIFICATION-SYNTAX_Bool_Val» V) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A)) V : SortVal) = (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» («seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» A («codesProject(_)_VERIFICATION-SYNTAX_IntSeq_Val» V))) : SortVal))

end Klean160DoAlgebra.Lemmas
