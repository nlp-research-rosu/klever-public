import Klean136LargestSmallestIntegers.Inj

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _105572a : SortK → Option SortBool
  | K => some false

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _d0a8392 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

axiom ListItem (x0 : SortKItem) : Option SortList

def _137740b : SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», B => some B
  | _, _ => none

def _7cbe70e : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom «.Map» : Option SortMap

def _dc0b5ad : SortInt → Option SortVal
  | 0 => some SortVal.«noneV_MPY-CORE_Val»
  | _ => none

def _afef3e3 : SortInt → Option SortVal
  | 0 => some SortVal.«noneV_MPY-CORE_Val»
  | _ => none

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _e4fd59b : SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», OLD => some OLD
  | _, _ => none

def _400db81 : SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», A => some A
  | _, _ => none

axiom «.List» : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def _d36be40 : SortInt → SortInt → Option SortInt
  | A, I => do
    let _Val0 <- «_>=Int_» I 0
    guard _Val0
    return A

def _8b01d7a : SortInt → SortInt → Option SortInt
  | B, I => do
    let _Val0 <- «_<=Int_» I 0
    guard _Val0
    return B

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def «intValue(_)_VERIFICATION_Int_Val» (x0 : SortVal) : Option SortInt := _7cbe70e x0

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _01539d8 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allInts(_)_VERIFICATION_Bool_ValSeq» REST
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allInts(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_01539d8 x0) <|> (_d0a8392 x0)
end

def _866502c : SortInt → SortInt → Option SortInt
  | A, I => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_==Int_» A 0
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return I

def _3a2e957 : SortInt → SortInt → Option SortInt
  | B, I => do
    let _Val0 <- «_>Int_» I 0
    let _Val1 <- «_==Int_» B 0
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return I

mutual
  def _5cc3e50 : SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, _OLD => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «intValue(_)_VERIFICATION_Int_Val» V
      let _Val2 <- «finalValue(_,_)_VERIFICATION_Int_ValSeq_Int» REST _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  def «finalValue(_,_)_VERIFICATION_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := (_5cc3e50 x0 x1) <|> (_e4fd59b x0 x1)
end

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

def _1237184 : SortInt → Option SortVal
  | I => do
    let _Val0 <- «_=/=Int_» I 0
    guard _Val0
    return ((@inj SortInt SortVal) I)

def _ca407d8 : SortInt → SortInt → Option SortInt
  | B, I => do
    let _Val0 <- «_>Int_» I 0
    let _Val1 <- «_=/=Int_» B 0
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» I B
    let _Val4 <- _andBool_ _Val2 _Val3
    guard _Val4
    return I

def _446fec7 : SortInt → SortInt → Option SortInt
  | A, I => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_=/=Int_» A 0
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<=Int_» I A
    let _Val4 <- _andBool_ _Val2 _Val3
    guard _Val4
    return A

def _203dc4d : SortInt → SortInt → Option SortInt
  | B, I => do
    let _Val0 <- «_>Int_» I 0
    let _Val1 <- «_=/=Int_» B 0
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_>=Int_» I B
    let _Val4 <- _andBool_ _Val2 _Val3
    guard _Val4
    return B

def _d79c2f1 : SortInt → Option SortVal
  | I => do
    let _Val0 <- «_=/=Int_» I 0
    guard _Val0
    return ((@inj SortInt SortVal) I)

def _56af667 : SortInt → SortInt → Option SortInt
  | A, I => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_=/=Int_» A 0
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_>Int_» I A
    let _Val4 <- _andBool_ _Val2 _Val3
    guard _Val4
    return I

def «optionalPos(_)_VERIFICATION_Val_Int» (x0 : SortInt) : Option SortVal := (_1237184 x0) <|> (_dc0b5ad x0)

def «posStep(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_203dc4d x0 x1) <|> (_3a2e957 x0 x1) <|> (_8b01d7a x0 x1) <|> (_ca407d8 x0 x1)

def «optionalNeg(_)_VERIFICATION_Val_Int» (x0 : SortInt) : Option SortVal := (_afef3e3 x0) <|> (_d79c2f1 x0)

def «negStep(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_446fec7 x0 x1) <|> (_56af667 x0 x1) <|> (_866502c x0 x1) <|> (_d36be40 x0 x1)

mutual
  def _2bf6c75 : SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, B => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «intValue(_)_VERIFICATION_Int_Val» V
      let _Val2 <- «posStep(_,_)_VERIFICATION_Int_Int_Int» B _Val1
      let _Val3 <- «posFold(_,_)_VERIFICATION_Int_ValSeq_Int» REST _Val2
      guard _Val0
      return _Val3
    | _, _ => none

  def «posFold(_,_)_VERIFICATION_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := (_137740b x0 x1) <|> (_2bf6c75 x0 x1)
end

mutual
  def _1d56dbf : SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, A => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «intValue(_)_VERIFICATION_Int_Val» V
      let _Val2 <- «negStep(_,_)_VERIFICATION_Int_Int_Int» A _Val1
      let _Val3 <- «negFold(_,_)_VERIFICATION_Int_ValSeq_Int» REST _Val2
      guard _Val0
      return _Val3
    | _, _ => none

  def «negFold(_,_)_VERIFICATION_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := (_1d56dbf x0 x1) <|> (_400db81 x0 x1)
end