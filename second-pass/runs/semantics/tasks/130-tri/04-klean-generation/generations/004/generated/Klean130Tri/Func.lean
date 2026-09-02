import Klean130Tri.Inj

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «.List» : Option SortList

axiom triAt (x0 : SortInt) : Option SortInt

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom prefixIndex (x0 : SortValSeq) : Option SortInt

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1