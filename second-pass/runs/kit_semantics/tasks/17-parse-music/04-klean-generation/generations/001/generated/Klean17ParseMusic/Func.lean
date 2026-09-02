import Klean17ParseMusic.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _543cd7c : SortIntSeq → SortInt → SortValSeq → Option SortValSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0, ACC => some ACC
  | _, _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _f771d88 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», CUR => some CUR
  | _, _ => none

noncomputable local instance : DecidableEq SortKItem :=
  Classical.typeDecidableEq SortKItem

private noncomputable def kleanMapLookupModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Option SortKItem :=
  match entries with
  | [] => none
  | (candidate, value) :: rest =>
      if candidate = key then some value
      else kleanMapLookupModel rest key

private noncomputable def kleanMapContainsModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Bool :=
  match entries with
  | [] => false
  | (candidate, _) :: rest =>
      if candidate = key then true
      else kleanMapContainsModel rest key

private noncomputable def kleanMapDisjointModel
    (left right : List (SortKItem × SortKItem)) : Bool :=
  match right with
  | [] => true
  | (key, _) :: rest =>
      if kleanMapContainsModel left key then false
      else kleanMapDisjointModel left rest

private noncomputable def kleanMapDeleteModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => []
  | (candidate, value) :: rest =>
      if candidate = key then kleanMapDeleteModel rest key
      else (candidate, value) :: kleanMapDeleteModel rest key

private noncomputable def kleanMapUpdateModel
    (entries : List (SortKItem × SortKItem))
    (key value : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => [(key, value)]
  | (candidate, oldValue) :: rest =>
      if candidate = key then (key, value) :: rest
      else (candidate, oldValue) :: kleanMapUpdateModel rest key value

noncomputable def «.List» : Option SortList := some ⟨[]⟩

noncomputable def «.Map» : Option SortMap := some ⟨[]⟩

noncomputable def _List_ (x0 : SortList) (x1 : SortList) : Option SortList := some ⟨x0.coll ++ x1.coll⟩

noncomputable def _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap :=
  if kleanMapDisjointModel x0.coll x1.coll then
    some ⟨x0.coll ++ x1.coll⟩
  else none

noncomputable def «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=
  some ⟨[(x0, x1)]⟩

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

def _201e5c6 : SortInt → SortInt → Option SortInt
  | C, _Gen0 => do
    let _Val0 <- «_==Int_» C 111
    guard _Val0
    return 4

def _3705d20 : SortInt → SortInt → Option SortInt
  | C, _Gen0 => do
    let _Val0 <- «_==Int_» C 46
    guard _Val0
    return 1

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _3789647 : SortValSeq → SortInt → SortInt → Option SortValSeq
  | ACC, C, CUR => do
    let _Val0 <- «_==Int_» C 124
    let _Val1 <- «_==Int_» CUR 4
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) 2) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    guard _Val2
    return _Val3

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

def _3c90424 : SortValSeq → SortInt → SortInt → Option SortValSeq
  | ACC, C, CUR => do
    let _Val0 <- «_==Int_» C 124
    let _Val1 <- «_=/=Int_» CUR 4
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) CUR) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    guard _Val2
    return _Val3

def _9546197 : SortInt → SortInt → Option SortInt
  | C, _Gen0 => do
    let _Val0 <- «_=/=Int_» C 111
    let _Val1 <- «_=/=Int_» C 46
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return 0

def _a873fe5 : SortValSeq → SortInt → SortInt → Option SortValSeq
  | ACC, C, CUR => do
    let _Val0 <- «_==Int_» C 111
    let _Val1 <- «_==Int_» C 46
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_=/=Int_» C 124
    let _Val4 <- «_=/=Int_» CUR 4
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    guard _Val6
    return ACC

def _a95cde8 : SortValSeq → SortInt → SortInt → Option SortValSeq
  | ACC, C, CUR => do
    let _Val0 <- «_=/=Int_» C 111
    let _Val1 <- «_=/=Int_» C 46
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_=/=Int_» C 124
    let _Val4 <- _andBool_ _Val2 _Val3
    let _Val5 <- «_==Int_» CUR 4
    let _Val6 <- _andBool_ _Val4 _Val5
    let _Val7 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) 4) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    guard _Val6
    return _Val7

def «nextCurrent(_,_)_VERIFICATION-SYNTAX_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_201e5c6 x0 x1) <|> (_3705d20 x0 x1) <|> (_9546197 x0 x1)

def «nextResult(_,_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) : Option SortValSeq := (_3789647 x0 x1 x2) <|> (_3c90424 x0 x1 x2) <|> (_a873fe5 x0 x1 x2) <|> (_a95cde8 x0 x1 x2)

mutual
  def _4dfdd31 : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST, CUR => do
      let _Val0 <- «nextCurrent(_,_)_VERIFICATION-SYNTAX_Int_Int_Int» C CUR
      let _Val1 <- «scanCurrent(_,_)_VERIFICATION-SYNTAX_Int_IntSeq_Int» REST _Val0
      return _Val1
    | _, _ => none

  def «scanCurrent(_,_)_VERIFICATION-SYNTAX_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_4dfdd31 x0 x1) <|> (_f771d88 x0 x1)
end

mutual
  def «scanResult(_,_,_)_VERIFICATION-SYNTAX_ValSeq_IntSeq_Int_ValSeq» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortValSeq) : Option SortValSeq := (_543cd7c x0 x1 x2) <|> (_bf8e90a x0 x1 x2)

  def _bf8e90a : SortIntSeq → SortInt → SortValSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST, CUR, ACC => do
      let _Val0 <- «nextCurrent(_,_)_VERIFICATION-SYNTAX_Int_Int_Int» C CUR
      let _Val1 <- «nextResult(_,_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_Int_Int» ACC C CUR
      let _Val2 <- «scanResult(_,_,_)_VERIFICATION-SYNTAX_ValSeq_IntSeq_Int_ValSeq» REST _Val0 _Val1
      return _Val2
    | _, _, _ => none
end

def _3834c55 : SortIntSeq → Option SortValSeq
  | CS => do
    let _Val0 <- «scanCurrent(_,_)_VERIFICATION-SYNTAX_Int_IntSeq_Int» CS 0
    let _Val1 <- «_==Int_» _Val0 4
    let _Val2 <- «scanResult(_,_,_)_VERIFICATION-SYNTAX_ValSeq_IntSeq_Int_ValSeq» CS 0 SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val3 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Val2 (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) 4) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    guard _Val1
    return _Val3

def _59833e8 : SortIntSeq → Option SortValSeq
  | CS => do
    let _Val0 <- «scanCurrent(_,_)_VERIFICATION-SYNTAX_Int_IntSeq_Int» CS 0
    let _Val1 <- «_=/=Int_» _Val0 4
    let _Val2 <- «scanResult(_,_,_)_VERIFICATION-SYNTAX_ValSeq_IntSeq_Int_ValSeq» CS 0 SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    guard _Val1
    return _Val2

def «musicResult(_)_VERIFICATION-SYNTAX_ValSeq_IntSeq» (x0 : SortIntSeq) : Option SortValSeq := (_3834c55 x0) <|> (_59833e8 x0)