import Klean94Skjkasdkd.Inj

def _48de78d : SortInt → SortInt → SortBool → Option SortBool
  | _Gen0, _Gen1, false => some false
  | _, _, _ => none

def _6239c81 : SortInt → SortInt → SortBool → Option SortInt
  | _Gen0, D, false => some D
  | _, _, _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «digitAcc(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _db2985f : SortIntList → SortInt → Option SortInt
  | SortIntList.«.IntList_VERIFICATION_IntList», CUR => some CUR
  | _, _ => none

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

noncomputable def _f584763 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «digitAcc(_,_)_VERIFICATION_Int_Int_Int» N 0
    return _Val0

def «largestPrime(_,_)_VERIFICATION_Int_IntList_Int» (x0 : SortIntList) (x1 : SortInt) : Option SortInt := _db2985f x0 x1

def «trialDivisor(_,_,_)_VERIFICATION_Int_Int_Int_Bool» (x0 : SortInt) (x1 : SortInt) (x2 : SortBool) : Option SortInt := (_6239c81 x0 x1 x2) <|> (_b2f455e x0 x1 x2)

def «trialPrime(_,_,_)_VERIFICATION_Bool_Int_Int_Bool» (x0 : SortInt) (x1 : SortInt) (x2 : SortBool) : Option SortBool := (_48de78d x0 x1 x2) <|> (_f49a4ea x0 x1 x2)

noncomputable def «digitSum(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _f584763 x0

def _a0dfaef : SortInt → Option SortBool
  | N => do
    let _Val0 <- «_>=Int_» N 2
    let _Val1 <- «trialPrime(_,_,_)_VERIFICATION_Bool_Int_Int_Bool» N 2 _Val0
    return _Val1

def «isPrime(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _a0dfaef x0