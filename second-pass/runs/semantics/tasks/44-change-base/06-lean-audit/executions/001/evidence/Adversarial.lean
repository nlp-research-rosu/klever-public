import Proof

namespace Adversarial

def emptyMap : SortMap := ⟨[]⟩

def constantMap₂ (_ _ : SortMap) : SortMap := emptyMap
def constantMembership (_ : SortKItem) (_ : SortMap) : SortBool := true
def constantDelete (_ : SortMap) (_ : SortKItem) : SortMap := emptyMap
def constantSingleton (_ _ : SortKItem) : SortMap := emptyMap
def constantUpdate (_ : SortMap) (_ _ : SortKItem) : SortMap := emptyMap
def constantFresh (_ : SortInt) (_ : SortMap) : SortBool := false
def constantNot (_ : SortBool) : SortBool := false

theorem sortScopeIsEmpty (value : SortScope) : False := by
  exact nomatch value

theorem constantDefinitionsStillProveTarget :
    Klean44ChangeBase.Lemmas.targetStatement
      constantMap₂
      constantMembership
      constantDelete
      constantSingleton
      constantUpdate
      constantFresh
      constantNot := by
  constructor
  · intro S L h
    simp [constantFresh] at h
  constructor
  · intro V
    exact nomatch V
  · intro L S V
    exact nomatch V

theorem candidateFreshAcceptsNonScopeValue :
    Proof.«freshScopes(_,_)_VERIFICATION_Bool_Int_Map»
      2
      ⟨[(
        SortKItem.inj_SortInt 0,
        SortKItem.inj_SortInt 99
      )]⟩ = true := by
  rfl

theorem candidateConcatAcceptsOverlap :
    (Proof._Map_
      ⟨[(SortKItem.inj_SortInt 0, SortKItem.inj_SortInt 10)]⟩
      ⟨[(SortKItem.inj_SortInt 0, SortKItem.inj_SortInt 20)]⟩).coll
    =
      [
        (SortKItem.inj_SortInt 0, SortKItem.inj_SortInt 10),
        (SortKItem.inj_SortInt 0, SortKItem.inj_SortInt 20)
      ] := by
  rfl

end Adversarial
