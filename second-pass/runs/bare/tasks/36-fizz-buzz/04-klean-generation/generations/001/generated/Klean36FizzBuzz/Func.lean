import Klean36FizzBuzz.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.Map» : Option SortMap

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _c65901c : SortInt → SortInt → Option SortInt
  | I, N => do
    let _Val0 <- «_>=Int_» I N
    guard _Val0
    return 0

def _fc539c8 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_>=Int_» N 0
    guard _Val0
    return N

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _562b278 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<Int_» N 0
    guard _Val0
    return 0

def _d123c45 : SortInt → Option SortInt
  | X => do
    let _Val0 <- «_<=Int_» X 0
    guard _Val0
    return 0

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «fizzEnd(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_562b278 x0) <|> (_fc539c8 x0)

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

axiom _29742c3 : SortInt → Option SortInt
axiom _50a6531 : SortInt → Option SortInt
axiom «digitSevens(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt

noncomputable def _da37715 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_%Int_» I 11
    let _Val1 <- «_=/=Int_» _Val0 0
    let _Val2 <- «_%Int_» I 13
    let _Val3 <- «_=/=Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    guard _Val4
    return 0

noncomputable def _596b751 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_%Int_» I 11
    let _Val1 <- «_=/=Int_» _Val0 0
    let _Val2 <- «_%Int_» I 13
    let _Val3 <- «_==Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    let _Val5 <- «digitSevens(_)_VERIFICATION_Int_Int» I
    guard _Val4
    return _Val5

noncomputable def _5360280 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_%Int_» I 11
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «digitSevens(_)_VERIFICATION_Int_Int» I
    guard _Val1
    return _Val2

noncomputable def «fizzContribution(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_5360280 x0) <|> (_596b751 x0) <|> (_da37715 x0)

axiom _4918970 : SortInt → SortInt → Option SortInt
axiom «fizzFrom(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt