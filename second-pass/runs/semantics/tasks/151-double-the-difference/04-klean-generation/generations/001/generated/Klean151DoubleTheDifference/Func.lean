import Klean151DoubleTheDifference.Inj

def _7d6a4a9 : SortNumSeq → SortVal → Option SortVal
  | SortNumSeq.«.NumSeq_DOUBLE-THE-DIFFERENCE-VERIFICATION_NumSeq», OLD => some OLD
  | _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _02791b8 : SortNumSeq → Option SortInt
  | SortNumSeq.«.NumSeq_DOUBLE-THE-DIFFERENCE-VERIFICATION_NumSeq» => some 0
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom ListItem (x0 : SortKItem) : Option SortList

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.List» : Option SortList

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

axiom «.Map» : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

mutual
  def _5d25368 : SortNumSeq → SortVal → Option SortVal
    | SortNumSeq.«fNum(_,_)_DOUBLE-THE-DIFFERENCE-VERIFICATION_NumSeq_Float_NumSeq» F REST, _OLD => do
      let _Val0 <- «finalNumber(_,_)_DOUBLE-THE-DIFFERENCE-VERIFICATION_Val_NumSeq_Val» REST ((@inj SortFloat SortVal) F)
      return _Val0
    | _, _ => none

  def _6527251 : SortNumSeq → SortVal → Option SortVal
    | SortNumSeq.«iNum(_,_)_DOUBLE-THE-DIFFERENCE-VERIFICATION_NumSeq_Int_NumSeq» I REST, _OLD => do
      let _Val0 <- «finalNumber(_,_)_DOUBLE-THE-DIFFERENCE-VERIFICATION_Val_NumSeq_Val» REST ((@inj SortInt SortVal) I)
      return _Val0
    | _, _ => none

  def «finalNumber(_,_)_DOUBLE-THE-DIFFERENCE-VERIFICATION_Val_NumSeq_Val» (x0 : SortNumSeq) (x1 : SortVal) : Option SortVal := (_5d25368 x0 x1) <|> (_6527251 x0 x1) <|> (_7d6a4a9 x0 x1)
end

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def _f5e832d : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_>Int_» I 0
    let _Val1 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
    let _Val2 <- «_==Int_» _Val1 1
    let _Val3 <- _andBool_ _Val0 _Val2
    let _Val4 <- «_*Int_» I I
    let _Val5 <- kite _Val3 _Val4 0
    return _Val5

noncomputable def «oddSquare(_)_DOUBLE-THE-DIFFERENCE-VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _f5e832d x0

mutual
  noncomputable def _0c678e8 : SortNumSeq → Option SortInt
    | SortNumSeq.«iNum(_,_)_DOUBLE-THE-DIFFERENCE-VERIFICATION_NumSeq_Int_NumSeq» I REST => do
      let _Val0 <- «oddSquare(_)_DOUBLE-THE-DIFFERENCE-VERIFICATION_Int_Int» I
      let _Val1 <- «doubleDifferenceSpec(_)_DOUBLE-THE-DIFFERENCE-VERIFICATION_Int_NumSeq» REST
      let _Val2 <- «_+Int_» _Val0 _Val1
      return _Val2
    | _ => none

  noncomputable def _7c202b7 : SortNumSeq → Option SortInt
    | SortNumSeq.«fNum(_,_)_DOUBLE-THE-DIFFERENCE-VERIFICATION_NumSeq_Float_NumSeq» _F REST => do
      let _Val0 <- «doubleDifferenceSpec(_)_DOUBLE-THE-DIFFERENCE-VERIFICATION_Int_NumSeq» REST
      return _Val0
    | _ => none

  noncomputable def «doubleDifferenceSpec(_)_DOUBLE-THE-DIFFERENCE-VERIFICATION_Int_NumSeq» (x0 : SortNumSeq) : Option SortInt := (_02791b8 x0) <|> (_0c678e8 x0) <|> (_7c202b7 x0)
end