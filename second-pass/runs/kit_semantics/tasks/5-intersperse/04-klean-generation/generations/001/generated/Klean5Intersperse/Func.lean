import Klean5Intersperse.Inj

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _5457a7a : SortValSeq → SortValSeq → SortVal → Option SortValSeq
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some ACC
  | _, _, _ => none

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
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

mutual
  def _1720fb7 : SortValSeq → SortValSeq → SortVal → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A AS, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» X REST, D => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A AS) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» D SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val1 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Val0 (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» X SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val2 <- «intersperseAcc(_,_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq_Val» _Val1 REST D
      return _Val2
    | _, _, _ => none

  def «intersperseAcc(_,_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq_Val» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortVal) : Option SortValSeq := (_1720fb7 x0 x1 x2) <|> (_5457a7a x0 x1 x2) <|> (_c4bedeb x0 x1 x2)

  def _c4bedeb : SortValSeq → SortValSeq → SortVal → Option SortValSeq
    | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» X REST, D => do
      let _Val0 <- «intersperseAcc(_,_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq_Val» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» X SortValSeq.«.ValSeq_MPY-CORE_ValSeq») REST D
      return _Val0
    | _, _, _ => none
end