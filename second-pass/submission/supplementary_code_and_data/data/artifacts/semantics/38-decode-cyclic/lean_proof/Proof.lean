import Klean38DecodeCyclic.Lemmas

namespace Proof

def intSeqToList : SortIntSeq → List SortInt
  | .«.IntSeq_MPY-CORE_IntSeq» => []
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs => x :: intSeqToList xs

def listToIntSeq : List SortInt → SortIntSeq
  | [] => .«.IntSeq_MPY-CORE_IntSeq»
  | x :: xs => .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x (listToIntSeq xs)

def intSeqGet? (xs : List SortInt) (i : SortInt) : Option SortInt :=
  if i < 0 then none else xs[i.toNat]?

def buildISAux
    (xs : List SortInt) (stop step : SortInt) :
    Nat → SortInt → List SortInt
  | 0, _ => []
  | fuel + 1, i =>
      if (0 < step ∧ i < stop) ∨ (step < 0 ∧ stop < i) then
        match intSeqGet? xs i with
        | some x => x :: buildISAux xs stop step fuel (i + step)
        | none => []
      else
        []

noncomputable def kItemEq (a b : SortKItem) : Bool :=
  @ite Bool (a = b) (Classical.propDecidable (a = b)) true false

noncomputable def eraseMapKey (key : SortKItem) :
    List (SortKItem × SortKItem) → List (SortKItem × SortKItem)
  | [] => []
  | entry :: rest =>
      if kItemEq key entry.1 then
        eraseMapKey key rest
      else
        entry :: eraseMapKey key rest

def mapEntryBelow (entry : SortKItem × SortKItem) (bound : SortInt) : Bool :=
  match entry.1 with
  | .inj_SortInt key => decide (key < bound)
  | _ => false

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-4281e752ff9a8d5db579bbac5643ad5601381eaf22b096d29d92335d12d66f5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» (a b : SortInt) : SortInt := a - b
/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-f0db16212bf58f7561bc29b239623e9a2ac5f7372a7228b99c3baf953e83b63c, rule-d7d11f1fc9fe34f62521436622edf9d5bea2ea8bfb4c788542b09eb6d23ffab9. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _Map_ (left right : SortMap) : SortMap :=
  ⟨left.coll ++ right.coll⟩
/- KORE symbol: Lbl'Unds'in'Unds'keys'LParUndsRParUnds'MAP'Unds'Bool'Unds'KItem'Unds'Map; frozen source obligations: rule-75fa33282a96ce93976534a56a3cbca68ee1b3b3369c99ec1a39f0690d886745. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_in_keys(_)_MAP_Bool_KItem_Map»
    (key : SortKItem) (map : SortMap) : SortBool :=
  map.coll.any (fun entry => kItemEq key entry.1)
/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-4281e752ff9a8d5db579bbac5643ad5601381eaf22b096d29d92335d12d66f5d, rule-e4afafd317ff2760b1290163a9583c9ff2cefc541daf634480a32a004199a9f2. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>=Int_» (a b : SortInt) : SortBool := decide (a ≥ b)
/- KORE symbol: Lbl'UndsLSqBUnds-LT-'-undef'RSqB'; frozen source obligations: rule-d7d11f1fc9fe34f62521436622edf9d5bea2ea8bfb4c788542b09eb6d23ffab9. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_[_<-undef]» (map : SortMap) (key : SortKItem) : SortMap :=
  ⟨eraseMapKey key map.coll⟩
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-f0db16212bf58f7561bc29b239623e9a2ac5f7372a7228b99c3baf953e83b63c, rule-d7d11f1fc9fe34f62521436622edf9d5bea2ea8bfb4c788542b09eb6d23ffab9. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-12b6390dc702f6660b47ee0c0a9b53b2797cbb240846a822a143c2125bd020b7. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (a b : SortInt) : SortInt := a + b
/- KORE symbol: LblMap'Coln'update; frozen source obligations: rule-f0db16212bf58f7561bc29b239623e9a2ac5f7372a7228b99c3baf953e83b63c. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «Map:update» (map : SortMap) (key value : SortKItem) : SortMap :=
  ⟨(key, value) :: eraseMapKey key map.coll⟩
/- KORE symbol: LblbuildIS'LParUndsCommUndsCommUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'IntSeq'Unds'IntSeq'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-4281e752ff9a8d5db579bbac5643ad5601381eaf22b096d29d92335d12d66f5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int»
    (seq : SortIntSeq) (start stop step : SortInt) : SortIntSeq :=
  let xs := intSeqToList seq
  if step = 1 then
    listToIntSeq ((xs.drop start.toNat).take (stop - start).toNat)
  else
    listToIntSeq (buildISAux xs stop step xs.length start)
/- KORE symbol: LblclampHi'LParUndsCommUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Int'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-4281e752ff9a8d5db579bbac5643ad5601381eaf22b096d29d92335d12d66f5d, rule-e4afafd317ff2760b1290163a9583c9ff2cefc541daf634480a32a004199a9f2. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int»
    (index len step : SortInt) : SortInt :=
  if index < len then index else if step < 0 then len - 1 else len
/- KORE symbol: LblisLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'IntSeq; frozen source obligations: rule-4281e752ff9a8d5db579bbac5643ad5601381eaf22b096d29d92335d12d66f5d, rule-e4afafd317ff2760b1290163a9583c9ff2cefc541daf634480a32a004199a9f2. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isLen(_)_MPY-CORE_Int_IntSeq» (seq : SortIntSeq) : SortInt :=
  Int.ofNat (intSeqToList seq).length
