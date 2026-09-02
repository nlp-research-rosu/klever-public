import Proof

namespace OperationalBridgeTests

def badMap (left _right : SortMap) : SortMap := left
def badContains (_key : SortKItem) (_map : SortMap) : SortBool := true
def badDelete (map : SortMap) (_key : SortKItem) : SortMap := map
def badElement (_key _value : SortKItem) : SortMap := ⟨[]⟩
def badNot (_value : SortBool) : SortBool := false

/- The generated proposition alone admits an operationally false bundle. -/
theorem counterfactual_target_still_provable :
    Klean70StrangeSortList.Lemmas.targetStatement
      badMap badContains badDelete badElement badNot := by
  intro K V M h
  rfl

/- Concrete witnesses that the counterfactual bundle is operationally false. -/
example (k v : SortKItem) : badElement k v = ⟨[]⟩ := by rfl
example (k : SortKItem) : badContains k ⟨[]⟩ = true := by rfl
example (k v : SortKItem) : badDelete ⟨[(k, v)]⟩ k = ⟨[(k, v)]⟩ := by rfl
example : badNot false = false := by rfl

/- Boundary witnesses for the candidate's five actual bindings. -/
example (k1 k2 v1 v2 : SortKItem) :
    Proof._Map_ ⟨[(k1, v1)]⟩ ⟨[(k2, v2)]⟩ =
      ⟨[(k1, v1), (k2, v2)]⟩ := by
  rfl

example (k v : SortKItem) : Proof.«_|->_» k v = ⟨[(k, v)]⟩ := by
  rfl

example : Proof.notBool_ true = false := by rfl
example : Proof.notBool_ false = true := by rfl

example (k : SortKItem) :
    Proof.«_in_keys(_)_MAP_Bool_KItem_Map» k ⟨[]⟩ = false := by
  rfl

example (k : SortKItem) : Proof.«_[_<-undef]» ⟨[]⟩ k = ⟨[]⟩ := by
  rfl

end OperationalBridgeTests
