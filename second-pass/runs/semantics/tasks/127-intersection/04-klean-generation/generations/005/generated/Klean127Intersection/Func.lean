import Klean127Intersection.Inj

def _eff2361 : Option SortVal := some ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 78 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 79 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))))

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _b60d52f : Option SortVal := some ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 89 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 69 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 83 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))))

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom ListItem (x0 : SortKItem) : Option SortList

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «.List» : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.Map» : Option SortMap

def «noV_VERIFICATION-BASE_Val» : Option SortVal := _eff2361

def _5615d55 : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_<Int_» I1 I2
    guard _Val0
    return I1

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def _e1effea : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_>=Int_» I1 I2
    guard _Val0
    return I2

def «yesV_VERIFICATION-BASE_Val» : Option SortVal := _b60d52f

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _2edc640 : SortInt → Option SortVal
  | N => do
    let _Val0 <- «_<=Int_» N 1
    let _Val1 <- «noV_VERIFICATION-BASE_Val»
    guard _Val0
    return _Val1

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def «minInt(_,_)_INT-COMMON_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_5615d55 x0 x1) <|> (_e1effea x0 x1)

def _1e34321 : SortInt → SortInt → Option SortVal
  | N, D => do
    let _Val0 <- «_>=Int_» D N
    let _Val1 <- «yesV_VERIFICATION-BASE_Val»
    guard _Val0
    return _Val1

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def _32083c7 : SortInt → SortInt → Option SortVal
  | N, D => do
    let _Val0 <- «_<Int_» D N
    let _Val1 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N D
    let _Val2 <- «_==Int_» _Val1 0
    let _Val3 <- _andBool_ _Val0 _Val2
    let _Val4 <- «noV_VERIFICATION-BASE_Val»
    guard _Val3
    return _Val4

def _1d39548 : SortInt → SortInt → SortInt → SortInt → Option SortInt
  | A, B, C, D => do
    let _Val0 <- «minInt(_,_)_INT-COMMON_Int_Int_Int» B D
    let _Val1 <- «maxInt(_,_)_INT-COMMON_Int_Int_Int» A C
    let _Val2 <- «_-Int_» _Val0 _Val1
    return _Val2

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

def «overlapLength(_,_,_,_)_VERIFICATION-BASE_Int_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortInt := _1d39548 x0 x1 x2 x3

axiom _7a9b8b6 : SortInt → SortInt → Option SortVal
axiom «primeFrom(_,_)_VERIFICATION-BASE_Val_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortVal

noncomputable def _324884a : SortInt → Option SortVal
  | N => do
    let _Val0 <- «_>Int_» N 1
    let _Val1 <- «primeFrom(_,_)_VERIFICATION-BASE_Val_Int_Int» N 2
    guard _Val0
    return _Val1

noncomputable def «primeResult(_)_VERIFICATION-BASE_Val_Int» (x0 : SortInt) : Option SortVal := (_2edc640 x0) <|> (_324884a x0)