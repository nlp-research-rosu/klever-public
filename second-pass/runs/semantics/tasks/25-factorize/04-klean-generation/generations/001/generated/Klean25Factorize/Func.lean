import Klean25Factorize.Inj

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «.List» : Option SortList

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def _b951085 : SortInt → SortInt → SortValSeq → Option SortValSeq
  | N, _D, VS => do
    let _Val0 <- «_<=Int_» N 1
    guard _Val0
    return VS

def _0d6a611 : SortInt → SortInt → Option SortInt
  | N, D => do
    let _Val0 <- «_<=Int_» N 1
    guard _Val0
    return D

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

axiom _898d0ed : SortInt → SortInt → Option SortInt
axiom «factorDivisor(_,_)_FACTORIZE-VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt
axiom _f74f42f : SortInt → SortInt → Option SortInt

axiom _93f80da : SortInt → SortInt → SortValSeq → Option SortValSeq
axiom «factorLoop(_,_,_)_FACTORIZE-VERIFICATION_ValSeq_Int_Int_ValSeq» (x0 : SortInt) (x1 : SortInt) (x2 : SortValSeq) : Option SortValSeq
axiom _a16cb4f : SortInt → SortInt → SortValSeq → Option SortValSeq

noncomputable def _07412d3 : SortInt → Option SortValSeq
  | N => do
    let _Val0 <- «factorLoop(_,_,_)_FACTORIZE-VERIFICATION_ValSeq_Int_Int_ValSeq» N 2 SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    return _Val0

noncomputable def «primeFactors(_)_FACTORIZE-VERIFICATION_ValSeq_Int» (x0 : SortInt) : Option SortValSeq := _07412d3 x0