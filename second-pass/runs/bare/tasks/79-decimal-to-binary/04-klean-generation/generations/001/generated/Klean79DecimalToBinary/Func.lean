import Klean79DecimalToBinary.Inj

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «Int2String(_)_STRING-COMMON_String_Int» (x0 : SortInt) : Option SortString

axiom «_+String__STRING-COMMON_String_String_String» (x0 : SortString) (x1 : SortString) : Option SortString

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _9d10ea8 : SortInt → Option SortString
  | I => do
    let _Val0 <- «_<=Int_» 0 I
    let _Val1 <- «_<Int_» I 2
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «Int2String(_)_STRING-COMMON_String_Int» I
    guard _Val2
    return _Val3

axiom «binDigits(_)_SEMANTIC_String_Int» (x0 : SortInt) : Option SortString
axiom _e888267 : SortInt → Option SortString

noncomputable def _6a1a4b3 : SortInt → Option SortString
  | I => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «binDigits(_)_SEMANTIC_String_Int» I
    let _Val2 <- «_+String__STRING-COMMON_String_String_String» "db" _Val1
    let _Val3 <- «_+String__STRING-COMMON_String_String_String» _Val2 "db"
    guard _Val0
    return _Val3

noncomputable def _fa622a8 : SortInt → Option SortString
  | I => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_-Int_» 0 I
    let _Val2 <- «binDigits(_)_SEMANTIC_String_Int» _Val1
    let _Val3 <- «_+String__STRING-COMMON_String_String_String» "b" _Val2
    let _Val4 <- «_+String__STRING-COMMON_String_String_String» "db" _Val3
    let _Val5 <- «_+String__STRING-COMMON_String_String_String» _Val4 "db"
    guard _Val0
    return _Val5

noncomputable def «decimalToBinarySpec(_)_VERIFICATION_String_Int» (x0 : SortInt) : Option SortString := (_6a1a4b3 x0) <|> (_fa622a8 x0)