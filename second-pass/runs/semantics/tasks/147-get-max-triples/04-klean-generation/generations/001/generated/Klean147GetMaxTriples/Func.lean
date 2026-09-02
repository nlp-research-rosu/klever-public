import Klean147GetMaxTriples.Inj

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

axiom «.List» : Option SortList

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

noncomputable def _73f48db : SortInt → Option SortInt
  | C => do
    let _Val0 <- «_-Int_» C 1
    let _Val1 <- «_*Int_» C _Val0
    let _Val2 <- «_-Int_» C 2
    let _Val3 <- «_*Int_» _Val1 _Val2
    let _Val4 <- «_-Int_» C 1
    let _Val5 <- «_*Int_» C _Val4
    let _Val6 <- «_-Int_» C 2
    let _Val7 <- «_*Int_» _Val5 _Val6
    let _Val8 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val7 6
    let _Val9 <- «_-Int_» _Val3 _Val8
    let _Val10 <- «_/Int_» _Val9 6
    return _Val10

noncomputable def _d725e94 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_+Int_» N 1
    let _Val1 <- «_+Int_» N 1
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val1 3
    let _Val3 <- «_-Int_» _Val0 _Val2
    let _Val4 <- «_/Int_» _Val3 3
    return _Val4

noncomputable def «chooseThree(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _73f48db x0

noncomputable def «zeroResidues(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _d725e94 x0

noncomputable def _84f363c : SortInt → Option SortInt
  | N => do
    let _Val0 <- «zeroResidues(_)_VERIFICATION_Int_Int» N
    let _Val1 <- «chooseThree(_)_VERIFICATION_Int_Int» _Val0
    let _Val2 <- «zeroResidues(_)_VERIFICATION_Int_Int» N
    let _Val3 <- «_-Int_» N _Val2
    let _Val4 <- «chooseThree(_)_VERIFICATION_Int_Int» _Val3
    let _Val5 <- «_+Int_» _Val1 _Val4
    return _Val5

noncomputable def «tripleCount(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _84f363c x0