import Klean133SumSquares.Inj

def _0f9305e : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

axiom «Float2Int(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

axiom «ceilFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

def _78d9b90 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

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

noncomputable def _3836331 : SortVal → Option SortInt
  | SortVal.inj_SortFloat F => do
    let _Val0 <- «ceilFloat(_)_FLOAT_Float_Float» F
    let _Val1 <- «Float2Int(_)_FLOAT_Int_Float» _Val0
    return _Val1
  | _ => none

noncomputable def ceilF (x0 : SortVal) : Option SortInt := (_0f9305e x0) <|> (_3836331 x0)

mutual
  noncomputable def «sumCeilSquares(_)_VERIFICATION_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_78d9b90 x0) <|> (_e6f36cd x0)

  noncomputable def _e6f36cd : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- ceilF V
      let _Val1 <- ceilF V
      let _Val2 <- «_*Int_» _Val0 _Val1
      let _Val3 <- «sumCeilSquares(_)_VERIFICATION_Int_ValSeq» VS
      let _Val4 <- «_+Int_» _Val2 _Val3
      return _Val4
    | _ => none
end