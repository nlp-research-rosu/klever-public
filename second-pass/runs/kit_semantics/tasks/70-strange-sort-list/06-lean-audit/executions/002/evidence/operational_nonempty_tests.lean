import Proof

namespace OperationalNonemptyTests

example (k v : SortKItem) :
    Proof.«_in_keys(_)_MAP_Bool_KItem_Map» k ⟨[(k, v)]⟩ = true := by
  simp [Proof.«_in_keys(_)_MAP_Bool_KItem_Map», Proof.proofMapContains]

example (k v : SortKItem) :
    Proof.«_[_<-undef]» ⟨[(k, v)]⟩ k = ⟨[]⟩ := by
  simp [Proof.«_[_<-undef]», Proof.proofMapDelete]

example (k other v : SortKItem) (h : other ≠ k) :
    Proof.«_in_keys(_)_MAP_Bool_KItem_Map» k ⟨[(other, v)]⟩ = false := by
  simp [Proof.«_in_keys(_)_MAP_Bool_KItem_Map», Proof.proofMapContains, h]

example (k other v : SortKItem) (h : other ≠ k) :
    Proof.«_[_<-undef]» ⟨[(other, v)]⟩ k = ⟨[(other, v)]⟩ := by
  simp [Proof.«_[_<-undef]», Proof.proofMapDelete, h]

end OperationalNonemptyTests
