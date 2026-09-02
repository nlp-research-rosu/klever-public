import Klean37SortEven.Lemmas
import Init.Classical

namespace Proof

/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-e4098f840641d982cc071ea690be2438850392507ef1b3d1e9de094705d06500. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _Map_ (left right : SortMap) : SortMap :=
  ⟨left.coll ++ right.coll⟩
/- KORE symbol: Lbl'Unds'in'Unds'keys'LParUndsRParUnds'MAP'Unds'Bool'Unds'KItem'Unds'Map; frozen source obligations: rule-e4098f840641d982cc071ea690be2438850392507ef1b3d1e9de094705d06500. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_in_keys(_)_MAP_Bool_KItem_Map»
    (key : SortKItem) (map : SortMap) : SortBool :=
  map.coll.any fun entry =>
    match Classical.typeDecidableEq SortKItem key entry.1 with
    | .isTrue _ => true
    | .isFalse _ => false
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-e4098f840641d982cc071ea690be2438850392507ef1b3d1e9de094705d06500. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩
/- KORE symbol: LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq; frozen source obligations: rule-656b75764c3203134f266be9408944fcc82d61f11a51b6ca12049b4e0fddc5cb, rule-654c2f49cd7e7e59ab81408e4712d1a42c74c6bd59416f943395163de8bed937. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
    (left right : SortValSeq) : SortValSeq :=
  match left with
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => right
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        value
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» rest right)
  termination_by left

theorem final :
    Klean37SortEven.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_|->_» «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» := by
  unfold Klean37SortEven.Lemmas.targetStatement
  constructor
  · intro VS
    induction VS using «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq».induct with
    | case1 =>
        simp [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»]
    | case2 value rest ih =>
        simp [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq», ih]
  · constructor
    · intro C B A
      induction A using «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq».induct with
      | case1 =>
          simp [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»]
      | case2 value rest ih =>
          simp [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq», ih]
    · intro M _ODD _IV _RV _OV _EV
      have evensNe :
          SortKItem.inj_SortString "$cells" ≠ SortKItem.inj_SortString "evens" := by
        simp
      have oddsNe :
          SortKItem.inj_SortString "$cells" ≠ SortKItem.inj_SortString "odds" := by
        simp
      have resultNe :
          SortKItem.inj_SortString "$cells" ≠ SortKItem.inj_SortString "result" := by
        simp
      have iNe :
          SortKItem.inj_SortString "$cells" ≠ SortKItem.inj_SortString "i" := by
        simp
      have oddNe :
          SortKItem.inj_SortString "$cells" ≠ SortKItem.inj_SortString "odd" := by
        simp
      simp [_Map_, «_|->_», «_in_keys(_)_MAP_Bool_KItem_Map»]
      cases Classical.typeDecidableEq SortKItem
          (SortKItem.inj_SortString "$cells") (SortKItem.inj_SortString "evens") with
      | isTrue h => exact (evensNe h).elim
      | isFalse _ =>
        cases Classical.typeDecidableEq SortKItem
            (SortKItem.inj_SortString "$cells") (SortKItem.inj_SortString "odds") with
        | isTrue h => exact (oddsNe h).elim
        | isFalse _ =>
          cases Classical.typeDecidableEq SortKItem
              (SortKItem.inj_SortString "$cells") (SortKItem.inj_SortString "result") with
          | isTrue h => exact (resultNe h).elim
          | isFalse _ =>
            cases Classical.typeDecidableEq SortKItem
                (SortKItem.inj_SortString "$cells") (SortKItem.inj_SortString "i") with
            | isTrue h => exact (iNe h).elim
            | isFalse _ =>
              cases Classical.typeDecidableEq SortKItem
                  (SortKItem.inj_SortString "$cells") (SortKItem.inj_SortString "odd") with
              | isTrue h => exact (oddNe h).elim
              | isFalse _ => rfl

end Proof
