import Proof

open Proof

#eval Proof.«_<=Int_» (-2) (-1)
#eval Proof.«_<=Int_» 3 2
#eval Proof.«_<=Int_» 3 3

#eval «lengthString(_)_STRING-COMMON_Int_String» ""
#eval «lengthString(_)_STRING-COMMON_Int_String» "a"
#eval «lengthString(_)_STRING-COMMON_Int_String» "😀"
#eval «lengthString(_)_STRING-COMMON_Int_String» "é"

#eval «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int»
  "a😀b" 1 2
#eval «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int»
  "a😀b" 0 3
#eval «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» "abc" 0 0
#eval «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» "abc" (-1) 1
#eval «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» "abc" 2 1
#eval «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» "abc" 0 4

private def key1 : SortKItem := .inj_SortInt 1
private def key2 : SortKItem := .inj_SortInt 2
private def value2 : SortKItem := .inj_SortInt 2
private def value8 : SortKItem := .inj_SortInt 8
private def value9 : SortKItem := .inj_SortInt 9

example :
    («Map:update» ⟨[]⟩ key1 value2).coll = [(key1, value2)] := by
  simp [«Map:update»]

example :
    («Map:update» ⟨[(key1, value9)]⟩ key1 value2).coll =
      [(key1, value2)] := by
  simp [«Map:update», key1]

example :
    («Map:update»
      ⟨[(key1, value9), (key2, value8)]⟩ key1 value2).coll =
      [(key1, value2), (key2, value8)] := by
  simp [«Map:update», key1, key2]
