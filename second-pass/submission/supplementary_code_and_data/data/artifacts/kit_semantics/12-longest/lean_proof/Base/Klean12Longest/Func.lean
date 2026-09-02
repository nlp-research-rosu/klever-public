import Klean12Longest.Inj

def _059c72f : SortValSeq → Option SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some SortVal.«noneV_MPY-CORE_Val»
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

def _6eec5a7 : SortValSeq → SortVal → Option SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», ACC => some ACC
  | _, _ => none

axiom projectString (x0 : SortVal) : Option SortStr

axiom seqLenString (x0 : SortStr) : Option SortInt

def _a3e4ffd : SortVal → Option SortBool
  | SortVal.inj_SortStr _Gen0 => some true
  | _ => none

def _d155d9d : SortVal → Option SortBool
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

def _fb4eb32 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def «isStringValue(_)_VERIFICATION-BASE_Bool_Val» (x0 : SortVal) : Option SortBool := (_a3e4ffd x0) <|> (_d155d9d x0)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def _3efeefa : SortValSeq → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0 => do
    let _Val0 <- «isStringValue(_)_VERIFICATION-BASE_Bool_Val» V
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return SortVal.«noneV_MPY-CORE_Val»
  | _ => none

mutual
  def «allStrings(_)_VERIFICATION-BASE_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_b5cc1c0 x0) <|> (_fb4eb32 x0)

  def _b5cc1c0 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «isStringValue(_)_VERIFICATION-BASE_Bool_Val» V
      let _Val1 <- «allStrings(_)_VERIFICATION-BASE_Bool_ValSeq» REST
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none
end

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

mutual
  noncomputable def «scanLongest(_,_)_VERIFICATION-BASE_Val_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortVal := (_6eec5a7 x0 x1) <|> (_b97871b x0 x1)

  noncomputable def _b97871b : SortValSeq → SortVal → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, ACC => do
      let _Val0 <- «isStringValue(_)_VERIFICATION-BASE_Bool_Val» V
      let _Val1 <- «isStringValue(_)_VERIFICATION-BASE_Bool_Val» ACC
      let _Val2 <- _andBool_ _Val0 _Val1
      let _Val3 <- projectString V
      let _Val4 <- seqLenString _Val3
      let _Val5 <- projectString ACC
      let _Val6 <- seqLenString _Val5
      let _Val7 <- «_>Int_» _Val4 _Val6
      let _Val8 <- _andBool_ _Val2 _Val7
      let _Val9 <- kite _Val8 V ACC
      let _Val10 <- «scanLongest(_,_)_VERIFICATION-BASE_Val_ValSeq_Val» REST _Val9
      return _Val10
    | _, _ => none
end

noncomputable def _0acef59 : SortValSeq → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
    let _Val0 <- «isStringValue(_)_VERIFICATION-BASE_Bool_Val» V
    let _Val1 <- «scanLongest(_,_)_VERIFICATION-BASE_Val_ValSeq_Val» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST) V
    guard _Val0
    return _Val1
  | _ => none

noncomputable def «longestValue(_)_VERIFICATION-BASE_Val_ValSeq» (x0 : SortValSeq) : Option SortVal := (_059c72f x0) <|> (_0acef59 x0) <|> (_3efeefa x0)