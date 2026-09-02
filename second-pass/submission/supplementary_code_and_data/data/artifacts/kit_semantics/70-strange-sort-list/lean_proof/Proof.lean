import Klean70StrangeSortList.Lemmas

namespace Proof

noncomputable local instance : DecidableEq SortKItem :=
  Classical.typeDecidableEq SortKItem

private noncomputable def proofMapContains
    (key : SortKItem) : List (SortKItem × SortKItem) → Bool
  | [] => false
  | (candidate, _) :: rest =>
      if candidate = key then true else proofMapContains key rest

private noncomputable def proofMapDelete
    (key : SortKItem) : List (SortKItem × SortKItem) → List (SortKItem × SortKItem)
  | [] => []
  | (candidate, value) :: rest =>
      if candidate = key then proofMapDelete key rest
      else (candidate, value) :: proofMapDelete key rest

private theorem proofMapDelete_append_singleton_of_not_contains
    (key value : SortKItem)
    (entries : List (SortKItem × SortKItem))
    (h : proofMapContains key entries = false) :
    proofMapDelete key (entries ++ [(key, value)]) = entries := by
  induction entries with
  | nil =>
      simp [proofMapDelete]
  | cons head rest ih =>
      rcases head with ⟨candidate, oldValue⟩
      by_cases hkey : candidate = key
      · simp [proofMapContains, hkey] at h
      · simp [proofMapContains, hkey] at h
        simp [proofMapDelete, hkey, ih h]

/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-565182bf10d31fb24d96318e023c71c80005ab90c1b99978f05bb734ef394503. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _Map_ (left right : SortMap) : SortMap :=
  ⟨left.coll ++ right.coll⟩
/- KORE symbol: Lbl'Unds'in'Unds'keys'LParUndsRParUnds'MAP'Unds'Bool'Unds'KItem'Unds'Map; frozen source obligations: rule-565182bf10d31fb24d96318e023c71c80005ab90c1b99978f05bb734ef394503. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_in_keys(_)_MAP_Bool_KItem_Map»
    (key : SortKItem) (map : SortMap) : SortBool :=
  proofMapContains key map.coll
/- KORE symbol: Lbl'UndsLSqBUnds-LT-'-undef'RSqB'; frozen source obligations: rule-565182bf10d31fb24d96318e023c71c80005ab90c1b99978f05bb734ef394503. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_[_<-undef]» (map : SortMap) (key : SortKItem) : SortMap :=
  ⟨proofMapDelete key map.coll⟩
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-565182bf10d31fb24d96318e023c71c80005ab90c1b99978f05bb734ef394503. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-565182bf10d31fb24d96318e023c71c80005ab90c1b99978f05bb734ef394503. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ (value : SortBool) : SortBool :=
  !value

theorem final :
    Klean70StrangeSortList.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_[_<-undef]» «_|->_» notBool_ := by
  intro K _V M h
  let key := SortKItem.inj_SortInt K
  let value := SortKItem.inj_SortScope _V
  have hnot : proofMapContains key M.coll = false := by
    cases hcontains : proofMapContains key M.coll with
    | false => rfl
    | true =>
        simp [notBool_, «_in_keys(_)_MAP_Bool_KItem_Map», key, hcontains] at h
  rcases M with ⟨entries⟩
  change SortMap.mk (proofMapDelete key (entries ++ [(key, value)])) = SortMap.mk entries
  exact congrArg SortMap.mk
    (proofMapDelete_append_singleton_of_not_contains key value entries hnot)

end Proof
