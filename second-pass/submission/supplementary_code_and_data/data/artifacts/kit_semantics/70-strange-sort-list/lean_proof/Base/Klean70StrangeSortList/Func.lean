import Klean70StrangeSortList.Inj

def _105572a : SortK → Option SortBool
  | K => some false

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _d0a8392 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _a66427b : SortValSeq → SortInt → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0, 0 => some V
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

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _1149ba1 : SortValSeq → SortValSeq → SortInt → SortInt → Option SortValSeq
  | A, _Gen0, L, R => do
    let _Val0 <- «_>Int_» L R
    guard _Val0
    return A

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

mutual
  def _86fc1c7 : SortValSeq → SortInt → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S, I => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» S _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  def «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortVal := (_86fc1c7 x0 x1) <|> (_a66427b x0 x1)
end

mutual
  def _01539d8 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allInts(_)_VERIFICATION_Bool_ValSeq» R
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allInts(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_01539d8 x0) <|> (_d0a8392 x0)
end

def _1410e05 : SortValSeq → SortValSeq → SortInt → SortInt → Option SortValSeq
  | A, S, L, R => do
    let _Val0 <- «_==Int_» L R
    let _Val1 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» S L
    let _Val2 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Val1 SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    guard _Val0
    return _Val2

axiom _51875bc : SortValSeq → SortValSeq → SortInt → SortInt → Option SortValSeq
axiom «strangeAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq_Int_Int» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortInt) (x3 : SortInt) : Option SortValSeq