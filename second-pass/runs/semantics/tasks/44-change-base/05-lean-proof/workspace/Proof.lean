import Klean44ChangeBase.Lemmas

namespace Proof

/- Equality on generated K items.  The generated syntax is inductive but does
   not expose a DecidableEq instance, so use total classical decidable
   equality to implement the map hooks. -/
noncomputable def kItemEq (a b : SortKItem) : Bool := by
  classical
  exact decide (a = b)

/- K map concatenation is disjoint union.  Generated SortMap values use an
   association list; append is its total implementation and agrees with K on
   well-formed maps, whose operand keys are disjoint. -/
/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-746c49465cb8335d005b3a331b93eb26bdf586974933b9d025250760d4d0c29d, rule-82f2c726c84180f9e0c75a16a31dd3a15476f84ccb4dacad03db18bcaca52fda. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _Map_ (left right : SortMap) : SortMap :=
  ⟨left.coll ++ right.coll⟩

/- K's in_keys hook observes association-list key membership. -/
/- KORE symbol: Lbl'Unds'in'Unds'keys'LParUndsRParUnds'MAP'Unds'Bool'Unds'KItem'Unds'Map; frozen source obligations: rule-437465420fc6223721ad7c1f90c24fba6434c7a8d0b69e9c65c7139faac9cb24, rule-746c49465cb8335d005b3a331b93eb26bdf586974933b9d025250760d4d0c29d, rule-82f2c726c84180f9e0c75a16a31dd3a15476f84ccb4dacad03db18bcaca52fda. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_in_keys(_)_MAP_Bool_KItem_Map»
    (key : SortKItem) (map : SortMap) : SortBool :=
  map.coll.any (fun entry => kItemEq entry.1 key)

/- K's [key <- undef] removes the key binding.  Filtering all occurrences is
   total and agrees with well-formed K maps, where keys are unique. -/
/- KORE symbol: Lbl'UndsLSqBUnds-LT-'-undef'RSqB'; frozen source obligations: rule-82f2c726c84180f9e0c75a16a31dd3a15476f84ccb4dacad03db18bcaca52fda. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_[_<-undef]»
    (map : SortMap) (key : SortKItem) : SortMap :=
  ⟨map.coll.filter (fun entry => !(kItemEq entry.1 key))⟩

/- A K map entry is a singleton association map. -/
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-746c49465cb8335d005b3a331b93eb26bdf586974933b9d025250760d4d0c29d, rule-82f2c726c84180f9e0c75a16a31dd3a15476f84ccb4dacad03db18bcaca52fda. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩

/- Map:update replaces a previous key binding, if present, and installs the
   supplied key/value association. -/
/- KORE symbol: LblMap'Coln'update; frozen source obligations: rule-746c49465cb8335d005b3a331b93eb26bdf586974933b9d025250760d4d0c29d. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «Map:update»
    (map : SortMap) (key value : SortKItem) : SortMap :=
  ⟨(key, value) :: («_[_<-undef]» map key).coll⟩

/- The allocator invariant from verification.k: every integer location in the
   frame-map suffix precedes the next fresh location.  Other key sorts cannot
   be scope locations. -/
def priorScopeKey (next : SortInt) (entry : SortKItem × SortKItem) : Bool :=
  match entry.1 with
  | SortKItem.inj_SortInt location => decide (location < next)
  | _ => false

/- KORE symbol: LblfreshScopes'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Int'Unds'Map; frozen source obligations: rule-437465420fc6223721ad7c1f90c24fba6434c7a8d0b69e9c65c7139faac9cb24. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «freshScopes(_,_)_VERIFICATION_Bool_Int_Map»
    (next : SortInt) (map : SortMap) : SortBool :=
  map.coll.all (priorScopeKey next)

/- K Boolean negation. -/
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-746c49465cb8335d005b3a331b93eb26bdf586974933b9d025250760d4d0c29d, rule-82f2c726c84180f9e0c75a16a31dd3a15476f84ccb4dacad03db18bcaca52fda. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ : SortBool → SortBool := Bool.not

