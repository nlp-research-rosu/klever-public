import Klean131Digits.Inj

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _0818b99 : SortInt → SortInt → Option SortInt
  | N, A => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return A

def _289f298 : SortInt → SortInt → Option SortInt
  | N, D => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return D

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _d6046b1 : SortInt → SortInt → Option SortInt
  | A, D => do
    let _Val0 <- «_%Int_» D 2
    let _Val1 <- «_==Int_» _Val0 0
    guard _Val1
    return A

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

axiom «finalScratchDigit(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt
axiom _a559666 : SortInt → SortInt → Option SortInt

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def _21e4c79 : SortInt → SortInt → Option SortInt
  | A, D => do
    let _Val0 <- «_%Int_» D 2
    let _Val1 <- «_=/=Int_» _Val0 0
    let _Val2 <- «_=/=Int_» A 0
    let _Val3 <- _andBool_ _Val1 _Val2
    let _Val4 <- «_*Int_» A D
    guard _Val3
    return _Val4

noncomputable def _6bf2342 : SortInt → SortInt → Option SortInt
  | A, D => do
    let _Val0 <- «_%Int_» D 2
    let _Val1 <- «_=/=Int_» _Val0 0
    let _Val2 <- «_==Int_» A 0
    let _Val3 <- _andBool_ _Val1 _Val2
    guard _Val3
    return D

noncomputable def «addOddDigit(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_21e4c79 x0 x1) <|> (_6bf2342 x0 x1) <|> (_d6046b1 x0 x1)

axiom _18ea9b6 : SortInt → SortInt → Option SortInt
axiom «oddProductFrom(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt

noncomputable def _55ce62c : SortInt → Option SortInt
  | N => do
    let _Val0 <- «oddProductFrom(_,_)_VERIFICATION_Int_Int_Int» N 0
    return _Val0

noncomputable def «oddProduct(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _55ce62c x0