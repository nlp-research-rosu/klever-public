import Klean38DecodeCyclic.Inj

def _03c958c : SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

def _1d9e564 : SortIntSeq → Option SortIntSeq
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _ => none

def _554f065 : SortIntSeq → Option SortIntSeq
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») => some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))
  | _ => none

def _3eb7d8c : SortIntSeq → SortVal → Option SortVal
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», OLD => some OLD
  | _, _ => none

def _38132f6 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | ACC, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some ACC
  | _, _ => none

def _7930361 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | ACC, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen1 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») => some ACC
  | _, _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _d729f60 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | ACC, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some ACC
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

mutual
  def _2c7365c : SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen1 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen2 R)) => do
      let _Val0 <- «decodedTail(_)_VERIFICATION_IntSeq_IntSeq» R
      return _Val0
    | _ => none

  def «decodedTail(_)_VERIFICATION_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := (_03c958c x0) <|> (_1d9e564 x0) <|> (_2c7365c x0) <|> (_554f065 x0)
end

mutual
  def _375884d : SortIntSeq → SortVal → Option SortVal
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, _Gen0 => do
      let _Val0 <- «finalLoopChar(_,_)_VERIFICATION_Val_IntSeq_Val» R ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
      return _Val0
    | _, _ => none

  def «finalLoopChar(_,_)_VERIFICATION_Val_IntSeq_Val» (x0 : SortIntSeq) (x1 : SortVal) : Option SortVal := (_375884d x0 x1) <|> (_3eb7d8c x0 x1)
end

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

mutual
  def _932b0f2 : SortIntSeq → SortIntSeq → Option SortIntSeq
    | ACC, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R)) => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» ACC (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
      let _Val1 <- «decodedResult(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» _Val0 R
      return _Val1
    | _, _ => none

  def «decodedResult(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_38132f6 x0 x1) <|> (_7930361 x0 x1) <|> (_932b0f2 x0 x1) <|> (_d729f60 x0 x1)
end

def _51f0da5 : SortIntSeq → Option SortIntSeq
  | IS => do
    let _Val0 <- «decodedResult(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» IS
    let _Val1 <- «decodedTail(_)_VERIFICATION_IntSeq_IntSeq» IS
    let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» _Val0 _Val1
    return _Val2

def «decodeCodes(_)_VERIFICATION_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _51f0da5 x0