theorem allPriorKeysExcludeNext
    (entries : List (SortKItem × SortKItem))
    (next : SortInt)
    (h : entries.all (priorScopeKey next) = true) :
    entries.any (fun entry =>
      kItemEq entry.1 (SortKItem.inj_SortInt next)) = false := by
  induction entries with
  | nil => rfl
  | cons entry rest ih =>
    rcases entry with ⟨key, value⟩
    rw [List.all_cons, Bool.and_eq_true] at h
    rcases h with ⟨headPrior, restPrior⟩
    rw [List.any_cons]
    by_cases keyIsNext : key = SortKItem.inj_SortInt next
    · subst key
      simp [priorScopeKey] at headPrior
    · have keyDoesNotMatch :
          kItemEq key (SortKItem.inj_SortInt next) = false := by
        simp [kItemEq, keyIsNext]
      rw [keyDoesNotMatch]
      exact ih restPrior

theorem filterNotKey_eq_self
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem)
    (h : entries.any (fun entry => kItemEq entry.1 key) = false) :
    entries.filter (fun entry => !(kItemEq entry.1 key)) = entries := by
  induction entries with
  | nil => rfl
  | cons entry rest ih =>
    rcases entry with ⟨entryKey, entryValue⟩
    by_cases entryMatches : entryKey = key
    · subst entryKey
      simp [kItemEq] at h
    · have headDoesNotMatch : kItemEq entryKey key = false := by
        simp [kItemEq, entryMatches]
      have restDoesNotContain :
          rest.any (fun pair => kItemEq pair.1 key) = false := by
        simpa [headDoesNotMatch] using h
      simp [headDoesNotMatch, ih restDoesNotContain]

theorem final :
    Klean44ChangeBase.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_[_<-undef]» «_|->_» «Map:update» «freshScopes(_,_)_VERIFICATION_Bool_Int_Map» notBool_ := by
  constructor
  · intro S L h
    rcases S with ⟨entries⟩
    exact allPriorKeysExcludeNext entries L h
  constructor
  · intro V L S h
    rcases S with ⟨entries⟩
    have keyAbsent :
        entries.any (fun entry =>
          kItemEq entry.1 (SortKItem.inj_SortInt L)) = false := by
      simpa [
        notBool_,
        «_in_keys(_)_MAP_Bool_KItem_Map»
      ] using h
    have deletionIsIdentity :=
      filterNotKey_eq_self
        entries
        (SortKItem.inj_SortInt L)
        keyAbsent
    change
      SortMap.mk
          ((SortKItem.inj_SortInt L, SortKItem.inj_SortScope V) ::
            entries.filter (fun entry =>
              !(kItemEq entry.1 (SortKItem.inj_SortInt L)))) =
        SortMap.mk
          ((SortKItem.inj_SortInt L, SortKItem.inj_SortScope V) ::
            entries)
    rw [deletionIsIdentity]
  · intro L S V
    intro h
    rcases S with ⟨entries⟩
    have keyAbsent :
        entries.any (fun entry =>
          kItemEq entry.1 (SortKItem.inj_SortInt L)) = false := by
      simpa [
        notBool_,
        «_in_keys(_)_MAP_Bool_KItem_Map»
      ] using h
    have deletionIsIdentity :=
      filterNotKey_eq_self
        entries
        (SortKItem.inj_SortInt L)
        keyAbsent
    change
      SortMap.mk
          (((SortKItem.inj_SortInt L, SortKItem.inj_SortScope V) ::
            entries).filter (fun entry =>
              !(kItemEq entry.1 (SortKItem.inj_SortInt L)))) =
        SortMap.mk entries
    simp only [List.filter_cons]
    have selfMatches :
        kItemEq
          (SortKItem.inj_SortInt L)
          (SortKItem.inj_SortInt L) = true := by
      simp [kItemEq]
    rw [selfMatches]
    simp only [Bool.not_true, Bool.false_eq_true, ↓reduceIte]
    rw [deletionIsIdentity]

end Proof
