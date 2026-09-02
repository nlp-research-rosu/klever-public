import Klean51RemoveVowels.Inj

axiom «deleteAll(_,_)_MPY_String_String_String» (x0 : SortString) (x1 : SortString) : Option SortString

noncomputable def _9279111 : SortString → Option SortString
  | S => do
    let _Val0 <- «deleteAll(_,_)_MPY_String_String_String» S "A"
    let _Val1 <- «deleteAll(_,_)_MPY_String_String_String» _Val0 "E"
    let _Val2 <- «deleteAll(_,_)_MPY_String_String_String» _Val1 "I"
    let _Val3 <- «deleteAll(_,_)_MPY_String_String_String» _Val2 "O"
    let _Val4 <- «deleteAll(_,_)_MPY_String_String_String» _Val3 "U"
    return _Val4

noncomputable def _fef4730 : SortString → Option SortString
  | S => do
    let _Val0 <- «deleteAll(_,_)_MPY_String_String_String» S "a"
    let _Val1 <- «deleteAll(_,_)_MPY_String_String_String» _Val0 "e"
    let _Val2 <- «deleteAll(_,_)_MPY_String_String_String» _Val1 "i"
    let _Val3 <- «deleteAll(_,_)_MPY_String_String_String» _Val2 "o"
    let _Val4 <- «deleteAll(_,_)_MPY_String_String_String» _Val3 "u"
    return _Val4

noncomputable def «removeUpperVowels(_)_VERIFICATION_String_String» (x0 : SortString) : Option SortString := _9279111 x0

noncomputable def «removeLowerVowels(_)_VERIFICATION_String_String» (x0 : SortString) : Option SortString := _fef4730 x0

noncomputable def _36c9fa9 : SortString → Option SortString
  | S => do
    let _Val0 <- «removeLowerVowels(_)_VERIFICATION_String_String» S
    let _Val1 <- «removeUpperVowels(_)_VERIFICATION_String_String» _Val0
    return _Val1

noncomputable def «removeVowelsSpec(_)_VERIFICATION_String_String» (x0 : SortString) : Option SortString := _36c9fa9 x0