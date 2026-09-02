import Klean84Solve.Inj

def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _fb352e3 : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

def _3ab5d6e : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

axiom «_^Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _8712d6f : SortIntSeq → Option SortBool
  | _Gen0 => some false

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

def _ec410ef : SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

mutual
  def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

mutual
  def _1cdf356 : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «_==Int_» C 48
      let _Val1 <- «_==Int_» C 49
      let _Val2 <- _orBool_ _Val0 _Val1
      let _Val3 <- «allBinDigits(_)_VERIFICATION_Bool_IntSeq» R
      let _Val4 <- _andBool_ _Val2 _Val3
      return _Val4
    | _ => none

  def «allBinDigits(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_1cdf356 x0) <|> (_fb352e3 x0)
end

def _2185f95 : SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
  | D0, D1, D2, D3, D4 => do
    let _Val0 <- «_<=Int_» 0 D0
    let _Val1 <- «_<Int_» D0 10
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<=Int_» 0 D1
    let _Val4 <- _andBool_ _Val2 _Val3
    let _Val5 <- «_<Int_» D1 10
    let _Val6 <- _andBool_ _Val4 _Val5
    let _Val7 <- «_<=Int_» 0 D2
    let _Val8 <- _andBool_ _Val6 _Val7
    let _Val9 <- «_<Int_» D2 10
    let _Val10 <- _andBool_ _Val8 _Val9
    let _Val11 <- «_<=Int_» 0 D3
    let _Val12 <- _andBool_ _Val10 _Val11
    let _Val13 <- «_<Int_» D3 10
    let _Val14 <- _andBool_ _Val12 _Val13
    let _Val15 <- «_<=Int_» 0 D4
    let _Val16 <- _andBool_ _Val14 _Val15
    let _Val17 <- «_<=Int_» D4 1
    let _Val18 <- _andBool_ _Val16 _Val17
    let _Val19 <- «_==Int_» D4 0
    let _Val20 <- «_==Int_» D4 1
    let _Val21 <- «_==Int_» D0 0
    let _Val22 <- _andBool_ _Val20 _Val21
    let _Val23 <- «_==Int_» D1 0
    let _Val24 <- _andBool_ _Val22 _Val23
    let _Val25 <- «_==Int_» D2 0
    let _Val26 <- _andBool_ _Val24 _Val25
    let _Val27 <- «_==Int_» D3 0
    let _Val28 <- _andBool_ _Val26 _Val27
    let _Val29 <- _orBool_ _Val19 _Val28
    let _Val30 <- _andBool_ _Val18 _Val29
    return _Val30

mutual
  noncomputable def _4c5f0a7 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «_-Int_» C 48
      let _Val1 <- «isLen(_)_MPY-CORE_Int_IntSeq» R
      let _Val2 <- «_^Int_» 2 _Val1
      let _Val3 <- «_*Int_» _Val0 _Val2
      let _Val4 <- «decodeBin(_)_VERIFICATION_Int_IntSeq» R
      let _Val5 <- «_+Int_» _Val3 _Val4
      return _Val5
    | _ => none

  noncomputable def «decodeBin(_)_VERIFICATION_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_3ab5d6e x0) <|> (_4c5f0a7 x0)
end

def _159105c : SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 49 R => do
    let _Val0 <- «allBinDigits(_)_VERIFICATION_Bool_IntSeq» R
    return _Val0
  | _ => none

def «digitDomain(_,_,_,_,_)_VERIFICATION_Bool_Int_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) : Option SortBool := _2185f95 x0 x1 x2 x3 x4

def «canonicalBin(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_159105c x0) <|> (_ec410ef x0) <|> (_8712d6f x0)