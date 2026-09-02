import Klean1SeparateParenGroups.Inj

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

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

axiom ListItem (x0 : SortKItem) : Option SortList

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _67a3980 : SortIntSeq → SortIntSeq → SortInt → SortValSeq → Option SortValSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _CUR, _DEPTH, ACC => some ACC
  | _, _, _, _ => none

def _b51c292 : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _936a810 : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», DEPTH => do
    let _Val0 <- «_==Int_» DEPTH 0
    return _Val0
  | _, _ => none

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

mutual
  def _70bb17c : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST => do
      let _Val0 <- «_==Int_» C 32
      let _Val1 <- «_==Int_» C 40
      let _Val2 <- _orBool_ _Val0 _Val1
      let _Val3 <- «_==Int_» C 41
      let _Val4 <- _orBool_ _Val2 _Val3
      let _Val5 <- «parenSpaceOnly(_)_VERIFICATION_Bool_IntSeq» REST
      let _Val6 <- _andBool_ _Val4 _Val5
      return _Val6
    | _ => none

  def «parenSpaceOnly(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_70bb17c x0) <|> (_b51c292 x0)
end

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

mutual
  def _1b31821 : SortIntSeq → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 40 REST, DEPTH => do
      let _Val0 <- «_+Int_» DEPTH 1
      let _Val1 <- «balancedTail(_,_)_VERIFICATION_Bool_IntSeq_Int» REST _Val0
      return _Val1
    | _, _ => none

  def _6634a71 : SortIntSeq → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST, DEPTH => do
      let _Val0 <- «_=/=Int_» C 32
      let _Val1 <- «_=/=Int_» C 40
      let _Val2 <- _andBool_ _Val0 _Val1
      let _Val3 <- «_==Int_» C 41
      let _Val4 <- «_>Int_» DEPTH 0
      let _Val5 <- _andBool_ _Val3 _Val4
      let _Val6 <- «_-Int_» DEPTH 1
      let _Val7 <- «balancedTail(_,_)_VERIFICATION_Bool_IntSeq_Int» REST _Val6
      let _Val8 <- _andBool_ _Val5 _Val7
      guard _Val2
      return _Val8
    | _, _ => none

  def «balancedTail(_,_)_VERIFICATION_Bool_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortBool := (_1b31821 x0 x1) <|> (_6634a71 x0 x1) <|> (_936a810 x0 x1) <|> (_b0c3abe x0 x1)

  def _b0c3abe : SortIntSeq → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 REST, DEPTH => do
      let _Val0 <- «balancedTail(_,_)_VERIFICATION_Bool_IntSeq_Int» REST DEPTH
      return _Val0
    | _, _ => none
end

axiom _4cd0922 : SortInt → SortIntSeq → SortIntSeq → SortInt → SortValSeq → Option SortValSeq
axiom _582e33c : SortIntSeq → SortIntSeq → SortInt → SortValSeq → Option SortValSeq
axiom «scanClose(_,_,_,_,_)_VERIFICATION_ValSeq_Int_IntSeq_IntSeq_Int_ValSeq» (x0 : SortInt) (x1 : SortIntSeq) (x2 : SortIntSeq) (x3 : SortInt) (x4 : SortValSeq) : Option SortValSeq
axiom «scanGroups(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_IntSeq_Int_ValSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortInt) (x3 : SortValSeq) : Option SortValSeq
axiom _c3323f2 : SortIntSeq → SortIntSeq → SortInt → SortValSeq → Option SortValSeq
axiom _ca6cab0 : SortIntSeq → SortIntSeq → SortInt → SortValSeq → Option SortValSeq
axiom _f8e7de8 : SortInt → SortIntSeq → SortIntSeq → SortInt → SortValSeq → Option SortValSeq