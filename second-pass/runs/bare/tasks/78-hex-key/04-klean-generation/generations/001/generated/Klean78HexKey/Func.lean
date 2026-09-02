import Klean78HexKey.Inj

axiom «.Map» : Option SortMap

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «findString(_,_,_)_STRING-COMMON_Int_String_String_Int» (x0 : SortString) (x1 : SortString) (x2 : SortInt) : Option SortInt

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

noncomputable def _1c726cd : SortString → SortString → Option SortInt
  | Source, ToCount => do
    let _Val0 <- «findString(_,_,_)_STRING-COMMON_Int_String_String_Int» Source ToCount 0
    let _Val1 <- «_<Int_» _Val0 0
    guard _Val1
    return 0

axiom _628cff0 : SortString → SortString → Option SortInt
axiom «countAllOccurrences(_,_)_STRING-COMMON_Int_String_String» (x0 : SortString) (x1 : SortString) : Option SortInt

noncomputable def _25b71bf : SortString → Option SortInt
  | S => do
    let _Val0 <- «countAllOccurrences(_,_)_STRING-COMMON_Int_String_String» S "2"
    let _Val1 <- «countAllOccurrences(_,_)_STRING-COMMON_Int_String_String» S "3"
    let _Val2 <- «_+Int_» _Val0 _Val1
    let _Val3 <- «countAllOccurrences(_,_)_STRING-COMMON_Int_String_String» S "5"
    let _Val4 <- «_+Int_» _Val2 _Val3
    let _Val5 <- «countAllOccurrences(_,_)_STRING-COMMON_Int_String_String» S "7"
    let _Val6 <- «_+Int_» _Val4 _Val5
    let _Val7 <- «countAllOccurrences(_,_)_STRING-COMMON_Int_String_String» S "B"
    let _Val8 <- «_+Int_» _Val6 _Val7
    let _Val9 <- «countAllOccurrences(_,_)_STRING-COMMON_Int_String_String» S "D"
    let _Val10 <- «_+Int_» _Val8 _Val9
    return _Val10

noncomputable def «primeHexCount(_)_VERIFICATION_Int_String» (x0 : SortString) : Option SortInt := _25b71bf x0