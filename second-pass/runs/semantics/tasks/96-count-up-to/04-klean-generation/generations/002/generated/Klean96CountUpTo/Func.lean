import Klean96CountUpTo.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _d0966d1 : SortValSeq → SortInt → SortBool → Option SortValSeq
  | VS, _Gen0, false => some VS
  | _, _, _ => none

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom «.List» : Option SortList

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «.Map» : Option SortMap

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def _c1d5bde : SortInt → SortInt → SortInt → Option SortBool
  | _Gen0, D, HI => do
    let _Val0 <- «_>=Int_» D HI
    guard _Val0
    return true

def _1a960bc : SortValSeq → SortInt → SortInt → Option SortValSeq
  | VS, I, N => do
    let _Val0 <- «_>=Int_» I N
    guard _Val0
    return VS

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def _b5bdd0e : SortValSeq → SortInt → SortBool → Option SortValSeq
  | VS, I, true => do
    let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» VS (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) I) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    return _Val0
  | _, _, _ => none

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

def appendIfPrime (x0 : SortValSeq) (x1 : SortInt) (x2 : SortBool) : Option SortValSeq := (_b5bdd0e x0 x1 x2) <|> (_d0966d1 x0 x1 x2)

noncomputable def _268434e : SortInt → SortInt → SortInt → Option SortBool
  | C, D, HI => do
    let _Val0 <- «_<Int_» D HI
    let _Val1 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» C D
    let _Val2 <- «_==Int_» _Val1 0
    let _Val3 <- _andBool_ _Val0 _Val2
    guard _Val3
    return false

axiom _0f51e5c : SortInt → SortInt → SortInt → Option SortBool
axiom noDivisor (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortBool

axiom primesAcc (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) : Option SortValSeq
axiom _c7631a7 : SortValSeq → SortInt → SortInt → Option SortValSeq