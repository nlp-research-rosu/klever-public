import Klean110Exchange.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean110Exchange.Lemmas

def targetStatement
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («definedProjectBool(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool)
    («definedProjectFloat(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool)
    («definedProjectInt(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool)
    («isNumberVal(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool)
    («numberEven(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool)
    («project:Bool» : SortK → SortBool)
    («project:Float» : SortK → SortFloat)
    («project:Int» : SortK → SortInt)
    : Prop :=
    (∀ (V : SortVal), (True) ↔ (((«definedProjectInt(_)_VERIFICATION-BASE_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal), (True) ↔ (((«definedProjectBool(_)_VERIFICATION-BASE_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal), (True) ↔ (((«definedProjectFloat(_)_VERIFICATION-BASE_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : («isNumberVal(_)_VERIFICATION-BASE_Bool_Val» V) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "==" («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "%" V (SortVal.inj_SortInt 2)) (SortVal.inj_SortInt 0) : SortBool) = («numberEven(_)_VERIFICATION-BASE_Bool_Val» V : SortBool))
    ∧ (∀ (V : SortVal) (h : («isNumberVal(_)_VERIFICATION-BASE_Bool_Val» V) = true), (True) ↔ (True))

end Klean110Exchange.Lemmas
