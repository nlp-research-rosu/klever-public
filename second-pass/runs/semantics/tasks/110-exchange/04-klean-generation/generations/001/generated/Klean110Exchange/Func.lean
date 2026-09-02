import Klean110Exchange.Inj

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _613a8c4 : SortInt → SortIntSeq → Option SortInt
  | A, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some A
  | _, _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _b0561ee : SortInt → SortIntSeq → Option SortInt
  | A, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some A
  | _, _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

mutual
  noncomputable def _20f54cb : SortInt → SortIntSeq → Option SortInt
    | A, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I R => do
      let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
      let _Val1 <- «_==Int_» _Val0 0
      let _Val2 <- «oddAcc(_,_)_EXCHANGE-VERIFICATION_Int_Int_IntSeq» A R
      guard _Val1
      return _Val2
    | _, _ => none

  noncomputable def «oddAcc(_,_)_EXCHANGE-VERIFICATION_Int_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortInt := (_20f54cb x0 x1) <|> (_613a8c4 x0 x1) <|> (_fa7e100 x0 x1)

  noncomputable def _fa7e100 : SortInt → SortIntSeq → Option SortInt
    | A, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I R => do
      let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
      let _Val1 <- «_=/=Int_» _Val0 0
      let _Val2 <- «_+Int_» A 1
      let _Val3 <- «oddAcc(_,_)_EXCHANGE-VERIFICATION_Int_Int_IntSeq» _Val2 R
      guard _Val1
      return _Val3
    | _, _ => none
end

mutual
  noncomputable def _2f91593 : SortInt → SortIntSeq → Option SortInt
    | A, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I R => do
      let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
      let _Val1 <- «_=/=Int_» _Val0 0
      let _Val2 <- «evenAcc(_,_)_EXCHANGE-VERIFICATION_Int_Int_IntSeq» A R
      guard _Val1
      return _Val2
    | _, _ => none

  noncomputable def «evenAcc(_,_)_EXCHANGE-VERIFICATION_Int_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortInt := (_2f91593 x0 x1) <|> (_b0561ee x0 x1) <|> (_c8f2a84 x0 x1)

  noncomputable def _c8f2a84 : SortInt → SortIntSeq → Option SortInt
    | A, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I R => do
      let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
      let _Val1 <- «_==Int_» _Val0 0
      let _Val2 <- «_+Int_» A 1
      let _Val3 <- «evenAcc(_,_)_EXCHANGE-VERIFICATION_Int_Int_IntSeq» _Val2 R
      guard _Val1
      return _Val3
    | _, _ => none
end

noncomputable def _e53561b : SortIntSeq → SortIntSeq → Option SortVal
  | A, B => do
    let _Val0 <- «oddAcc(_,_)_EXCHANGE-VERIFICATION_Int_Int_IntSeq» 0 A
    let _Val1 <- «evenAcc(_,_)_EXCHANGE-VERIFICATION_Int_Int_IntSeq» 0 B
    let _Val2 <- «_>Int_» _Val0 _Val1
    guard _Val2
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 78 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 79 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))))

noncomputable def _aecc062 : SortIntSeq → SortIntSeq → Option SortVal
  | A, B => do
    let _Val0 <- «oddAcc(_,_)_EXCHANGE-VERIFICATION_Int_Int_IntSeq» 0 A
    let _Val1 <- «evenAcc(_,_)_EXCHANGE-VERIFICATION_Int_Int_IntSeq» 0 B
    let _Val2 <- «_<=Int_» _Val0 _Val1
    guard _Val2
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 89 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 69 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 83 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))))

noncomputable def «exchangeResult(_,_)_EXCHANGE-VERIFICATION_Val_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortVal := (_aecc062 x0 x1) <|> (_e53561b x0 x1)