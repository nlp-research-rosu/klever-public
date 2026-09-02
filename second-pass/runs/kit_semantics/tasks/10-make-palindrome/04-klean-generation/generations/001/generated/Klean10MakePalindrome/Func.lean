import Klean10MakePalindrome.Inj

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

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

def _a87abe3 : SortIntSeq → SortIntSeq → SortIntSeq → SortIntSeq → SortIntSeq → SortBool → SortIntSeq → Option SortIntSeq
  | _Gen0, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen1, _Gen2, _Gen3, _Gen4, RESULT => some RESULT
  | _, _, _, _, _, _, _ => none

def _d8fc047 : SortIntSeq → SortIntSeq → SortIntSeq → SortIntSeq → SortIntSeq → SortBool → SortIntSeq → Option SortIntSeq
  | _Gen0, _Gen1, _Gen2, _Gen3, _Gen4, true, RESULT => some RESULT
  | _, _, _, _, _, _, _ => none

def _463fa2e : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», A => some A
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

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

mutual
  def «reverseAcc(_,_)_VERIFICATION-SYNTAX_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_463fa2e x0 x1) <|> (_df45d65 x0 x1)

  def _df45d65 : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, A => do
      let _Val0 <- «reverseAcc(_,_)_VERIFICATION-SYNTAX_IntSeq_IntSeq_IntSeq» R (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C A)
      return _Val0
    | _, _ => none
end

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

noncomputable def _a773065 : SortIntSeq → Option SortBool
  | S => do
    let _Val0 <- «reverseAcc(_,_)_VERIFICATION-SYNTAX_IntSeq_IntSeq_IntSeq» S SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) S) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val0) SortK.dotk)
    return _Val1

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def «palIS(_)_VERIFICATION-SYNTAX_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := _a773065 x0

mutual
  noncomputable def _302ef15 : SortIntSeq → SortIntSeq → SortIntSeq → SortIntSeq → SortIntSeq → SortBool → SortIntSeq → Option SortIntSeq
    | S, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, P, RP, REV, false, RESULT => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» P (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val1 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» _Val0 REV
      let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C RP)
      let _Val3 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) _Val1) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val2) SortK.dotk)
      let _Val4 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C RP)
      let _Val5 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» P (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val6 <- «searchResult(_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_IntSeq_IntSeq_IntSeq_IntSeq_IntSeq_IntSeq_Bool_IntSeq» S R _Val5 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C RP) REV false RESULT
      let _Val7 <- kite _Val3 _Val4 _Val6
      return _Val7
    | _, _, _, _, _, _, _ => none

  noncomputable def «searchResult(_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_IntSeq_IntSeq_IntSeq_IntSeq_IntSeq_IntSeq_Bool_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortIntSeq) (x3 : SortIntSeq) (x4 : SortIntSeq) (x5 : SortBool) (x6 : SortIntSeq) : Option SortIntSeq := (_302ef15 x0 x1 x2 x3 x4 x5 x6) <|> (_a87abe3 x0 x1 x2 x3 x4 x5 x6) <|> (_d8fc047 x0 x1 x2 x3 x4 x5 x6)
end

noncomputable def _74db4ad : SortIntSeq → Option SortIntSeq
  | S => do
    let _Val0 <- «palIS(_)_VERIFICATION-SYNTAX_Bool_IntSeq» S
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «reverseAcc(_,_)_VERIFICATION-SYNTAX_IntSeq_IntSeq_IntSeq» S SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val3 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S _Val2
    guard _Val1
    return _Val3

noncomputable def _de836de : SortIntSeq → Option SortIntSeq
  | S => do
    let _Val0 <- «palIS(_)_VERIFICATION-SYNTAX_Bool_IntSeq» S
    guard _Val0
    return S

noncomputable def «seedResult(_)_VERIFICATION-SYNTAX_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := (_74db4ad x0) <|> (_de836de x0)

noncomputable def _93d61d2 : SortIntSeq → Option SortIntSeq
  | S => do
    let _Val0 <- «reverseAcc(_,_)_VERIFICATION-SYNTAX_IntSeq_IntSeq_IntSeq» S SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val1 <- «palIS(_)_VERIFICATION-SYNTAX_Bool_IntSeq» S
    let _Val2 <- «seedResult(_)_VERIFICATION-SYNTAX_IntSeq_IntSeq» S
    let _Val3 <- «searchResult(_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_IntSeq_IntSeq_IntSeq_IntSeq_IntSeq_IntSeq_Bool_IntSeq» S S SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» _Val0 _Val1 _Val2
    return _Val3

noncomputable def «completePal(_)_VERIFICATION-SYNTAX_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _93d61d2 x0