import Klean97Multiply.Inj

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

axiom «.List» : Option SortList

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.Map» : Option SortMap

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

noncomputable def _f7cf927 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 10
    return _Val0

noncomputable def «unitDigit(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _f7cf927 x0

noncomputable def _724d961 : SortInt → SortInt → Option SortInt
  | A, B => do
    let _Val0 <- «unitDigit(_)_VERIFICATION_Int_Int» A
    let _Val1 <- «unitDigit(_)_VERIFICATION_Int_Int» B
    let _Val2 <- «_*Int_» _Val0 _Val1
    return _Val2

noncomputable def «unitDigitProduct(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _724d961 x0 x1