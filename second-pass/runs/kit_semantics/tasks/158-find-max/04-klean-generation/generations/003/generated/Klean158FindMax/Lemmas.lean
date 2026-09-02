import Klean158FindMax.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean158FindMax.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» : SortString → SortVals → SortVal)
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («codesOf(_)_VERIFICATION_IntSeq_Str» : SortStr → SortIntSeq)
    («dedupCodes(_)_MPY-SET_IntSeq_IntSeq» : SortIntSeq → SortIntSeq)
    («definedProjectStr(_)_VERIFICATION_Bool_Val» : SortVal → SortBool)
    (projectStrTotal : SortVal → SortStr)
    («strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» : SortIntSeq → SortIntSeq → SortBool)
    («project:Str?» : SortK → Option SortStr)
    : Prop :=
    (∀ (V : SortVal), ((«project:Str?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((«definedProjectStr(_)_VERIFICATION_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal), (projectStrTotal (SortVal.inj_SortStr (projectStrTotal V)) : SortStr) = (projectStrTotal V : SortStr))
    ∧ (∀ (V : SortVal) (h : («definedProjectStr(_)_VERIFICATION_Bool_Val» V) = true), («applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» "set" (SortVals.«_,__MPY-CORE_Vals_Val_Vals» V SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») : SortVal) = (SortVal.«setV(_)_MPY-SET_Val_IntSeq» («dedupCodes(_)_MPY-SET_IntSeq_IntSeq» («codesOf(_)_VERIFICATION_IntSeq_Str» (projectStrTotal V))) : SortVal))
    ∧ (∀ (B : SortVal) (A : SortVal) (h : (_andBool_ («definedProjectStr(_)_VERIFICATION_Bool_Val» A) («definedProjectStr(_)_VERIFICATION_Bool_Val» B)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "<" A B : SortBool) = («strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» («codesOf(_)_VERIFICATION_IntSeq_Str» (projectStrTotal A)) («codesOf(_)_VERIFICATION_IntSeq_Str» (projectStrTotal B)) : SortBool))

end Klean158FindMax.Lemmas
