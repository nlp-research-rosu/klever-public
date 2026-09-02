import Klean101WordsString.Inj

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «_+String__STRING-COMMON_String_String_String» (x0 : SortString) (x1 : SortString) : Option SortString

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

axiom «findString(_,_,_)_STRING-COMMON_Int_String_String_Int» (x0 : SortString) (x1 : SortString) (x2 : SortInt) : Option SortInt

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «.List» : Option SortList

def _8baee90 : SortString → SortString → SortString → SortInt → Option SortString
  | Source, _Gen0, _Gen1, Count => do
    let _Val0 <- «_>=Int_» Count 0
    guard _Val0
    return Source

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _1c726cd : SortString → SortString → Option SortInt
  | Source, ToCount => do
    let _Val0 <- «findString(_,_,_)_STRING-COMMON_Int_String_String_Int» Source ToCount 0
    let _Val1 <- «_<Int_» _Val0 0
    guard _Val1
    return 0

noncomputable def _9277e79 : SortString → Option SortList
  | "" => do
    let _Val0 <- «.List»
    return _Val0
  | _ => none

axiom _4d80f4d : SortString → SortString → SortString → SortInt → Option SortString
axiom «replace(_,_,_,_)_STRING-COMMON_String_String_String_String_Int» (x0 : SortString) (x1 : SortString) (x2 : SortString) (x3 : SortInt) : Option SortString

noncomputable def _ba58b91 : SortString → Option SortList
  | S => do
    let _Val0 <- «lengthString(_)_STRING-COMMON_Int_String» S
    let _Val1 <- «_>Int_» _Val0 0
    let _Val2 <- «findString(_,_,_)_STRING-COMMON_Int_String_String_Int» S " " 0
    let _Val3 <- «_==Int_» _Val2 (-1)
    let _Val4 <- _andBool_ _Val1 _Val3
    let _Val5 <- ListItem ((@inj SortString SortKItem) S)
    guard _Val4
    return _Val5

axiom _628cff0 : SortString → SortString → Option SortInt
axiom «countAllOccurrences(_,_)_STRING-COMMON_Int_String_String» (x0 : SortString) (x1 : SortString) : Option SortInt

axiom _4254329 : SortString → Option SortList
axiom _8c61d4e : SortString → Option SortList
axiom «splitSpaces(_)_VERIFICATION_List_String» (x0 : SortString) : Option SortList

noncomputable def _2621671 : SortString → SortString → SortString → Option SortString
  | Source, ToReplace, Replacement => do
    let _Val0 <- «countAllOccurrences(_,_)_STRING-COMMON_Int_String_String» Source ToReplace
    let _Val1 <- «replace(_,_,_,_)_STRING-COMMON_String_String_String_String_Int» Source ToReplace Replacement _Val0
    return _Val1

noncomputable def «replaceAll(_,_,_)_STRING-COMMON_String_String_String_String» (x0 : SortString) (x1 : SortString) (x2 : SortString) : Option SortString := _2621671 x0 x1 x2

noncomputable def _7b58a9e : SortString → Option SortList
  | S => do
    let _Val0 <- «replaceAll(_,_,_)_STRING-COMMON_String_String_String_String» S "," " "
    let _Val1 <- «splitSpaces(_)_VERIFICATION_List_String» _Val0
    return _Val1

noncomputable def «wordsContract(_)_VERIFICATION_List_String» (x0 : SortString) : Option SortList := _7b58a9e x0