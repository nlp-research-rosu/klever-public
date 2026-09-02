import Klean5Intersperse.Inj

def _eef6ae2 : SortValSeq → SortValSeq → SortInt → Option SortValSeq
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some ACC
  | _, _, _ => none

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

axiom «.List» : Option SortList

def _fd52cb1 : SortVal → SortValSeq → Option SortVal
  | OLD, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some OLD
  | _, _ => none

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

mutual
  def _8f944ab : SortVal → SortValSeq → Option SortVal
    | _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «lastNumber(_,_)_INTERSPERSE-VERIFICATION_Val_Val_ValSeq» V REST
      return _Val0
    | _, _ => none

  def «lastNumber(_,_)_INTERSPERSE-VERIFICATION_Val_Val_ValSeq» (x0 : SortVal) (x1 : SortValSeq) : Option SortVal := (_8f944ab x0 x1) <|> (_fd52cb1 x0 x1)
end

mutual
  def _4580d60 : SortValSeq → SortValSeq → SortInt → Option SortValSeq
    | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, D => do
      let _Val0 <- «intersperseAcc(_,_,_)_INTERSPERSE-VERIFICATION_ValSeq_ValSeq_ValSeq_Int» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq») REST D
      return _Val0
    | _, _, _ => none

  def _4de75aa : SortValSeq → SortValSeq → SortInt → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A AS, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, D => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A AS) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) D) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val1 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Val0 (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val2 <- «intersperseAcc(_,_,_)_INTERSPERSE-VERIFICATION_ValSeq_ValSeq_ValSeq_Int» _Val1 REST D
      return _Val2
    | _, _, _ => none

  def «intersperseAcc(_,_,_)_INTERSPERSE-VERIFICATION_ValSeq_ValSeq_ValSeq_Int» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortInt) : Option SortValSeq := (_4580d60 x0 x1 x2) <|> (_4de75aa x0 x1 x2) <|> (_eef6ae2 x0 x1 x2)
end

def _e6abd1f : SortValSeq → SortInt → Option SortValSeq
  | NUMBERS, D => do
    let _Val0 <- «intersperseAcc(_,_,_)_INTERSPERSE-VERIFICATION_ValSeq_ValSeq_ValSeq_Int» SortValSeq.«.ValSeq_MPY-CORE_ValSeq» NUMBERS D
    return _Val0

def «intersperseVS(_,_)_INTERSPERSE-VERIFICATION_ValSeq_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortValSeq := _e6abd1f x0 x1