import Proof

namespace BridgeAudit

open Proof

def k1 : SortKItem := SortKItem.inj_SortInt 1
def k2 : SortKItem := SortKItem.inj_SortInt 2
def v10 : SortKItem := SortKItem.inj_SortInt 10
def v20 : SortKItem := SortKItem.inj_SortInt 20

example :
    (Proof._List_ ⟨[k1]⟩ ⟨[k2]⟩).coll = [k1, k2] := by
  rfl

example :
    (Proof.«_|->_» k1 v10).coll = [(k1, v10)] := by
  rfl

example :
    (Proof.ListItem k1).coll = [k1] := by
  rfl

example :
    Proof.notBool_ true = false ∧ Proof.notBool_ false = true := by
  decide

example :
    Proof.«_in_keys(_)_MAP_Bool_KItem_Map»
        k1 (Proof.«_|->_» k1 v10) = true := by
  simp [Proof.«_in_keys(_)_MAP_Bool_KItem_Map», Proof.«_|->_»,
    _root_.«_in_keys(_)_MAP_Bool_KItem_Map», _root_.«_|->_»]
  kunfold_contains
  simp

example :
    Proof.«_in_keys(_)_MAP_Bool_KItem_Map»
        k2 (Proof.«_|->_» k1 v10) = false := by
  simp [Proof.«_in_keys(_)_MAP_Bool_KItem_Map», Proof.«_|->_»,
    _root_.«_in_keys(_)_MAP_Bool_KItem_Map», _root_.«_|->_»]
  kunfold_contains
  simp [k1, k2]
  kunfold_contains
  rfl

example :
    (Proof.«_[_<-undef]» (Proof.«_|->_» k1 v10) k1).coll = [] := by
  simp [Proof.«_[_<-undef]», Proof.«_|->_»,
    _root_.«_[_<-undef]», _root_.«_|->_»]
  kunfold_delete
  simp
  kunfold_delete
  rfl

example :
    (Proof._Map_
        (Proof.«_|->_» k1 v10)
        (Proof.«_|->_» k2 v20)).coll =
      [(k2, v20), (k1, v10)] := by
  simp [Proof._Map_, Proof.«_|->_», _root_._Map_, _root_.«_|->_»]
  kunfold_maps

abbrev nilInts : SortInts :=
  SortInts.«nilInts_NEXT-SMALLEST-VERIFICATION_Ints»

abbrev consInts (head : SortInt) (tail : SortInts) : SortInts :=
  SortInts.«consInts(_,_)_NEXT-SMALLEST-VERIFICATION_Ints_Int_Ints»
    head tail

abbrev noneV : SortVal := SortVal.«noneV_MPY-CORE_Val»

abbrev nsScan :=
  Proof.«nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int»

example : nsScan nilInts 0 7 2 = SortVal.inj_SortInt 7 := by
  rfl

example : nsScan nilInts 0 7 1 = noneV := by
  rfl

example :
    nsScan (consInts 1 (consInts 2 (consInts 3 nilInts))) 0 0 0 =
      SortVal.inj_SortInt 2 := by
  rfl

example :
    nsScan
        (consInts 5
          (consInts 1
            (consInts 4 (consInts 3 (consInts 2 nilInts)))))
        0 0 0 =
      SortVal.inj_SortInt 2 := by
  rfl

example : nsScan (consInts 1 (consInts 1 nilInts)) 0 0 0 = noneV := by
  rfl

example :
    nsScan (consInts (-1) (consInts (-3) (consInts (-2) nilInts)))
        0 0 0 =
      SortVal.inj_SortInt (-2) := by
  rfl

-- Adversarial accumulator states exercise every nonzero/nonone branch.
example : nsScan (consInts 5 nilInts) 10 20 99 =
    SortVal.inj_SortInt 10 := by
  rfl

example : nsScan (consInts 15 nilInts) 10 20 99 =
    SortVal.inj_SortInt 15 := by
  rfl

example : nsScan (consInts 25 nilInts) 10 20 99 =
    noneV := by
  rfl

end BridgeAudit
