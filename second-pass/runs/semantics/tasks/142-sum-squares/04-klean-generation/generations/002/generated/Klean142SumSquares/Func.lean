import Klean142SumSquares.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _11819d0 : SortInts → SortInt → Option SortInt
  | SortInts.«.Ints_SUM-SQUARES-VERIFICATION_Ints», I => some I
  | _, _ => none

def _233e0dc : SortInts → SortInt → SortInt → Option SortInt
  | SortInts.«.Ints_SUM-SQUARES-VERIFICATION_Ints», _Gen0, ACC => some ACC
  | _, _, _ => none

def _cc42bb5 : SortInts → SortInt → Option SortInt
  | SortInts.«.Ints_SUM-SQUARES-VERIFICATION_Ints», OLD => some OLD
  | _, _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

mutual
  def _6d64303 : SortInts → SortInt → Option SortInt
    | SortInts.«intCons(_,_)_SUM-SQUARES-VERIFICATION_Ints_Int_Ints» _Gen0 XS, I => do
      let _Val0 <- «_+Int_» I 1
      let _Val1 <- «endIndex(_,_)_SUM-SQUARES-VERIFICATION_Int_Ints_Int» XS _Val0
      return _Val1
    | _, _ => none

  def «endIndex(_,_)_SUM-SQUARES-VERIFICATION_Int_Ints_Int» (x0 : SortInts) (x1 : SortInt) : Option SortInt := (_11819d0 x0 x1) <|> (_6d64303 x0 x1)
end

mutual
  def _2710dca : SortInts → SortInt → Option SortInt
    | SortInts.«intCons(_,_)_SUM-SQUARES-VERIFICATION_Ints_Int_Ints» X XS, _Gen0 => do
      let _Val0 <- «endValue(_,_)_SUM-SQUARES-VERIFICATION_Int_Ints_Int» XS X
      return _Val0
    | _, _ => none

  def «endValue(_,_)_SUM-SQUARES-VERIFICATION_Int_Ints_Int» (x0 : SortInts) (x1 : SortInt) : Option SortInt := (_2710dca x0 x1) <|> (_cc42bb5 x0 x1)
end

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def _d2dab81 : SortInt → SortInt → Option SortInt
  | I, X => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 3
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «_*Int_» X X
    guard _Val1
    return _Val2

noncomputable def _0a6c4eb : SortInt → SortInt → Option SortInt
  | I, X => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 3
    let _Val1 <- «_=/=Int_» _Val0 0
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 4
    let _Val3 <- «_=/=Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    guard _Val4
    return X

noncomputable def _6aad4b1 : SortInt → SortInt → Option SortInt
  | I, X => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 3
    let _Val1 <- «_=/=Int_» _Val0 0
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 4
    let _Val3 <- «_==Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    let _Val5 <- «_*Int_» X X
    let _Val6 <- «_*Int_» _Val5 X
    guard _Val4
    return _Val6

noncomputable def «contribution(_,_)_SUM-SQUARES-VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_0a6c4eb x0 x1) <|> (_6aad4b1 x0 x1) <|> (_d2dab81 x0 x1)

mutual
  noncomputable def «sumSquares(_,_,_)_SUM-SQUARES-VERIFICATION_Int_Ints_Int_Int» (x0 : SortInts) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_233e0dc x0 x1 x2) <|> (_ee47eca x0 x1 x2)

  noncomputable def _ee47eca : SortInts → SortInt → SortInt → Option SortInt
    | SortInts.«intCons(_,_)_SUM-SQUARES-VERIFICATION_Ints_Int_Ints» X XS, I, ACC => do
      let _Val0 <- «_+Int_» I 1
      let _Val1 <- «contribution(_,_)_SUM-SQUARES-VERIFICATION_Int_Int_Int» I X
      let _Val2 <- «_+Int_» ACC _Val1
      let _Val3 <- «sumSquares(_,_,_)_SUM-SQUARES-VERIFICATION_Int_Ints_Int_Int» XS _Val0 _Val2
      return _Val3
    | _, _, _ => none
end