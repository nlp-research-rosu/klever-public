import Klean133SumSquares.Inj

def _a4a7830 : SortPosNat → Option SortInt
  | SortPosNat.ten => some 10
  | _ => none

def _111a569 : SortInt → SortPList → Option SortInt
  | A, SortPList.nil => some A
  | _, _ => none

def _0cf822b : SortNumValue → Option SortInt
  | SortNumValue.intVal I => some I
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _25bd9ec : SortPosNat → Option SortInt
  | SortPosNat.one => some 1
  | _ => none

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _6028faa : SortPosNat → Option SortInt
    | SortPosNat.next P => do
      let _Val0 <- «posInt(_)_MPY-DOMAIN_Int_PosNat» P
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «posInt(_)_MPY-DOMAIN_Int_PosNat» (x0 : SortPosNat) : Option SortInt := (_25bd9ec x0) <|> (_6028faa x0) <|> (_a4a7830 x0)
end

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

def _83dcf9b : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_=/=Int_» I2 0
    let _Val1 <- _modInt_ I1 I2
    let _Val2 <- «_-Int_» I1 _Val1
    let _Val3 <- «_/Int_» _Val2 I2
    guard _Val0
    return _Val3

def _divInt_ (x0 : SortInt) (x1 : SortInt) : Option SortInt := _83dcf9b x0 x1

def _4e3bca4 : SortNumValue → Option SortInt
  | SortNumValue.ratVal N D => do
    let _Val0 <- «_-Int_» 0 N
    let _Val1 <- «posInt(_)_MPY-DOMAIN_Int_PosNat» D
    let _Val2 <- _divInt_ _Val0 _Val1
    let _Val3 <- «_-Int_» 0 _Val2
    return _Val3
  | _ => none

def «ceilInt(_)_MPY-DOMAIN_Int_NumValue» (x0 : SortNumValue) : Option SortInt := (_0cf822b x0) <|> (_4e3bca4 x0)

def _f1adef5 : SortNumValue → Option SortInt
  | V => do
    let _Val0 <- «ceilInt(_)_MPY-DOMAIN_Int_NumValue» V
    let _Val1 <- «ceilInt(_)_MPY-DOMAIN_Int_NumValue» V
    let _Val2 <- «_*Int_» _Val0 _Val1
    return _Val2

def «squareCeil(_)_VERIFICATION_Int_NumValue» (x0 : SortNumValue) : Option SortInt := _f1adef5 x0

mutual
  def _34b829d : SortInt → SortPList → Option SortInt
    | A, SortPList.cons V VS => do
      let _Val0 <- «squareCeil(_)_VERIFICATION_Int_NumValue» V
      let _Val1 <- «_+Int_» A _Val0
      let _Val2 <- «sumSquaresFrom(_,_)_VERIFICATION_Int_Int_PList» _Val1 VS
      return _Val2
    | _, _ => none

  def «sumSquaresFrom(_,_)_VERIFICATION_Int_Int_PList» (x0 : SortInt) (x1 : SortPList) : Option SortInt := (_111a569 x0 x1) <|> (_34b829d x0 x1)
end

def _dc184e5 : SortPList → Option SortInt
  | VS => do
    let _Val0 <- «sumSquaresFrom(_,_)_VERIFICATION_Int_Int_PList» 0 VS
    return _Val0

def «sumSquares(_)_VERIFICATION_Int_PList» (x0 : SortPList) : Option SortInt := _dc184e5 x0