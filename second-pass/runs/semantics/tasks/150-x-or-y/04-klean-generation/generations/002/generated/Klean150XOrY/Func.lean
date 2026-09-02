import Klean150XOrY.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _27e21f7 : SortInt → SortInt → SortInt → Option SortInt
  | N, D, OLD => do
    let _Val0 <- «_>=Int_» N 2
    let _Val1 <- «_>=Int_» D 2
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_>=Int_» D N
    let _Val4 <- _andBool_ _Val2 _Val3
    guard _Val4
    return OLD

def _cfc968c : SortInt → SortInt → SortVal → SortVal → Option SortVal
  | N, D, X, Y => do
    let _Val0 <- «_>=Int_» D 2
    let _Val1 <- «_>=Int_» N 2
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_>=Int_» D N
    let _Val4 <- _andBool_ _Val2 _Val3
    guard _Val4
    return X

def _dce0bb7 : SortInt → SortInt → SortVal → SortVal → Option SortVal
  | N, D, X, Y => do
    let _Val0 <- «_>=Int_» D 2
    let _Val1 <- «_<Int_» N 2
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return Y

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def _18e1f2e : SortInt → SortInt → SortVal → SortVal → Option SortVal
  | N, D, X, Y => do
    let _Val0 <- «_>=Int_» D 2
    let _Val1 <- «_>=Int_» N 2
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» D N
    let _Val4 <- _andBool_ _Val2 _Val3
    let _Val5 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N D
    let _Val6 <- «_==Int_» _Val5 0
    let _Val7 <- _andBool_ _Val4 _Val6
    guard _Val7
    return Y

noncomputable def _5118e89 : SortInt → SortInt → SortInt → Option SortInt
  | N, D, OLD => do
    let _Val0 <- «_>=Int_» N 2
    let _Val1 <- «_>=Int_» D 2
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» D N
    let _Val4 <- _andBool_ _Val2 _Val3
    let _Val5 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N D
    let _Val6 <- «_==Int_» _Val5 0
    let _Val7 <- _andBool_ _Val4 _Val6
    guard _Val7
    return D

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

axiom _93f5802 : SortInt → SortInt → SortInt → Option SortInt
axiom «scanLast(_,_,_)_X-OR-Y-VERIFICATION_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt

axiom _9f6a0c3 : SortInt → SortInt → SortVal → SortVal → Option SortVal
axiom «primeSelect(_,_,_,_)_X-OR-Y-VERIFICATION_Val_Int_Int_Val_Val» (x0 : SortInt) (x1 : SortInt) (x2 : SortVal) (x3 : SortVal) : Option SortVal