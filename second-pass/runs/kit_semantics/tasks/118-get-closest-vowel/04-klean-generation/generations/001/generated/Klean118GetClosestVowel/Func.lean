import Klean118GetClosestVowel.Inj

noncomputable local instance : DecidableEq SortKItem :=
  Classical.typeDecidableEq SortKItem

private noncomputable def kleanMapLookupModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Option SortKItem :=
  match entries with
  | [] => none
  | (candidate, value) :: rest =>
      if candidate = key then some value
      else kleanMapLookupModel rest key

private noncomputable def kleanMapContainsModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Bool :=
  match entries with
  | [] => false
  | (candidate, _) :: rest =>
      if candidate = key then true
      else kleanMapContainsModel rest key

private noncomputable def kleanMapDisjointModel
    (left right : List (SortKItem × SortKItem)) : Bool :=
  match right with
  | [] => true
  | (key, _) :: rest =>
      if kleanMapContainsModel left key then false
      else kleanMapDisjointModel left rest

private noncomputable def kleanMapDeleteModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => []
  | (candidate, value) :: rest =>
      if candidate = key then kleanMapDeleteModel rest key
      else (candidate, value) :: kleanMapDeleteModel rest key

private noncomputable def kleanKeyOrderModel : SortKItem → SortKItem → Bool
  | SortKItem.inj_SortInt a,    SortKItem.inj_SortInt b    => decide (a < b)
  | SortKItem.inj_SortInt _,    _                          => true
  | _,                          SortKItem.inj_SortInt _    => false
  | SortKItem.inj_SortString a, SortKItem.inj_SortString b => decide (a < b)
  | SortKItem.inj_SortString _, _                          => true
  | _,                          SortKItem.inj_SortString _ => false
  | _, _ => false

private noncomputable def kleanMapInsertModel
    (key value : SortKItem) :
    List (SortKItem × SortKItem) → List (SortKItem × SortKItem)
  | [] => [(key, value)]
  | (candidate, oldValue) :: rest =>
      if kleanKeyOrderModel candidate key then
        (candidate, oldValue) :: kleanMapInsertModel key value rest
      else (key, value) :: (candidate, oldValue) :: rest

private noncomputable def kleanMapUpdateModel
    (entries : List (SortKItem × SortKItem))
    (key value : SortKItem) : List (SortKItem × SortKItem) :=
  kleanMapInsertModel key value (kleanMapDeleteModel entries key)

noncomputable def «.List» : Option SortList := some ⟨[]⟩

noncomputable def «.Map» : Option SortMap := some ⟨[]⟩

noncomputable def _List_ (x0 : SortList) (x1 : SortList) : Option SortList := some ⟨x0.coll ++ x1.coll⟩

noncomputable def _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap :=
  if kleanMapDisjointModel x0.coll x1.coll then
    some ⟨x0.coll.foldr
      (fun kv acc => kleanMapInsertModel kv.1 kv.2 acc)
      x1.coll⟩
  else none

noncomputable def «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=
  some ⟨[(x0, x1)]⟩

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