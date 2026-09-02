import Proof

namespace AuditBridge

def key0 : SortKItem := SortKItem.inj_SortInt 0
def key1 : SortKItem := SortKItem.inj_SortInt 1
def value : SortKItem := SortKItem.inj_SortInt 2
def left : SortMap := ⟨[(key0, value)]⟩
def right : SortMap := ⟨[(key1, value)]⟩

theorem candidate_Map_is_not_commutative :
    Proof._Map_ left right ≠ Proof._Map_ right left := by
  intro h
  have hcoll := congrArg SortMap.coll h
  simp [Proof._Map_, left, right, key0, key1, value] at hcoll

end AuditBridge
