import Klean102ChooseNum.Inj

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

axiom ListItem (x0 : SortKItem) : Option SortList

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.Map» : Option SortMap

axiom «.List» : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def _fae664e : SortInt → SortInt → Option SortInt
  | X, Y => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» Y 2
    let _Val1 <- «_-Int_» Y _Val0
    let _Val2 <- «_<=Int_» X _Val1
    let _Val3 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» Y 2
    let _Val4 <- «_-Int_» Y _Val3
    let _Val5 <- kite _Val2 _Val4 (-1)
    return _Val5

noncomputable def «largestEvenInRange(_,_)_CHOOSE-NUM-VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _fae664e x0 x1