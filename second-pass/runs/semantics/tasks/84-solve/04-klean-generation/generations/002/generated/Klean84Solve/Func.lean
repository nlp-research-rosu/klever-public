import Klean84Solve.Inj

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _37dc11b : SortInt → SortIntSeq → Option SortIntSeq
  | 0, ACC => some ACC
  | _, _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom ListItem (x0 : SortKItem) : Option SortList

def _49c55eb : SortInt → Option SortIntSeq
  | 0 => some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _ => none

axiom «.List» : Option SortList

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

axiom _62d7600 : SortInt → SortIntSeq → Option SortIntSeq
axiom «binAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortIntSeq

noncomputable def _4643944 : SortInt → SortInt → Option SortInt
  | N, P => do
    let _Val0 <- «_>=Int_» N 0
    let _Val1 <- «_>Int_» P 1
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N P
    let _Val4 <- «_-Int_» N _Val3
    let _Val5 <- «_/Int_» _Val4 P
    let _Val6 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val5 10
    guard _Val2
    return _Val6

noncomputable def _4a00573 : SortInt → SortInt → Option SortInt
  | N, 1 => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N 10
    return _Val0
  | _, _ => none

noncomputable def _323c995 : SortInt → Option SortIntSeq
  | N => do
    let _Val0 <- «_>Int_» N 0
    let _Val1 <- «binAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» N SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    guard _Val0
    return _Val1

noncomputable def «decimalDigit(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_4643944 x0 x1) <|> (_4a00573 x0 x1)

noncomputable def «binCodes(_)_MPY-BUILTINS_IntSeq_Int» (x0 : SortInt) : Option SortIntSeq := (_323c995 x0) <|> (_49c55eb x0)

noncomputable def _47ece17 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» 0 N
    let _Val1 <- «_<=Int_» N 10000
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «decimalDigit(_,_)_VERIFICATION_Int_Int_Int» N 1
    let _Val4 <- «decimalDigit(_,_)_VERIFICATION_Int_Int_Int» N 10
    let _Val5 <- «_+Int_» _Val3 _Val4
    let _Val6 <- «decimalDigit(_,_)_VERIFICATION_Int_Int_Int» N 100
    let _Val7 <- «_+Int_» _Val5 _Val6
    let _Val8 <- «decimalDigit(_,_)_VERIFICATION_Int_Int_Int» N 1000
    let _Val9 <- «_+Int_» _Val7 _Val8
    let _Val10 <- «decimalDigit(_,_)_VERIFICATION_Int_Int_Int» N 10000
    let _Val11 <- «_+Int_» _Val9 _Val10
    guard _Val2
    return _Val11

noncomputable def _d529f62 : SortInt → Option SortStr
  | N => do
    let _Val0 <- «binCodes(_)_MPY-BUILTINS_IntSeq_Int» N
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0)

noncomputable def «decimalDigitSum(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _47ece17 x0

noncomputable def «binaryNumeral(_)_VERIFICATION_Str_Int» (x0 : SortInt) : Option SortStr := _d529f62 x0