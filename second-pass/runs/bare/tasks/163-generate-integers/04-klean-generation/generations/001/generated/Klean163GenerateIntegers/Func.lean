import Klean163GenerateIntegers.Inj

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «.List» : Option SortList

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _4a1333b : SortInt → SortInt → SortInt → Option SortList
  | A, B, D => do
    let _Val0 <- «_<=Int_» A D
    let _Val1 <- «_<=Int_» D B
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<=Int_» B D
    let _Val4 <- «_<=Int_» D A
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    let _Val7 <- ListItem ((@inj SortInt SortKItem) D)
    guard _Val6
    return _Val7

noncomputable def _6847e54 : SortInt → SortInt → SortInt → Option SortList
  | A, B, D => do
    let _Val0 <- «_<=Int_» A D
    let _Val1 <- «_<=Int_» D B
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<=Int_» B D
    let _Val4 <- «_<=Int_» D A
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    let _Val7 <- notBool_ _Val6
    let _Val8 <- «.List»
    guard _Val7
    return _Val8

noncomputable def «expectedDigit(_,_,_)_VERIFICATION_List_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortList := (_4a1333b x0 x1 x2) <|> (_6847e54 x0 x1 x2)

noncomputable def _4e80cce : SortInt → SortInt → Option SortList
  | A, B => do
    let _Val0 <- «expectedDigit(_,_,_)_VERIFICATION_List_Int_Int_Int» A B 2
    let _Val1 <- «expectedDigit(_,_,_)_VERIFICATION_List_Int_Int_Int» A B 4
    let _Val2 <- _List_ _Val0 _Val1
    let _Val3 <- «expectedDigit(_,_,_)_VERIFICATION_List_Int_Int_Int» A B 6
    let _Val4 <- _List_ _Val2 _Val3
    let _Val5 <- «expectedDigit(_,_,_)_VERIFICATION_List_Int_Int_Int» A B 8
    let _Val6 <- _List_ _Val4 _Val5
    return _Val6

noncomputable def «expected(_,_)_VERIFICATION_List_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortList := _4e80cce x0 x1