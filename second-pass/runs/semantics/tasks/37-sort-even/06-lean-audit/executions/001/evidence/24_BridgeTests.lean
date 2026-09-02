import Proof

namespace BridgeAudit

open Proof

def emptyVS : SortValSeq :=
  SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

def oneVS : SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
    (SortVal.inj_SortInt 7)
    emptyVS

def keyA : SortKItem := SortKItem.inj_SortString "a"
def keyB : SortKItem := SortKItem.inj_SortString "b"
def value1 : SortKItem :=
  SortKItem.inj_SortVal (SortVal.inj_SortInt 1)
def value2 : SortKItem :=
  SortKItem.inj_SortVal (SortVal.inj_SortInt 2)

example :
    «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» emptyVS oneVS =
      oneVS := by
  simp [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq», emptyVS]

example :
    «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» oneVS oneVS =
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortInt 7)
        oneVS := by
  simp [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»,
    emptyVS, oneVS]

example : («_|->_» keyA value1).coll = [(keyA, value1)] := by
  rfl

example :
    (_Map_ («_|->_» keyA value1) («_|->_» keyB value2)).coll =
      [(keyA, value1), (keyB, value2)] := by
  rfl

example :
    «_in_keys(_)_MAP_Bool_KItem_Map»
        keyA (_Map_ («_|->_» keyA value1) («_|->_» keyB value2)) =
      true := by
  cases d : Classical.typeDecidableEq SortKItem keyA keyA with
  | isTrue _ =>
      simp [_Map_, «_|->_», «_in_keys(_)_MAP_Bool_KItem_Map», d]
  | isFalse h => exact (h rfl).elim

example :
    «_in_keys(_)_MAP_Bool_KItem_Map»
        (SortKItem.inj_SortString "absent")
        (_Map_ («_|->_» keyA value1) («_|->_» keyB value2)) =
      false := by
  cases dA : Classical.typeDecidableEq SortKItem
      (SortKItem.inj_SortString "absent") keyA with
  | isTrue h =>
      have : False := by simpa [keyA] using h
      contradiction
  | isFalse _ =>
      cases dB : Classical.typeDecidableEq SortKItem
          (SortKItem.inj_SortString "absent") keyB with
      | isTrue h =>
          have : False := by simpa [keyB] using h
          contradiction
      | isFalse _ =>
          simp [_Map_, «_|->_»,
            «_in_keys(_)_MAP_Bool_KItem_Map», dA, dB]

/- Deliberately wrong total parameter meanings.  These show that the fixed
   equations alone do not enforce the operational bridge, so the candidate
   definitions must be checked independently. -/
def badMap (_left _right : SortMap) : SortMap := ⟨[]⟩
def badMembership (_key : SortKItem) (_map : SortMap) : SortBool := false
def badSingleton (_key _value : SortKItem) : SortMap := ⟨[]⟩
def badConcat (left _right : SortValSeq) : SortValSeq := left

theorem wrongMeaningsStillProveFixedEquations :
    Klean37SortEven.Lemmas.targetStatement
      badMap badMembership badSingleton badConcat := by
  unfold Klean37SortEven.Lemmas.targetStatement
  simp [badConcat, badMembership]

example : badConcat emptyVS oneVS ≠
    «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» emptyVS oneVS := by
  simp [badConcat, emptyVS, oneVS,
    «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»]

example : badSingleton keyA value1 ≠ «_|->_» keyA value1 := by
  simp [badSingleton, «_|->_»]

example :
    badMap («_|->_» keyA value1) («_|->_» keyB value2) ≠
      _Map_ («_|->_» keyA value1) («_|->_» keyB value2) := by
  simp [badMap, _Map_, «_|->_»]

example :
    badMembership keyA («_|->_» keyA value1) ≠
      «_in_keys(_)_MAP_Bool_KItem_Map» keyA («_|->_» keyA value1) := by
  cases d : Classical.typeDecidableEq SortKItem keyA keyA with
  | isTrue _ =>
      simp [badMembership, «_|->_»,
        «_in_keys(_)_MAP_Bool_KItem_Map», d]
  | isFalse h => exact (h rfl).elim

end BridgeAudit
