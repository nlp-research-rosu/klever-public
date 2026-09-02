import Klean24LargestDivisor.Lemmas

namespace Proof

/- Frozen MPY maps use integer keys for frame/heap locations and string keys
   for Python bindings.  This is the structural equality on that operational
   key domain. -/
def sameMapKey : SortKItem → SortKItem → SortBool
  | .inj_SortInt a, .inj_SortInt b => decide (a = b)
  | .inj_SortString a, .inj_SortString b => decide (a = b)
  | _, _ => false

/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-feff944e2f19f17c55e3bc4182bfa0059f8872fc9fa1462060bd73b09293f630. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _Map_ (left right : SortMap) : SortMap :=
  ⟨left.coll ++ right.coll⟩
/- KORE symbol: Lbl'Unds'in'Unds'keys'LParUndsRParUnds'MAP'Unds'Bool'Unds'KItem'Unds'Map; frozen source obligations: rule-feff944e2f19f17c55e3bc4182bfa0059f8872fc9fa1462060bd73b09293f630. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_in_keys(_)_MAP_Bool_KItem_Map» (key : SortKItem) (map : SortMap) : SortBool :=
  map.coll.any fun entry => sameMapKey key entry.1
/- KORE symbol: Lbl'UndsLSqBUnds-LT-'-undef'RSqB'; frozen source obligations: rule-feff944e2f19f17c55e3bc4182bfa0059f8872fc9fa1462060bd73b09293f630. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_[_<-undef]» (map : SortMap) (key : SortKItem) : SortMap :=
  ⟨map.coll.filter fun entry => !sameMapKey key entry.1⟩
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-feff944e2f19f17c55e3bc4182bfa0059f8872fc9fa1462060bd73b09293f630. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-feff944e2f19f17c55e3bc4182bfa0059f8872fc9fa1462060bd73b09293f630. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ (value : SortBool) : SortBool :=
  !value

theorem filter_not_sameMapKey_of_any_eq_false
    (key : SortKItem)
    (entries : List (SortKItem × SortKItem))
    (h : entries.any (fun entry => sameMapKey key entry.1) = false) :
    entries.filter (fun entry => !sameMapKey key entry.1) = entries := by
  induction entries with
  | nil =>
      rfl
  | cons head tail ih =>
      cases hHead : sameMapKey key head.1 with
      | false =>
          have hTail : tail.any (fun entry => sameMapKey key entry.1) = false := by
            simpa [hHead] using h
          simp [hHead, ih hTail]
      | true =>
          simp [hHead] at h

theorem final :
    Klean24LargestDivisor.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_[_<-undef]» «_|->_» notBool_ := by
  unfold Klean24LargestDivisor.Lemmas.targetStatement
  intro SC _S h
  have hAbsent :
      SC.coll.any (fun entry =>
        sameMapKey (SortKItem.inj_SortInt 1) entry.1) = false := by
    simpa [notBool_, «_in_keys(_)_MAP_Bool_KItem_Map»] using h
  cases SC with
  | mk entries =>
      have hFilter :
          entries.filter (fun entry =>
            !sameMapKey (SortKItem.inj_SortInt 1) entry.1) = entries :=
        filter_not_sameMapKey_of_any_eq_false _ _ hAbsent
      simp only [_Map_, «_|->_», «_[_<-undef]»]
      congr 1

end Proof
