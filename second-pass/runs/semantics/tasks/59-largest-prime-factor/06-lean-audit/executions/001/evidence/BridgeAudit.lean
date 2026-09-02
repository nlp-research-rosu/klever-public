import Proof

namespace BridgeAudit

theorem sortScope_is_empty (scope : SortScope) : False :=
  nomatch scope

def badMap (_left _right : SortMap) : SortMap := ⟨[]⟩
def badInKeys (_key : SortKItem) (_map : SortMap) : SortBool := true
def badDelete (_map : SortMap) (_key : SortKItem) : SortMap := ⟨[]⟩
def badElement (_key _value : SortKItem) : SortMap := ⟨[]⟩
def badNot (_value : SortBool) : SortBool := false

theorem fixedTarget_is_vacuous :
    Klean59LargestPrimeFactor.Lemmas.targetStatement
      badMap badInKeys badDelete badElement badNot := by
  intro _L _M scope _h
  exact nomatch scope

def key0 : SortKItem := SortKItem.inj_SortInt 0
def key1 : SortKItem := SortKItem.inj_SortInt 1

theorem candidateMap_is_not_commutative :
    Proof._Map_
        (Proof.«_|->_» key0 key0)
        (Proof.«_|->_» key1 key1)
      ≠
    Proof._Map_
        (Proof.«_|->_» key1 key1)
        (Proof.«_|->_» key0 key0) := by
  simp [Proof._Map_, Proof.«_|->_», key0, key1]

end BridgeAudit
