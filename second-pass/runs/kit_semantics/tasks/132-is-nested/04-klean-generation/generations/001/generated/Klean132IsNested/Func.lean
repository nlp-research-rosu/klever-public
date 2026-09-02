import Klean132IsNested.Inj

def _17717b5 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», S => some S
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

def _03eb52b : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
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

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _cbb099a : SortInt → SortInt → Option SortInt
  | _C, S => do
    let _Val0 <- «_>=Int_» S 4
    guard _Val0
    return S

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def _30be423 : SortInt → SortInt → Option SortInt
  | C, S => do
    let _Val0 <- «_>=Int_» S 2
    let _Val1 <- «_<Int_» S 4
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_==Int_» C 93
    let _Val4 <- _andBool_ _Val2 _Val3
    let _Val5 <- «_+Int_» S 1
    guard _Val4
    return _Val5

def _cf101ad : SortInt → SortInt → Option SortInt
  | C, S => do
    let _Val0 <- «_<Int_» S 2
    let _Val1 <- «_==Int_» C 91
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_+Int_» S 1
    guard _Val2
    return _Val3

mutual
  def _800e7ad : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C CS => do
      let _Val0 <- «_==Int_» C 91
      let _Val1 <- «_==Int_» C 93
      let _Val2 <- _orBool_ _Val0 _Val1
      let _Val3 <- «bracketInput(_)_VERIFICATION_Bool_IntSeq» CS
      let _Val4 <- _andBool_ _Val2 _Val3
      return _Val4
    | _ => none

  def «bracketInput(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_03eb52b x0) <|> (_800e7ad x0)
end

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

def _32d0f13 : SortInt → SortInt → Option SortInt
  | C, S => do
    let _Val0 <- «_<Int_» S 2
    let _Val1 <- «_=/=Int_» C 91
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return S

def _e52de95 : SortInt → SortInt → Option SortInt
  | C, S => do
    let _Val0 <- «_>=Int_» S 2
    let _Val1 <- «_<Int_» S 4
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_=/=Int_» C 93
    let _Val4 <- _andBool_ _Val2 _Val3
    guard _Val4
    return S

def «nestedStep(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_30be423 x0 x1) <|> (_32d0f13 x0 x1) <|> (_cbb099a x0 x1) <|> (_cf101ad x0 x1) <|> (_e52de95 x0 x1)

mutual
  def _9c3d425 : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C CS, S => do
      let _Val0 <- «nestedStep(_,_)_VERIFICATION_Int_Int_Int» C S
      let _Val1 <- «nestedScan(_,_)_VERIFICATION_Int_IntSeq_Int» CS _Val0
      return _Val1
    | _, _ => none

  def «nestedScan(_,_)_VERIFICATION_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_17717b5 x0 x1) <|> (_9c3d425 x0 x1)
end

def _026c653 : SortIntSeq → Option SortBool
  | CS => do
    let _Val0 <- «nestedScan(_,_)_VERIFICATION_Int_IntSeq_Int» CS 0
    let _Val1 <- «_==Int_» _Val0 4
    return _Val1

def «nestedResult(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := _026c653 x0