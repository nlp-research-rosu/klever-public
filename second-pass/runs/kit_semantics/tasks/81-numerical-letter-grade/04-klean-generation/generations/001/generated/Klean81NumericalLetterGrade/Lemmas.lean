import Klean81NumericalLetterGrade.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean81NumericalLetterGrade.Lemmas

def targetStatement
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («gradeEq(_,_)_VERIFICATION_Bool_Val_Float» : SortVal → SortFloat → SortBool)
    («gradeGt(_,_)_VERIFICATION_Bool_Val_Float» : SortVal → SortFloat → SortBool)
    («isGradeNumber(_)_VERIFICATION_Bool_Val» : SortVal → SortBool)
    : Prop :=
    (∀ (F : SortFloat) (V : SortVal) (h : («isGradeNumber(_)_VERIFICATION_Bool_Val» V) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "==" V (SortVal.inj_SortFloat F) : SortBool) = («gradeEq(_,_)_VERIFICATION_Bool_Val_Float» V F : SortBool))
    ∧ (∀ (F : SortFloat) (V : SortVal) (h : («isGradeNumber(_)_VERIFICATION_Bool_Val» V) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" V (SortVal.inj_SortFloat F) : SortBool) = («gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V F : SortBool))

end Klean81NumericalLetterGrade.Lemmas
