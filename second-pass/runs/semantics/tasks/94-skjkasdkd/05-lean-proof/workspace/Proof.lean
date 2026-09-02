import Klean94Skjkasdkd.Lemmas

namespace Proof

/- The generated `SortMap` is a list of key/value pairs.  K's map hooks are
   represented here by the corresponding total list operations.  Equality of
   generated K items is mathematical equality; `Classical.decEq` only supplies
   a decision procedure for that equality and does not add an equation. -/
private noncomputable def sameKey (left right : SortKItem) : Bool := by
  classical
  exact decide (left = right)

/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-75f08df4443da8a48ee02cff10c65980b5cd03f6f6f15985f63ba60ad2f96854, rule-cd6fef5d8c48828cab2f7185fc582c06349b39cd6c4a267fac6bc46b6ba7413b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _Map_ (left right : SortMap) : SortMap :=
  ⟨left.coll ++ right.coll⟩
/- KORE symbol: Lbl'Unds'in'Unds'keys'LParUndsRParUnds'MAP'Unds'Bool'Unds'KItem'Unds'Map; frozen source obligations: rule-75f08df4443da8a48ee02cff10c65980b5cd03f6f6f15985f63ba60ad2f96854, rule-cd6fef5d8c48828cab2f7185fc582c06349b39cd6c4a267fac6bc46b6ba7413b. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_in_keys(_)_MAP_Bool_KItem_Map»
    (key : SortKItem) (map : SortMap) : SortBool :=
  map.coll.any (fun entry => sameKey entry.1 key)
/- KORE symbol: Lbl'UndsLSqBUnds-LT-'-undef'RSqB'; frozen source obligations: rule-75f08df4443da8a48ee02cff10c65980b5cd03f6f6f15985f63ba60ad2f96854. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_[_<-undef]» (map : SortMap) (key : SortKItem) : SortMap :=
  ⟨map.coll.filter (fun entry => !(sameKey entry.1 key))⟩
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-75f08df4443da8a48ee02cff10c65980b5cd03f6f6f15985f63ba60ad2f96854, rule-cd6fef5d8c48828cab2f7185fc582c06349b39cd6c4a267fac6bc46b6ba7413b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩
/- KORE symbol: LblMap'Coln'update; frozen source obligations: rule-cd6fef5d8c48828cab2f7185fc582c06349b39cd6c4a267fac6bc46b6ba7413b. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «Map:update»
    (map : SortMap) (key value : SortKItem) : SortMap :=
  ⟨(key, value) :: map.coll.filter (fun entry => !(sameKey entry.1 key))⟩
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-75f08df4443da8a48ee02cff10c65980b5cd03f6f6f15985f63ba60ad2f96854, rule-cd6fef5d8c48828cab2f7185fc582c06349b39cd6c4a267fac6bc46b6ba7413b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ (value : SortBool) : SortBool :=
  !value

private theorem filter_missing_key
    (key : SortKItem) (entries : List (SortKItem × SortKItem))
    (h : !(entries.any (fun entry => sameKey entry.1 key)) = true) :
    entries.filter (fun entry => !(sameKey entry.1 key)) = entries := by
  induction entries with
  | nil =>
      rfl
  | cons entry rest ih =>
      cases hkey : sameKey entry.1 key with
      | false =>
          have hrest :
              !(rest.any (fun item => sameKey item.1 key)) = true := by
            simpa [hkey] using h
          rw [List.filter_cons]
          simp only [hkey, Bool.not_false, if_true]
          rw [ih hrest]
      | true =>
          simp [hkey] at h

theorem final :
    Klean94Skjkasdkd.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_[_<-undef]» «_|->_» «Map:update» notBool_ := by
  constructor
  · intro X M _Gen0 h
    cases M with
    | mk entries =>
        have hfilter :
            entries.filter (fun entry => !(sameKey entry.1 X)) = entries :=
          filter_missing_key X entries (by
            simpa [notBool_, «_in_keys(_)_MAP_Bool_KItem_Map»] using h)
        have hdeleted :
            ((X, _Gen0) :: entries).filter
                (fun entry => !(sameKey entry.1 X)) = entries := by
          simpa [sameKey] using hfilter
        simpa [_Map_, «_|->_», «_[_<-undef]»] using
          congrArg SortMap.mk hdeleted
  · intro V X M h
    cases M with
    | mk entries =>
        have hfilter :
            entries.filter (fun entry => !(sameKey entry.1 X)) = entries :=
          filter_missing_key X entries (by
            simpa [notBool_, «_in_keys(_)_MAP_Bool_KItem_Map»] using h)
        have hupdated :
            (X, V) :: entries.filter (fun entry => !(sameKey entry.1 X)) =
              (X, V) :: entries :=
          congrArg (List.cons (X, V)) hfilter
        simpa [_Map_, «_|->_», «Map:update»] using
          congrArg SortMap.mk hupdated

end Proof
