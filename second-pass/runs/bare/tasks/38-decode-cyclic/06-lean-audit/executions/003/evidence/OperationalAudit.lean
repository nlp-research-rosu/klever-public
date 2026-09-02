import Proof

open Klean38DecodeCyclic

namespace OperationalAudit

#eval Proof.«_<=Int_» (-1) 0
#eval Proof.«_<=Int_» 0 0
#eval Proof.«_<=Int_» 1 0

#eval Proof.«lengthString(_)_STRING-COMMON_Int_String» ""
#eval Proof.«lengthString(_)_STRING-COMMON_Int_String» "abc"
#eval Proof.«lengthString(_)_STRING-COMMON_Int_String» "é"
#eval Proof.«lengthString(_)_STRING-COMMON_Int_String» "🙂"
#eval Proof.«lengthString(_)_STRING-COMMON_Int_String» "é"

#eval Proof.«substrString(_,_,_)_STRING-COMMON_String_String_Int_Int»
  "abcdef" 0 6
#eval Proof.«substrString(_,_,_)_STRING-COMMON_String_String_Int_Int»
  "abcdef" 1 4
#eval Proof.«substrString(_,_,_)_STRING-COMMON_String_String_Int_Int»
  "a🙂éz" 1 3
#eval Proof.«substrString(_,_,_)_STRING-COMMON_String_String_Int_Int»
  "abcdef" 3 3

def key1 : SortKItem := .inj_SortString "key1"
def key2 : SortKItem := .inj_SortString "key2"
def value1 : SortKItem := .inj_SortInt 11
def value2 : SortKItem := .inj_SortInt 22
def value3 : SortKItem := .inj_SortInt 33
def sampleMap : SortMap := ⟨[(key1, value1), (key2, value2)]⟩

example :
    (Proof.«Map:update» sampleMap key1 value3).coll =
      [(key1, value3), (key2, value2)] := by
  simp [Proof.«Map:update», sampleMap, key1, key2, value1, value2, value3]

example :
    (Proof.«Map:update» sampleMap (.inj_SortString "new") value3).coll =
      [(.inj_SortString "new", value3), (key1, value1), (key2, value2)] := by
  simp [Proof.«Map:update», sampleMap, key1, key2, value1, value2, value3]

-- Counterfactual implementations that satisfy the generated proposition but
-- do not implement the frozen operations.
def badLe (_ _ : SortInt) : SortBool := true
def badMapUpdate (_ : SortMap) (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩
def badLength (_ : SortString) : SortInt := 0
def badSubstring (s : SortString) (_ _ : SortInt) : SortString := s

theorem counterfactualTarget :
    Klean38DecodeCyclic.Lemmas.targetStatement
      badLe badMapUpdate badLength badSubstring := by
  constructor
  · intro V' K M V
    simp [badMapUpdate]
  constructor <;> simp [badLe, badSubstring]

-- The real candidate is distinguished from all four counterfactuals.
example : Proof.«_<=Int_» 1 0 ≠ badLe 1 0 := by decide
example :
    Proof.«lengthString(_)_STRING-COMMON_Int_String» "abc" ≠
      badLength "abc" := by decide
example :
    Proof.«substrString(_,_,_)_STRING-COMMON_String_String_Int_Int»
        "abcdef" 1 4 ≠
      badSubstring "abcdef" 1 4 := by decide
example :
    (Proof.«Map:update» sampleMap key1 value3).coll ≠
      (badMapUpdate sampleMap key1 value3).coll := by
  simp [Proof.«Map:update», badMapUpdate, sampleMap, key1, key2,
    value1, value2, value3]

end OperationalAudit
