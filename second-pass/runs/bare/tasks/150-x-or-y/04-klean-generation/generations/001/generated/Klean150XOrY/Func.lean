import Klean150XOrY.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _d55cf96 : SortBool → SortInt → SortInt → Option SortVal
  | false, _X, Y => some (SortVal.«intVal(_)_MPY_Val_Int» Y)
  | _, _, _ => none

def _bd71977 : SortBool → SortInt → SortInt → Option SortVal
  | true, X, _Y => some (SortVal.«intVal(_)_MPY_Val_Int» X)
  | _, _, _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.Map» : Option SortMap

def _3ac6f3e : SortInt → Option SortBool
  | N => do
    let _Val0 <- «_<Int_» N 2
    guard _Val0
    return false

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _70c13ee : SortInt → SortInt → Option SortBool
  | N, D => do
    let _Val0 <- «_*Int_» D D
    let _Val1 <- «_<Int_» N _Val0
    guard _Val1
    return true

def «chooseVal(_,_,_)_MPY-VERIFICATION_Val_Bool_Int_Int» (x0 : SortBool) (x1 : SortInt) (x2 : SortInt) : Option SortVal := (_bd71977 x0 x1 x2) <|> (_d55cf96 x0 x1 x2)

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def _bf50540 : SortInt → SortInt → Option SortBool
  | N, D => do
    let _Val0 <- «_*Int_» D D
    let _Val1 <- «_<=Int_» _Val0 N
    let _Val2 <- «_%Int_» N D
    let _Val3 <- «_==Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    guard _Val4
    return false

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

axiom _9fc4d94 : SortInt → SortInt → Option SortBool
axiom «primeFrom(_,_)_MPY-VERIFICATION_Bool_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortBool

noncomputable def _fab8c28 : SortInt → Option SortBool
  | N => do
    let _Val0 <- «_<=Int_» 2 N
    let _Val1 <- «primeFrom(_,_)_MPY-VERIFICATION_Bool_Int_Int» N 2
    guard _Val0
    return _Val1

noncomputable def «isPrime(_)_MPY-VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := (_3ac6f3e x0) <|> (_fab8c28 x0)