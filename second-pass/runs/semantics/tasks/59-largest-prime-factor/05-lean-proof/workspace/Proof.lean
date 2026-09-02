import Klean59LargestPrimeFactor.Lemmas

namespace Proof

private noncomputable def sameKItem (x y : SortKItem) : Bool := by
  classical
  exact decide (x = y)

private noncomputable def containsKey
    (key : SortKItem) : List (SortKItem × SortKItem) → Bool
  | [] => false
  | (entryKey, _) :: rest =>
      sameKItem entryKey key || containsKey key rest

private noncomputable def deleteKey
    (key : SortKItem) : List (SortKItem × SortKItem) →
      List (SortKItem × SortKItem)
  | [] => []
  | entry :: rest =>
      if sameKItem entry.1 key then
        deleteKey key rest
      else
        entry :: deleteKey key rest

private theorem sameKItem_self (key : SortKItem) :
    sameKItem key key = true := by
  classical
  simp [sameKItem]

private theorem deleteKey_of_not_contains (key : SortKItem) :
    ∀ entries : List (SortKItem × SortKItem),
      containsKey key entries = false →
      deleteKey key entries = entries := by
  intro entries
  induction entries with
  | nil =>
      intro _
      rfl
  | cons entry rest ih =>
      intro h
      have hBoth :
          sameKItem entry.1 key = false ∧
            containsKey key rest = false := by
        simpa [containsKey] using h
      have hEntry := hBoth.1
      have hRest := hBoth.2
      simp [deleteKey, hEntry, ih hRest]

/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-fa3b6a435d659d4827ca8eeba38ca4416c9da4fd5da5bac92820eb663e7ddd84. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _Map_ (left right : SortMap) : SortMap :=
  ⟨left.coll ++ right.coll⟩
/- KORE symbol: Lbl'Unds'in'Unds'keys'LParUndsRParUnds'MAP'Unds'Bool'Unds'KItem'Unds'Map; frozen source obligations: rule-fa3b6a435d659d4827ca8eeba38ca4416c9da4fd5da5bac92820eb663e7ddd84. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_in_keys(_)_MAP_Bool_KItem_Map»
    (key : SortKItem) (map : SortMap) : SortBool :=
  containsKey key map.coll
/- KORE symbol: Lbl'UndsLSqBUnds-LT-'-undef'RSqB'; frozen source obligations: rule-fa3b6a435d659d4827ca8eeba38ca4416c9da4fd5da5bac92820eb663e7ddd84. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_[_<-undef]»
    (map : SortMap) (key : SortKItem) : SortMap :=
  ⟨deleteKey key map.coll⟩
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-fa3b6a435d659d4827ca8eeba38ca4416c9da4fd5da5bac92820eb663e7ddd84. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-fa3b6a435d659d4827ca8eeba38ca4416c9da4fd5da5bac92820eb663e7ddd84. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ (value : SortBool) : SortBool :=
  !value

theorem final :
    Klean59LargestPrimeFactor.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_[_<-undef]» «_|->_» notBool_ := by
  intro L M _V h
  let key := SortKItem.inj_SortInt L
  have hAbsent : containsKey key M.coll = false := by
    simpa [notBool_, «_in_keys(_)_MAP_Bool_KItem_Map», key] using h
  cases M with
  | mk entries =>
      apply congrArg SortMap.mk
      change
        deleteKey key
          ((key, SortKItem.inj_SortScope _V) :: entries) = entries
      rw [deleteKey, sameKItem_self]
      exact deleteKey_of_not_contains key entries hAbsent

end Proof
