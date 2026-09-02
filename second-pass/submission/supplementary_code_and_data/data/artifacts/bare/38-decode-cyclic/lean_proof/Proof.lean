import Klean38DecodeCyclic.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-aa08fc7ab00f7ed5932bfabaec47fbf527e50b83d0b239787af7e592a9c05a9d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (x y : SortInt) : SortBool :=
  decide (x ≤ y)

/- KORE symbol: LblMap'Coln'update; frozen source obligations: rule-ef7d5d777b33ed834768f6d5eae1abcfc5bb3ea8e0391ad21da31281612828ec. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «Map:update» (m : SortMap) (key value : SortKItem) : SortMap := by
  classical
  exact
    ⟨(key, value) ::
      m.coll.filter (fun entry => decide (entry.1 ≠ key))⟩

/- KORE symbol: LbllengthString'LParUndsRParUnds'STRING-COMMON'Unds'Int'Unds'String; frozen source obligations: rule-aa08fc7ab00f7ed5932bfabaec47fbf527e50b83d0b239787af7e592a9c05a9d, rule-6a69a83530cb8d2469f0452d5b6878c9d18dc4dbc80234500bed171c1b093548. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «lengthString(_)_STRING-COMMON_Int_String» (s : SortString) : SortInt :=
  Int.ofNat s.length

/- KORE symbol: LblsubstrString'LParUndsCommUndsCommUndsRParUnds'STRING-COMMON'Unds'String'Unds'String'Unds'Int'Unds'Int; frozen source obligations: rule-6a69a83530cb8d2469f0452d5b6878c9d18dc4dbc80234500bed171c1b093548. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int»
    (s : SortString) (startIndex endIndex : SortInt) : SortString :=
  String.mk <|
    (s.toList.drop startIndex.toNat).take (endIndex - startIndex).toNat

theorem final :
    Klean38DecodeCyclic.Lemmas.targetStatement «_<=Int_» «Map:update» «lengthString(_)_STRING-COMMON_Int_String» «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» := by
  constructor
  · intro V' K M V
    constructor
    · intro h
      have hcoll := congrArg SortMap.coll h
      simpa [«Map:update»] using hcoll
    · intro h
      subst V'
      rfl
  constructor
  · intro S
    simp [«_<=Int_», «lengthString(_)_STRING-COMMON_Int_String»]
  · intro S
    cases S with
    | mk data =>
      simp [«substrString(_,_,_)_STRING-COMMON_String_String_Int_Int»,
        «lengthString(_)_STRING-COMMON_Int_String»]

end Proof
