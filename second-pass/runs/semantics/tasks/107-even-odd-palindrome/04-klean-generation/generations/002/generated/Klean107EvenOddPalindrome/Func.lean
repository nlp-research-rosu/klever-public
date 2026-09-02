import Klean107EvenOddPalindrome.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _95d5924 : SortInt → Option SortInt
  | 1000 => some 48
  | _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def _da9fcff : SortInt → Option SortInt
  | 1000 => some 60
  | _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _387f1b0 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_/Int_» N 100
    return _Val0

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def «leadingDigit(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _387f1b0 x0

def _6f7cfd5 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» 10 N
    let _Val1 <- «_<Int_» N 100
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_/Int_» N 11
    let _Val4 <- «_/Int_» _Val3 2
    let _Val5 <- «_+Int_» 4 _Val4
    guard _Val2
    return _Val5

def _75c9fa5 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» 1 N
    let _Val1 <- «_<Int_» N 10
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_+Int_» N 1
    let _Val4 <- «_/Int_» _Val3 2
    guard _Val2
    return _Val4

def _96685c3 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» 1 N
    let _Val1 <- «_<Int_» N 10
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_/Int_» N 2
    guard _Val2
    return _Val3

def _f259a9a : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» 10 N
    let _Val1 <- «_<Int_» N 100
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_/Int_» N 11
    let _Val4 <- «_+Int_» _Val3 1
    let _Val5 <- «_/Int_» _Val4 2
    let _Val6 <- «_+Int_» 5 _Val5
    guard _Val2
    return _Val6

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def _a8cd13c : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_%Int_» N 100
    let _Val1 <- «leadingDigit(_)_VERIFICATION_Int_Int» N
    let _Val2 <- «_-Int_» _Val0 _Val1
    let _Val3 <- «_+Int_» _Val2 10
    let _Val4 <- «_/Int_» _Val3 10
    return _Val4

noncomputable def «currentBlock(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _a8cd13c x0

noncomputable def _5696543 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» 100 N
    let _Val1 <- «_<Int_» N 1000
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «leadingDigit(_)_VERIFICATION_Int_Int» N
    let _Val4 <- «_-Int_» _Val3 1
    let _Val5 <- «_/Int_» _Val4 2
    let _Val6 <- «_*Int_» 10 _Val5
    let _Val7 <- «_+Int_» 8 _Val6
    let _Val8 <- «leadingDigit(_)_VERIFICATION_Int_Int» N
    let _Val9 <- «_%Int_» _Val8 2
    let _Val10 <- «_==Int_» _Val9 0
    let _Val11 <- «currentBlock(_)_VERIFICATION_Int_Int» N
    let _Val12 <- kite _Val10 _Val11 0
    let _Val13 <- «_+Int_» _Val7 _Val12
    guard _Val2
    return _Val13

noncomputable def _fdb1726 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» 100 N
    let _Val1 <- «_<Int_» N 1000
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «leadingDigit(_)_VERIFICATION_Int_Int» N
    let _Val4 <- «_/Int_» _Val3 2
    let _Val5 <- «_*Int_» 10 _Val4
    let _Val6 <- «_+Int_» 10 _Val5
    let _Val7 <- «leadingDigit(_)_VERIFICATION_Int_Int» N
    let _Val8 <- «_%Int_» _Val7 2
    let _Val9 <- «_==Int_» _Val8 1
    let _Val10 <- «currentBlock(_)_VERIFICATION_Int_Int» N
    let _Val11 <- kite _Val9 _Val10 0
    let _Val12 <- «_+Int_» _Val6 _Val11
    guard _Val2
    return _Val12

noncomputable def «evenPalindromes(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_5696543 x0) <|> (_6f7cfd5 x0) <|> (_95d5924 x0) <|> (_96685c3 x0)

noncomputable def «oddPalindromes(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_75c9fa5 x0) <|> (_da9fcff x0) <|> (_f259a9a x0) <|> (_fdb1726 x0)