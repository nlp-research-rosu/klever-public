import Klean151DoubleTheDifference.Inj

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _75391d9 : SortVals → SortInt → Option SortInt
  | SortVals.«nil_MPY-SYNTAX_Vals», ACC => some ACC
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _ab26d3e : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «_%Int_» I 2
    let _Val2 <- «_==Int_» _Val1 1
    let _Val3 <- _andBool_ _Val0 _Val2
    let _Val4 <- «_*Int_» I I
    guard _Val3
    return _Val4

noncomputable def _2deb552 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «_%Int_» I 2
    let _Val2 <- «_==Int_» _Val1 1
    let _Val3 <- _andBool_ _Val0 _Val2
    let _Val4 <- notBool_ _Val3
    guard _Val4
    return 0

noncomputable def «selectedSquare(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_2deb552 x0) <|> (_ab26d3e x0)

mutual
  noncomputable def _4fe2896 : SortVals → SortInt → Option SortInt
    | SortVals.«boolCons(_,_)_MPY-SYNTAX_Vals_Bool_Vals» false VS, ACC => do
      let _Val0 <- «oddSquareFold(_,_)_VERIFICATION_Int_Vals_Int» VS ACC
      return _Val0
    | _, _ => none

  noncomputable def _6a4e957 : SortVals → SortInt → Option SortInt
    | SortVals.«floatCons(_,_)_MPY-SYNTAX_Vals_Float_Vals» _Gen0 VS, ACC => do
      let _Val0 <- «oddSquareFold(_,_)_VERIFICATION_Int_Vals_Int» VS ACC
      return _Val0
    | _, _ => none

  noncomputable def _72d289c : SortVals → SortInt → Option SortInt
    | SortVals.«intCons(_,_)_MPY-SYNTAX_Vals_Int_Vals» I VS, ACC => do
      let _Val0 <- «selectedSquare(_)_VERIFICATION_Int_Int» I
      let _Val1 <- «_+Int_» ACC _Val0
      let _Val2 <- «oddSquareFold(_,_)_VERIFICATION_Int_Vals_Int» VS _Val1
      return _Val2
    | _, _ => none

  noncomputable def _8893292 : SortVals → SortInt → Option SortInt
    | SortVals.«boolCons(_,_)_MPY-SYNTAX_Vals_Bool_Vals» true VS, ACC => do
      let _Val0 <- «_+Int_» ACC 1
      let _Val1 <- «oddSquareFold(_,_)_VERIFICATION_Int_Vals_Int» VS _Val0
      return _Val1
    | _, _ => none

  noncomputable def «oddSquareFold(_,_)_VERIFICATION_Int_Vals_Int» (x0 : SortVals) (x1 : SortInt) : Option SortInt := (_4fe2896 x0 x1) <|> (_6a4e957 x0 x1) <|> (_72d289c x0 x1) <|> (_75391d9 x0 x1) <|> (_8893292 x0 x1) <|> (_d1e4987 x0 x1)

  noncomputable def _d1e4987 : SortVals → SortInt → Option SortInt
    | SortVals.«listCons(_,_)_MPY-SYNTAX_Vals_Vals_Vals» _Gen0 VS, ACC => do
      let _Val0 <- «oddSquareFold(_,_)_VERIFICATION_Int_Vals_Int» VS ACC
      return _Val0
    | _, _ => none
end