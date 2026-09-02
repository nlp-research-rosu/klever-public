import Klean87GetRow.Inj

def _037082e : SortValSeq → SortValSeq → SortInt → SortInt → SortInt → Option SortValSeq
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, _Gen1, _Gen2 => some ACC
  | _, _, _, _, _ => none

def _812fb20 : SortInt → SortValSeq → Option SortInt
  | I, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some I
  | _, _ => none

def _5988be0 : SortValSeq → SortValSeq → SortInt → SortInt → Option SortValSeq
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, _Gen1 => some ACC
  | _, _, _, _ => none

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

def «scanAppend(_,_,_,_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_ValSeq_Int_Int_Int» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) : Option SortValSeq := _037082e x0 x1 x2 x3 x4

mutual
  def _4f69d86 : SortInt → SortValSeq → Option SortInt
    | I, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 VS => do
      let _Val0 <- «_+Int_» I 1
      let _Val1 <- «advanceIndex(_,_)_VERIFICATION-SYNTAX_Int_Int_ValSeq» _Val0 VS
      return _Val1
    | _, _ => none

  def «advanceIndex(_,_)_VERIFICATION-SYNTAX_Int_Int_ValSeq» (x0 : SortInt) (x1 : SortValSeq) : Option SortInt := (_4f69d86 x0 x1) <|> (_812fb20 x0 x1)
end

def «rowsAppend(_,_,_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_ValSeq_Int_Int» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortInt) (x3 : SortInt) : Option SortValSeq := _5988be0 x0 x1 x2 x3