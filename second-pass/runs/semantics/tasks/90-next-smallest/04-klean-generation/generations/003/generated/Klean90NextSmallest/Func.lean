import Klean90NextSmallest.Inj

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _bdc576b : SortInts → Option SortBool
  | SortInts.«consInts(_,_)_NEXT-SMALLEST-VERIFICATION_Ints_Int_Ints» _Gen0 _Gen1 => some false
  | _ => none

def _7c9eb36 : SortInts → Option SortBool
  | SortInts.«nilInts_NEXT-SMALLEST-VERIFICATION_Ints» => some true
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _0d21514 : SortInts → Option SortInts
  | SortInts.«consInts(_,_)_NEXT-SMALLEST-VERIFICATION_Ints_Int_Ints» _Gen0 XS => some XS
  | _ => none

axiom «.Map» : Option SortMap

def _a9065e7 : SortInts → Option SortInt
  | SortInts.«consInts(_,_)_NEXT-SMALLEST-VERIFICATION_Ints_Int_Ints» X _Gen0 => some X
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «.List» : Option SortList

def «intsEmpty(_)_NEXT-SMALLEST-VERIFICATION_Bool_Ints» (x0 : SortInts) : Option SortBool := (_7c9eb36 x0) <|> (_bdc576b x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def «intsTail(_)_NEXT-SMALLEST-VERIFICATION_Ints_Ints» (x0 : SortInts) : Option SortInts := _0d21514 x0

def «intsHead(_)_NEXT-SMALLEST-VERIFICATION_Int_Ints» (x0 : SortInts) : Option SortInt := _a9065e7 x0

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _c68f9d7 : SortInts → SortInt → SortInt → SortInt → Option SortVal
  | IS, _Gen0, N, C => do
    let _Val0 <- «intsEmpty(_)_NEXT-SMALLEST-VERIFICATION_Bool_Ints» IS
    let _Val1 <- «_==Int_» C 2
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return ((@inj SortInt SortVal) N)

def _11f64e6 : SortInts → SortInt → SortInt → SortInt → Option SortVal
  | IS, _Gen0, _Gen1, C => do
    let _Val0 <- «intsEmpty(_)_NEXT-SMALLEST-VERIFICATION_Bool_Ints» IS
    let _Val1 <- «_==Int_» C 2
    let _Val2 <- notBool_ _Val1
    let _Val3 <- _andBool_ _Val0 _Val2
    guard _Val3
    return SortVal.«noneV_MPY-CORE_Val»

axiom _29d7acd : SortInts → SortInt → SortInt → SortInt → Option SortVal
axiom _4d3e91d : SortInts → SortInt → SortInt → SortInt → Option SortVal
axiom _4e28461 : SortInts → SortInt → SortInt → SortInt → Option SortVal
axiom _784fa17 : SortInts → SortInt → SortInt → SortInt → Option SortVal
axiom «nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int» (x0 : SortInts) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortVal
axiom _b0d9be8 : SortInts → SortInt → SortInt → SortInt → Option SortVal
axiom _ffacc98 : SortInts → SortInt → SortInt → SortInt → Option SortVal