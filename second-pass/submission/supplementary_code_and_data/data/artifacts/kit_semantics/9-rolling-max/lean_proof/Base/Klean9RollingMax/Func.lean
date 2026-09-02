import Klean9RollingMax.Inj

def _0bfca02 : SortValSeq → SortInt → SortValSeq → Option SortValSeq
  | A, _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen1 _Gen2 => some A
  | _, _, _ => none

def _0cbe282 : SortInt → SortValSeq → Option SortInt
  | M, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some M
  | _, _ => none

def _105572a : SortK → Option SortBool
  | K => some false

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _702a650 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _de45d75 : SortValSeq → SortInt → SortValSeq → Option SortValSeq
  | A, _Gen0, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some A
  | _, _, _ => none

def _56e0eca : SortInt → SortValSeq → Option SortInt
  | D, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 _Gen1 => some D
  | _, _ => none

def _5feb18e : SortInt → SortValSeq → Option SortInt
  | D, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some D
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

def _d822a7e : SortInt → SortValSeq → Option SortInt
  | M, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 _Gen1 => some M
  | _, _ => none

def _b405765 : SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

def _cc1bd42 : SortValSeq → Option SortValSeq
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 _Gen1 => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def _2bb550e : SortInt → SortInt → Option SortInt
  | M, I => do
    let _Val0 <- «_>Int_» I M
    guard _Val0
    return I

def _28958a6 : SortInt → SortInt → Option SortInt
  | M, I => do
    let _Val0 <- «_<=Int_» I M
    guard _Val0
    return M

mutual
  def _8da43e9 : SortInt → SortValSeq → Option SortInt
    | _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) R => do
      let _Val0 <- «lastOr(_,_)_VERIFICATION-SUMMARIES_Int_Int_ValSeq» I R
      return _Val0
    | _, _ => none

  def «lastOr(_,_)_VERIFICATION-SUMMARIES_Int_Int_ValSeq» (x0 : SortInt) (x1 : SortValSeq) : Option SortInt := (_5feb18e x0 x1) <|> (_8da43e9 x0 x1) <|> (_56e0eca x0 x1)
end

mutual
  def _0ebf81a : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allInts(_)_VERIFICATION-SUMMARIES_Bool_ValSeq» R
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allInts(_)_VERIFICATION-SUMMARIES_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_0ebf81a x0) <|> (_702a650 x0)
end

def «stepMax(_,_)_VERIFICATION-SUMMARIES_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_28958a6 x0 x1) <|> (_2bb550e x0 x1)

mutual
  def _88c16dd : SortValSeq → SortInt → SortValSeq → Option SortValSeq
    | A, M, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) R => do
      let _Val0 <- «stepMax(_,_)_VERIFICATION-SUMMARIES_Int_Int_Int» M I
      let _Val1 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) _Val0) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val2 <- «stepMax(_,_)_VERIFICATION-SUMMARIES_Int_Int_Int» M I
      let _Val3 <- «rollAcc(_,_,_)_VERIFICATION-SUMMARIES_ValSeq_ValSeq_Int_ValSeq» _Val1 _Val2 R
      return _Val3
    | _, _, _ => none

  def «rollAcc(_,_,_)_VERIFICATION-SUMMARIES_ValSeq_ValSeq_Int_ValSeq» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortValSeq) : Option SortValSeq := (_88c16dd x0 x1 x2) <|> (_de45d75 x0 x1 x2) <|> (_0bfca02 x0 x1 x2)
end

mutual
  def «foldMax(_,_)_VERIFICATION-SUMMARIES_Int_Int_ValSeq» (x0 : SortInt) (x1 : SortValSeq) : Option SortInt := (_0cbe282 x0 x1) <|> (_bc7311b x0 x1) <|> (_d822a7e x0 x1)

  def _bc7311b : SortInt → SortValSeq → Option SortInt
    | M, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) R => do
      let _Val0 <- «stepMax(_,_)_VERIFICATION-SUMMARIES_Int_Int_Int» M I
      let _Val1 <- «foldMax(_,_)_VERIFICATION-SUMMARIES_Int_Int_ValSeq» _Val0 R
      return _Val1
    | _, _ => none
end

def _14de73a : SortValSeq → Option SortValSeq
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt H) T => do
    let _Val0 <- «rollAcc(_,_,_)_VERIFICATION-SUMMARIES_ValSeq_ValSeq_Int_ValSeq» SortValSeq.«.ValSeq_MPY-CORE_ValSeq» H (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) H) T)
    return _Val0
  | _ => none

def «rollingMax(_)_VERIFICATION-SUMMARIES_ValSeq_ValSeq» (x0 : SortValSeq) : Option SortValSeq := (_14de73a x0) <|> (_b405765 x0) <|> (_cc1bd42 x0)