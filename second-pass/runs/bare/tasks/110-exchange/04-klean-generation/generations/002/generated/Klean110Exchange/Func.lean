import Klean110Exchange.Inj

def _a3ead1c : SortPyList → Option SortInt
  | SortPyList.Nil => some 0
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _54a2537 : SortPyList → SortInt → Option SortInt
  | SortPyList.Nil, DEFAULT => some DEFAULT
  | _, _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _0d31010 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_%Int_» I 2
    let _Val1 <- «_==Int_» _Val0 0
    guard _Val1
    return 1

mutual
  def _7155794 : SortPyList → SortInt → Option SortInt
    | SortPyList.Cons I REST, _Gen0 => do
      let _Val0 <- «lastValue(_,_)_VERIFICATION_Int_PyList_Int» REST I
      return _Val0
    | _, _ => none

  def «lastValue(_,_)_VERIFICATION_Int_PyList_Int» (x0 : SortPyList) (x1 : SortInt) : Option SortInt := (_54a2537 x0 x1) <|> (_7155794 x0 x1)
end

noncomputable def _6515011 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_%Int_» I 2
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- notBool_ _Val1
    guard _Val2
    return 0

noncomputable def «evenBit(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_0d31010 x0) <|> (_6515011 x0)

mutual
  noncomputable def «countEven(_)_VERIFICATION_Int_PyList» (x0 : SortPyList) : Option SortInt := (_a3ead1c x0) <|> (_fdaf77e x0)

  noncomputable def _fdaf77e : SortPyList → Option SortInt
    | SortPyList.Cons I REST => do
      let _Val0 <- «evenBit(_)_VERIFICATION_Int_Int» I
      let _Val1 <- «countEven(_)_VERIFICATION_Int_PyList» REST
      let _Val2 <- «_+Int_» _Val0 _Val1
      return _Val2
    | _ => none
end