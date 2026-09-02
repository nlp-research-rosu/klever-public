import Klean61CorrectBracketing.Inj

def _03eb52b : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

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

def _0901651 : SortInt → SortBool → Option SortBool
  | B, _Gen0 => do
    let _Val0 <- «_<Int_» B 0
    guard _Val0
    return false

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _b9d2417 : SortInt → SortBool → Option SortBool
  | B, V => do
    let _Val0 <- «_>=Int_» B 0
    guard _Val0
    return V

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def _ab46bfb : SortIntSeq → SortInt → SortBool → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», B, V => do
    let _Val0 <- «_==Int_» B 0
    let _Val1 <- _andBool_ V _Val0
    return _Val1
  | _, _, _ => none

def «keepValid(_,_)_VERIFICATION_Bool_Int_Bool» (x0 : SortInt) (x1 : SortBool) : Option SortBool := (_0901651 x0 x1) <|> (_b9d2417 x0 x1)

mutual
  def «bracketInput(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_03eb52b x0) <|> (_b83d0b3 x0)

  def _b83d0b3 : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST => do
      let _Val0 <- «_==Int_» C 40
      let _Val1 <- «_==Int_» C 41
      let _Val2 <- _orBool_ _Val0 _Val1
      let _Val3 <- «bracketInput(_)_VERIFICATION_Bool_IntSeq» REST
      let _Val4 <- _andBool_ _Val2 _Val3
      return _Val4
    | _ => none
end

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

mutual
  def _32fa294 : SortIntSeq → SortInt → SortBool → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST, B, V => do
      let _Val0 <- «_==Int_» C 40
      let _Val1 <- «_+Int_» B 1
      let _Val2 <- «_-Int_» B 1
      let _Val3 <- kite _Val0 _Val1 _Val2
      let _Val4 <- «_==Int_» C 40
      let _Val5 <- «_+Int_» B 1
      let _Val6 <- «_-Int_» B 1
      let _Val7 <- kite _Val4 _Val5 _Val6
      let _Val8 <- «keepValid(_,_)_VERIFICATION_Bool_Int_Bool» _Val7 V
      let _Val9 <- «scanBrackets(_,_,_)_VERIFICATION_Bool_IntSeq_Int_Bool» REST _Val3 _Val8
      return _Val9
    | _, _, _ => none

  def «scanBrackets(_,_,_)_VERIFICATION_Bool_IntSeq_Int_Bool» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortBool) : Option SortBool := (_32fa294 x0 x1 x2) <|> (_ab46bfb x0 x1 x2)
end