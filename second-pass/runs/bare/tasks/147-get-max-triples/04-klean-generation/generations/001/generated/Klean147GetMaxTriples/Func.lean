import Klean147GetMaxTriples.Inj

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «.Map» : Option SortMap

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

def _83dcf9b : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_=/=Int_» I2 0
    let _Val1 <- _modInt_ I1 I2
    let _Val2 <- «_-Int_» I1 _Val1
    let _Val3 <- «_/Int_» _Val2 I2
    guard _Val0
    return _Val3

def _divInt_ (x0 : SortInt) (x1 : SortInt) : Option SortInt := _83dcf9b x0 x1

def _8c062fa : SortInt → Option SortInt
  | X => do
    let _Val0 <- «_-Int_» X 1
    let _Val1 <- «_*Int_» X _Val0
    let _Val2 <- «_-Int_» X 2
    let _Val3 <- «_*Int_» _Val1 _Val2
    let _Val4 <- _divInt_ _Val3 6
    return _Val4

def «choose3(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _8c062fa x0

def _3af731e : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_+Int_» N 1
    let _Val1 <- _divInt_ _Val0 3
    let _Val2 <- «choose3(_)_VERIFICATION_Int_Int» _Val1
    let _Val3 <- «_+Int_» N 1
    let _Val4 <- _divInt_ _Val3 3
    let _Val5 <- «_-Int_» N _Val4
    let _Val6 <- «choose3(_)_VERIFICATION_Int_Int» _Val5
    let _Val7 <- «_+Int_» _Val2 _Val6
    return _Val7

def «validTripleCount(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _3af731e x0