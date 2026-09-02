import Klean59LargestPrimeFactor.Inj

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _dc5d578 : SortInt → SortInt → Option SortInt
  | N, F => do
    let _Val0 <- «_*Int_» F F
    let _Val1 <- «_>Int_» _Val0 N
    guard _Val1
    return N

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

axiom _92bac24 : SortInt → SortInt → Option SortInt
axiom «lpfSpec(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt
axiom _e3a465c : SortInt → SortInt → Option SortInt