import Klean55Fib.Inj

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom «.Map» : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _299a5aa : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» 0 N
    let _Val1 <- «_<=Int_» N 1
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return N

axiom «fibMath(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt
axiom _a242653 : SortInt → Option SortInt