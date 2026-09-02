import Klean77Iscube.Lemmas

namespace Proof

noncomputable section

private local instance : DecidableEq SortKItem :=
  Classical.typeDecidableEq SortKItem

private def tbMapContains
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Bool :=
  match entries with
  | [] => false
  | (candidate, _) :: rest =>
      if candidate = key then true else tbMapContains rest key

private def tbMapDelete
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => []
  | (candidate, value) :: rest =>
      if candidate = key then tbMapDelete rest key
      else (candidate, value) :: tbMapDelete rest key

private theorem tbMapDelete_eq_self_of_not_contains
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem)
    (h : tbMapContains entries key = false) :
    tbMapDelete entries key = entries := by
  induction entries with
  | nil => rfl
  | cons entry rest ih =>
      rcases entry with ⟨candidate, value⟩
      by_cases hkey : candidate = key
      · simp [tbMapContains, hkey] at h
      · simp only [tbMapContains, hkey, ↓reduceIte] at h
        simp only [tbMapDelete, hkey, ↓reduceIte, List.cons.injEq, true_and]
        exact ih h

private def tbCubeScan (a start : SortInt) : SortBool :=
  let radius := a.natAbs + 1
  (List.range (2 * radius + 1)).any fun offset =>
    let candidate : SortInt := (offset : Int) - (radius : Int)
    decide (start ≤ candidate ∧ (candidate * candidate) * candidate = a)

/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-6a2681616cee874c5a1856e102a2ab5794a9175a210318f62d58e2c74647c6a2. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _Map_ (left right : SortMap) : SortMap :=
  ⟨left.coll ++ right.coll⟩
/- KORE symbol: Lbl'Unds'in'Unds'keys'LParUndsRParUnds'MAP'Unds'Bool'Unds'KItem'Unds'Map; frozen source obligations: rule-6a2681616cee874c5a1856e102a2ab5794a9175a210318f62d58e2c74647c6a2. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_in_keys(_)_MAP_Bool_KItem_Map» (key : SortKItem) (map : SortMap) : SortBool :=
  tbMapContains map.coll key
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-050c02c309a5a530a8227be9add80d806c43948fb2a4cee44e6a4d8da7a1a71d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (left right : SortInt) : SortBool :=
  decide (left < right)
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-050c02c309a5a530a8227be9add80d806c43948fb2a4cee44e6a4d8da7a1a71d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (left right : SortInt) : SortBool :=
  decide (left = right)
/- KORE symbol: Lbl'UndsLSqBUnds-LT-'-undef'RSqB'; frozen source obligations: rule-6a2681616cee874c5a1856e102a2ab5794a9175a210318f62d58e2c74647c6a2. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_[_<-undef]» (map : SortMap) (key : SortKItem) : SortMap :=
  ⟨tbMapDelete map.coll key⟩
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-6a2681616cee874c5a1856e102a2ab5794a9175a210318f62d58e2c74647c6a2. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩
/- KORE symbol: Lbl'UndsStar'Int'Unds'; frozen source obligations: rule-050c02c309a5a530a8227be9add80d806c43948fb2a4cee44e6a4d8da7a1a71d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_*Int_» (left right : SortInt) : SortInt :=
  left * right
/- KORE symbol: LblcubeSearch'LParUndsCommUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'Int'Unds'Int; frozen source obligations: rule-050c02c309a5a530a8227be9add80d806c43948fb2a4cee44e6a4d8da7a1a71d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «cubeSearch(_,_)_VERIFICATION-SYNTAX_Bool_Int_Int»
    (a candidate : SortInt) : SortBool :=
  if (candidate * candidate) * candidate < a then tbCubeScan a candidate
  else decide ((candidate * candidate) * candidate = a)
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-050c02c309a5a530a8227be9add80d806c43948fb2a4cee44e6a4d8da7a1a71d, rule-6a2681616cee874c5a1856e102a2ab5794a9175a210318f62d58e2c74647c6a2. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ (value : SortBool) : SortBool :=
  !value

theorem final :
    Klean77Iscube.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_<Int_» «_==Int_» «_[_<-undef]» «_|->_» «_*Int_» «cubeSearch(_,_)_VERIFICATION-SYNTAX_Bool_Int_Int» notBool_ := by
  constructor
  · intro A I h
    have hExit : ¬(I * I) * I < A := by
      simpa [notBool_, «_<Int_», «_*Int_»] using h
    simp [«_==Int_», «_*Int_»,
      «cubeSearch(_,_)_VERIFICATION-SYNTAX_Bool_Int_Int», hExit]
  · intro REST S h
    have hAbsent :
        tbMapContains REST.coll (SortKItem.inj_SortInt 1) = false := by
      simpa [notBool_, «_in_keys(_)_MAP_Bool_KItem_Map»] using h
    rcases REST with ⟨entries⟩
    simp only [«_[_<-undef]», _Map_, «_|->_», List.singleton_append]
    simp only [tbMapDelete, ↓reduceIte]
    rw [tbMapDelete_eq_self_of_not_contains
      entries (SortKItem.inj_SortInt 1) hAbsent]

end

end Proof
