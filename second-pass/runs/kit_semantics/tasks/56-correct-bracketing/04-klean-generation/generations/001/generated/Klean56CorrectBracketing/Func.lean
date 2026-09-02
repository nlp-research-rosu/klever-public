import Klean56CorrectBracketing.Inj

def _0aa9d03 : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _BAL => some true
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _8256842 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
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

def _f4cbe70 : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

mutual
  def «bracketChars(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_d1defd7 x0) <|> (_f4cbe70 x0)

  def _d1defd7 : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST => do
      let _Val0 <- «_==Int_» C 60
      let _Val1 <- «_==Int_» C 62
      let _Val2 <- _orBool_ _Val0 _Val1
      let _Val3 <- «bracketChars(_)_VERIFICATION_Bool_IntSeq» REST
      let _Val4 <- _andBool_ _Val2 _Val3
      return _Val4
    | _ => none
end

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

mutual
  def _59f0343 : SortIntSeq → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST, BAL => do
      let _Val0 <- «_==Int_» C 60
      let _Val1 <- «_+Int_» BAL 1
      let _Val2 <- «_>=Int_» _Val1 0
      let _Val3 <- «_+Int_» BAL 1
      let _Val4 <- «bracketPrefixOK(_,_)_VERIFICATION_Bool_IntSeq_Int» REST _Val3
      let _Val5 <- _andBool_ _Val2 _Val4
      let _Val6 <- «_-Int_» BAL 1
      let _Val7 <- «_>=Int_» _Val6 0
      let _Val8 <- «_-Int_» BAL 1
      let _Val9 <- «bracketPrefixOK(_,_)_VERIFICATION_Bool_IntSeq_Int» REST _Val8
      let _Val10 <- _andBool_ _Val7 _Val9
      let _Val11 <- kite _Val0 _Val5 _Val10
      return _Val11
    | _, _ => none

  def «bracketPrefixOK(_,_)_VERIFICATION_Bool_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortBool := (_0aa9d03 x0 x1) <|> (_59f0343 x0 x1)
end

mutual
  def _7e946c5 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST => do
      let _Val0 <- «_==Int_» C 60
      let _Val1 <- kite _Val0 1 (-1)
      let _Val2 <- «bracketDelta(_)_VERIFICATION_Int_IntSeq» REST
      let _Val3 <- «_+Int_» _Val1 _Val2
      return _Val3
    | _ => none

  def «bracketDelta(_)_VERIFICATION_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_7e946c5 x0) <|> (_8256842 x0)
end

def _1bf0298 : SortIntSeq → Option SortBool
  | CODES => do
    let _Val0 <- «bracketPrefixOK(_,_)_VERIFICATION_Bool_IntSeq_Int» CODES 0
    let _Val1 <- «bracketDelta(_)_VERIFICATION_Int_IntSeq» CODES
    let _Val2 <- «_==Int_» _Val1 0
    let _Val3 <- _andBool_ _Val0 _Val2
    return _Val3

def «bracketCorrect(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := _1bf0298 x0