/- KORE symbol: LblkeysBelow'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Map'Unds'Int; frozen source obligations: rule-12b6390dc702f6660b47ee0c0a9b53b2797cbb240846a822a143c2125bd020b7, rule-75fa33282a96ce93976534a56a3cbca68ee1b3b3369c99ec1a39f0690d886745, rule-f0db16212bf58f7561bc29b239623e9a2ac5f7372a7228b99c3baf953e83b63c, rule-d7d11f1fc9fe34f62521436622edf9d5bea2ea8bfb4c788542b09eb6d23ffab9. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «keysBelow(_,_)_VERIFICATION_Bool_Map_Int»
    (map : SortMap) (bound : SortInt) : SortBool :=
  map.coll.all (fun entry => mapEntryBelow entry bound)

@[simp] theorem intSeqToList_listToIntSeq (xs : List SortInt) :
    intSeqToList (listToIntSeq xs) = xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp [listToIntSeq, intSeqToList, ih]

theorem mapEntryBelow_succ
    (entry : SortKItem × SortKItem) (bound : SortInt)
    (h : mapEntryBelow entry bound = true) :
    mapEntryBelow entry (bound + 1) = true := by
  rcases entry with ⟨key, value⟩
  cases key <;> simp [mapEntryBelow] at h ⊢
  rename_i key
  change Int at key bound
  exact Int.lt_trans h (Int.lt_add_succ bound 0)

theorem mapEntriesBelow_succ
    (entries : List (SortKItem × SortKItem)) (bound : SortInt)
    (h : entries.all (fun entry => mapEntryBelow entry bound) = true) :
    entries.all (fun entry => mapEntryBelow entry (bound + 1)) = true := by
  induction entries with
  | nil => rfl
  | cons entry entries ih =>
      simp only [List.all_cons, Bool.and_eq_true] at h ⊢
      exact ⟨mapEntryBelow_succ entry bound h.1, ih h.2⟩

theorem mapEntryBelow_ne_boundary
    (entry : SortKItem × SortKItem) (bound : SortInt)
    (h : mapEntryBelow entry bound = true) :
    kItemEq (.inj_SortInt bound) entry.1 = false := by
  rcases entry with ⟨key, value⟩
  cases key <;> simp [mapEntryBelow] at h
  rename_i key
  have hne : bound ≠ key := (Int.ne_of_lt h).symm
  simp [kItemEq, hne]

theorem mapEntriesBelow_not_mem
    (entries : List (SortKItem × SortKItem)) (bound : SortInt)
    (h : entries.all (fun entry => mapEntryBelow entry bound) = true) :
    entries.any (fun entry => kItemEq (.inj_SortInt bound) entry.1) = false := by
  induction entries with
  | nil => rfl
  | cons entry entries ih =>
      simp only [List.all_cons, Bool.and_eq_true] at h
      simp [mapEntryBelow_ne_boundary entry bound h.1, ih h.2]

theorem unitSliceLengthFromThree
    (xs : List SortInt)
    (h : (3 : Int) ≤ Int.ofNat xs.length) :
    Int.ofNat
        (((xs.drop 3).take (Int.ofNat xs.length - 3).toNat).length) =
      Int.ofNat xs.length - 3 := by
  simp only [List.length_take, List.length_drop]
  have hcount :
      (Int.ofNat xs.length - (3 : Int)).toNat = xs.length - 3 :=
    Int.toNat_sub' (Int.ofNat xs.length) 3
  rw [hcount, Nat.min_self, ← hcount]
  exact Int.toNat_of_nonneg (Int.sub_nonneg.mpr h)

theorem final :
    Klean38DecodeCyclic.Lemmas.targetStatement «_-Int_» _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_>=Int_» «_[_<-undef]» «_|->_» «_+Int_» «Map:update» «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» «isLen(_)_MPY-CORE_Int_IntSeq» «keysBelow(_,_)_VERIFICATION_Bool_Map_Int» := by
  unfold Klean38DecodeCyclic.Lemmas.targetStatement
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro CS h
    simp only [«_>=Int_», decide_eq_true_eq] at h
    have hclamp :
        «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int»
            3 («isLen(_)_MPY-CORE_Int_IntSeq» CS) 1 = 3 := by
      simp only [«clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int»]
      split
      · rfl
      · split
        · simp_all
        · exact Int.le_antisymm
            (Int.le_of_not_gt
              ‹¬3 < «isLen(_)_MPY-CORE_Int_IntSeq» CS›)
            h
    rw [hclamp]
    simpa [
      «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int»,
      «isLen(_)_MPY-CORE_Int_IntSeq»,
      «_-Int_»
    ] using (unitSliceLengthFromThree (intSeqToList CS) h)
  · intro CS h
    simp only [«_>=Int_», decide_eq_true_eq] at h
    simp only [«clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int»]
    split
    · rfl
    · split
      · simp_all
      · exact Int.le_antisymm
          (Int.le_of_not_gt
            ‹¬3 < «isLen(_)_MPY-CORE_Int_IntSeq» CS›)
          h
  · intro N M h
    cases M with
    | mk entries =>
        exact mapEntriesBelow_succ entries N h
  · intro M N h
    cases M with
    | mk entries =>
        exact mapEntriesBelow_not_mem entries N h
  · intro S
    exact nomatch S
  · intro N M S
    exact nomatch S

end Proof
