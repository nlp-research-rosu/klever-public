import Proof

namespace CounterfactualGuard

def badAnd (_ _ : SortBool) : SortBool := false

/- This deliberately dishonest bridge makes both arithmetic hypotheses false.
   It demonstrates why the operational-bridge audit is necessary in addition
   to checking Proof.final. -/
theorem vacuousArithmetic :
    Klean8SumProduct.Lemmas.targetStatement
      badAnd
      Proof.«_+Int_»
      Proof.«_*Int_»
      Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val»
      Proof.isInt
      Proof.projectIntTotal
      Proof.«project:Int?» := by
  have h := Proof.final
  unfold Klean8SumProduct.Lemmas.targetStatement at h ⊢
  rcases h with ⟨hDefined, hProjection, _, _⟩
  refine ⟨hDefined, hProjection, ?_, ?_⟩
  · intro W V hFalse
    simp [badAnd] at hFalse
  · intro W V hFalse
    simp [badAnd] at hFalse

def badPlus (_ _ : SortInt) : SortInt := 0
def badMul (_ _ : SortInt) : SortInt := 0
def badApply (_ : SortString) (_ _ : SortVal) : SortVal :=
  SortVal.inj_SortInt 0

/- A coordinated hard-coded arithmetic interpretation also satisfies the bare
   generated equations.  The actual candidate must therefore be checked
   against K, not merely accepted because this proposition is inhabited. -/
theorem hardCodedArithmetic :
    Klean8SumProduct.Lemmas.targetStatement
      Proof._andBool_
      badPlus
      badMul
      badApply
      Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val»
      Proof.isInt
      Proof.projectIntTotal
      Proof.«project:Int?» := by
  have h := Proof.final
  unfold Klean8SumProduct.Lemmas.targetStatement at h ⊢
  rcases h with ⟨hDefined, hProjection, _, _⟩
  refine ⟨hDefined, hProjection, ?_, ?_⟩
  · intro W V _
    rfl
  · intro W V _
    rfl

end CounterfactualGuard
