import Klean9RollingMax.Inj

def _0c5a2a5 : SortBool → SortInt → SortInt → Option SortInt
  | true, _M, I => some I
  | _, _, _ => none

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _27cd65e : SortIntSeq → SortBool → SortInt → SortValSeq → Option SortValSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _F, _M, ACC => some ACC
  | _, _, _, _ => none

def _3cd4b09 : SortIntSeq → SortBool → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _F, M => some M
  | _, _, _ => none

def _740b7f0 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», N => some N
  | _, _ => none

def _64813b0 : SortIntSeq → SortBool → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _I _R, _F => some false
  | _, _ => none

def _9407ea6 : SortIntSeq → SortBool → Option SortBool
  | _IS, false => some false
  | _, _ => none

def _94e6ee6 : SortIntSeq → SortBool → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», F => some F
  | _, _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def _27936ba : SortBool → SortInt → SortInt → Option SortInt
  | false, M, I => do
    let _Val0 <- «maxInt(_,_)_INT-COMMON_Int_Int_Int» M I
    return _Val0
  | _, _, _ => none

mutual
  def _463d0da : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I R, _N => do
      let _Val0 <- «numberAfter(_,_)_VERIFICATION_Int_IntSeq_Int» R I
      return _Val0
    | _, _ => none

  def «numberAfter(_,_)_VERIFICATION_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_463d0da x0 x1) <|> (_740b7f0 x0 x1)
end

def «firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» (x0 : SortIntSeq) (x1 : SortBool) : Option SortBool := (_64813b0 x0 x1) <|> (_9407ea6 x0 x1) <|> (_94e6ee6 x0 x1)

def «nextRolling(_,_,_)_VERIFICATION_Int_Bool_Int_Int» (x0 : SortBool) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_0c5a2a5 x0 x1 x2) <|> (_27936ba x0 x1 x2)

mutual
  def _044e5c6 : SortIntSeq → SortBool → SortInt → SortValSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I R, F, M, ACC => do
      let _Val0 <- «nextRolling(_,_,_)_VERIFICATION_Int_Bool_Int_Int» F M I
      let _Val1 <- «nextRolling(_,_,_)_VERIFICATION_Int_Bool_Int_Int» F M I
      let _Val2 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) _Val1) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val3 <- «rollingAcc(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Bool_Int_ValSeq» R false _Val0 _Val2
      return _Val3
    | _, _, _, _ => none

  def «rollingAcc(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Bool_Int_ValSeq» (x0 : SortIntSeq) (x1 : SortBool) (x2 : SortInt) (x3 : SortValSeq) : Option SortValSeq := (_044e5c6 x0 x1 x2 x3) <|> (_27cd65e x0 x1 x2 x3)
end

mutual
  def _42a5711 : SortIntSeq → SortBool → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I R, F, M => do
      let _Val0 <- «nextRolling(_,_,_)_VERIFICATION_Int_Bool_Int_Int» F M I
      let _Val1 <- «maximumAfter(_,_,_)_VERIFICATION_Int_IntSeq_Bool_Int» R false _Val0
      return _Val1
    | _, _, _ => none

  def «maximumAfter(_,_,_)_VERIFICATION_Int_IntSeq_Bool_Int» (x0 : SortIntSeq) (x1 : SortBool) (x2 : SortInt) : Option SortInt := (_3cd4b09 x0 x1 x2) <|> (_42a5711 x0 x1 x2)
end