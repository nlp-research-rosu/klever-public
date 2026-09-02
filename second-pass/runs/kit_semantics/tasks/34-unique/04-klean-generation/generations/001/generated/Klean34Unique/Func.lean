import Klean34Unique.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _3d98329 : SortVal → SortValSeq → Option SortBool
  | _Gen0, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some false
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _c585a8f : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», ACC => some ACC
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

def _b5db171 : SortValSeq → SortVal → Option SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», X => some X
  | _, _ => none

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def «memberVS(_,_)_VERIFICATION-BASE_Bool_Val_ValSeq» (x0 : SortVal) (x1 : SortValSeq) : Option SortBool := _3d98329 x0 x1

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def «lastFromVS(_,_)_VERIFICATION-BASE_Val_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortVal := (_b5db171 x0 x1) <|> (_e506718 x0 x1)

  def _e506718 : SortValSeq → SortVal → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R, _Gen0 => do
      let _Val0 <- «lastFromVS(_,_)_VERIFICATION-BASE_Val_ValSeq_Val» R V
      return _Val0
    | _, _ => none
end

def _85a12aa : SortValSeq → SortVal → Option SortValSeq
  | ACC, V => do
    let _Val0 <- «memberVS(_,_)_VERIFICATION-BASE_Bool_Val_ValSeq» V ACC
    guard _Val0
    return ACC

def _a79bda4 : SortValSeq → SortVal → Option SortValSeq
  | ACC, V => do
    let _Val0 <- «memberVS(_,_)_VERIFICATION-BASE_Bool_Val_ValSeq» V ACC
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    guard _Val1
    return _Val2

def «appendUnique(_,_)_VERIFICATION-BASE_ValSeq_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortValSeq := (_85a12aa x0 x1) <|> (_a79bda4 x0 x1)

mutual
  def _3eccfd9 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R, ACC => do
      let _Val0 <- «appendUnique(_,_)_VERIFICATION-BASE_ValSeq_ValSeq_Val» ACC V
      let _Val1 <- «dedupFromVS(_,_)_VERIFICATION-BASE_ValSeq_ValSeq_ValSeq» R _Val0
      return _Val1
    | _, _ => none

  def «dedupFromVS(_,_)_VERIFICATION-BASE_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_3eccfd9 x0 x1) <|> (_c585a8f x0 x1)
end