import Klean94Skjkasdkd.Inj

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _48de78d : SortInt → SortInt → SortBool → Option SortBool
  | _Gen0, _Gen1, false => some false
  | _, _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom «Map:update» (x0 : SortMap) (x1 : SortKItem) (x2 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

axiom «_in_keys(_)_MAP_Bool_KItem_Map» (x0 : SortKItem) (x1 : SortMap) : Option SortBool

axiom «_[_<-undef]» (x0 : SortMap) (x1 : SortKItem) : Option SortMap

def _db2985f : SortIntList → SortInt → Option SortInt
  | SortIntList.«.IntList_VERIFICATION_IntList», CUR => some CUR
  | _, _ => none

def _6239c81 : SortInt → SortInt → SortBool → Option SortInt
  | _Gen0, D, false => some D
  | _, _, _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «.List» : Option SortList

def _d2e3b6b : SortInt → SortInt → Option SortInt
  | N, A => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return A

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def _b2f455e : SortInt → SortInt → SortBool → Option SortInt
  | N, D, true => do
    let _Val0 <- «_*Int_» D D
    let _Val1 <- «_>Int_» _Val0 N
    guard _Val1
    return D
  | _, _, _ => none

def _f49a4ea : SortInt → SortInt → SortBool → Option SortBool
  | N, D, true => do
    let _Val0 <- «_*Int_» D D
    let _Val1 <- «_>Int_» _Val0 N
    guard _Val1
    return true
  | _, _, _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

axiom _6502fd4 : SortInt → SortInt → Option SortInt
axiom «digitAcc(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt

noncomputable def _4352fab : SortInt → SortInt → SortBool → Option SortInt
  | N, D, true => do
    let _Val0 <- «_*Int_» D D
    let _Val1 <- «_<=Int_» _Val0 N
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N D
    let _Val3 <- «_==Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    let _Val5 <- «_+Int_» D 1
    guard _Val4
    return _Val5
  | _, _, _ => none

noncomputable def _2af527e : SortInt → SortInt → SortBool → Option SortBool
  | N, D, true => do
    let _Val0 <- «_*Int_» D D
    let _Val1 <- «_<=Int_» _Val0 N
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N D
    let _Val3 <- «_==Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    guard _Val4
    return false
  | _, _, _ => none

noncomputable def _f584763 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «digitAcc(_,_)_VERIFICATION_Int_Int_Int» N 0
    return _Val0

axiom «trialDivisor(_,_,_)_VERIFICATION_Int_Int_Int_Bool» (x0 : SortInt) (x1 : SortInt) (x2 : SortBool) : Option SortInt
axiom _e79459a : SortInt → SortInt → SortBool → Option SortInt

axiom _9ee5ecc : SortInt → SortInt → SortBool → Option SortBool
axiom «trialPrime(_,_,_)_VERIFICATION_Bool_Int_Int_Bool» (x0 : SortInt) (x1 : SortInt) (x2 : SortBool) : Option SortBool

noncomputable def «digitSum(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _f584763 x0

noncomputable def _a0dfaef : SortInt → Option SortBool
  | N => do
    let _Val0 <- «_>=Int_» N 2
    let _Val1 <- «trialPrime(_,_,_)_VERIFICATION_Bool_Int_Int_Bool» N 2 _Val0
    return _Val1

noncomputable def «isPrime(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _a0dfaef x0

mutual
  noncomputable def _50acd05 : SortIntList → SortInt → Option SortInt
    | SortIntList.«intCons(_,_)_VERIFICATION_IntList_Int_IntList» N IS, CUR => do
      let _Val0 <- «_>Int_» N CUR
      let _Val1 <- «isPrime(_)_VERIFICATION_Bool_Int» N
      let _Val2 <- _andBool_ _Val0 _Val1
      let _Val3 <- «largestPrime(_,_)_VERIFICATION_Int_IntList_Int» IS N
      guard _Val2
      return _Val3
    | _, _ => none

  noncomputable def «largestPrime(_,_)_VERIFICATION_Int_IntList_Int» (x0 : SortIntList) (x1 : SortInt) : Option SortInt := (_50acd05 x0 x1) <|> (_cd9cea6 x0 x1) <|> (_db2985f x0 x1)

  noncomputable def _cd9cea6 : SortIntList → SortInt → Option SortInt
    | SortIntList.«intCons(_,_)_VERIFICATION_IntList_Int_IntList» N IS, CUR => do
      let _Val0 <- «_<=Int_» N CUR
      let _Val1 <- «_>Int_» N CUR
      let _Val2 <- «isPrime(_)_VERIFICATION_Bool_Int» N
      let _Val3 <- notBool_ _Val2
      let _Val4 <- _andBool_ _Val1 _Val3
      let _Val5 <- _orBool_ _Val0 _Val4
      let _Val6 <- «largestPrime(_,_)_VERIFICATION_Int_IntList_Int» IS CUR
      guard _Val5
      return _Val6
    | _, _ => none
end