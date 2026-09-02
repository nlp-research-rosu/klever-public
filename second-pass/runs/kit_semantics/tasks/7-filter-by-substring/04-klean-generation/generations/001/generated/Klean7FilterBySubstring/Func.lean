import Klean7FilterBySubstring.Inj

def _1e06cee : SortVal → Option SortIntSeq
  | _Gen0 => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

def _eb4efe9 : SortVal → Option SortIntSeq
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» S) => some S
  | _ => none

def _fb7db52 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
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

def _fea1e7e : SortValSeq → SortIntSeq → SortValSeq → Option SortValSeq
  | A, _Gen0, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some A
  | _, _, _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def «strCodes(_)_VERIFICATION_IntSeq_Val» (x0 : SortVal) : Option SortIntSeq := (_eb4efe9 x0) <|> (_1e06cee x0)

def «filterAcc(_,_,_)_VERIFICATION_ValSeq_ValSeq_IntSeq_ValSeq» (x0 : SortValSeq) (x1 : SortIntSeq) (x2 : SortValSeq) : Option SortValSeq := _fea1e7e x0 x1 x2

mutual
  noncomputable def _5895ae4 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- «strCodes(_)_VERIFICATION_IntSeq_Val» V
      let _Val1 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0)) SortK.dotk)
      let _Val2 <- «allStrVS(_)_VERIFICATION_Bool_ValSeq» R
      let _Val3 <- _andBool_ _Val1 _Val2
      return _Val3
    | _ => none

  noncomputable def «allStrVS(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_5895ae4 x0) <|> (_fb7db52 x0)
end