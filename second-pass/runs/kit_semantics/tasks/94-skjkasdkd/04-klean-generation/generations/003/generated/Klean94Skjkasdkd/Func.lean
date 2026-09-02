import Klean94Skjkasdkd.Inj

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

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom projectIntTotal (x0 : SortVal) : Option SortInt

def _f242d72 : SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», M => some M
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

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _8ad777b : SortInt → SortInt → Option SortBool
  | _N, D => do
    let _Val0 <- «_<Int_» D 2
    guard _Val0
    return false

def _8aff840 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return 0

def _2108796 : SortInt → SortInt → Option SortBool
  | N, D => do
    let _Val0 <- «_>=Int_» D 2
    let _Val1 <- «_>=Int_» D N
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return true

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

def _21add3b : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

def «digitSum(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _8aff840 x0

def «primeTail(_,_)_VERIFICATION_Bool_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortBool := (_2108796 x0 x1) <|> (_8ad777b x0 x1)

def «definedProjectInt(_)_VERIFICATION_Bool_Val» (x0 : SortVal) : Option SortBool := _21add3b x0

def _db5e55e : SortInt → Option SortBool
  | N => do
    let _Val0 <- «_>=Int_» N 2
    let _Val1 <- «primeTail(_,_)_VERIFICATION_Bool_Int_Int» N 2
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

def «isPrime(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _db5e55e x0

def _6eda1da : SortInt → SortInt → Option SortInt
  | M, X => do
    let _Val0 <- «_>Int_» X M
    let _Val1 <- «isPrime(_)_VERIFICATION_Bool_Int» X
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return X

def _71f0fe4 : SortInt → SortInt → Option SortInt
  | M, X => do
    let _Val0 <- «_>Int_» X M
    let _Val1 <- «isPrime(_)_VERIFICATION_Bool_Int» X
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- notBool_ _Val2
    guard _Val3
    return M

def «selectPrime(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_6eda1da x0 x1) <|> (_71f0fe4 x0 x1)

mutual
  noncomputable def _62a1354 : SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R, M => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «largestPrime(_,_)_VERIFICATION_Int_ValSeq_Int» R M
      guard _Val1
      return _Val2
    | _, _ => none

  noncomputable def _963ca20 : SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R, M => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- projectIntTotal V
      let _Val2 <- «selectPrime(_,_)_VERIFICATION_Int_Int_Int» M _Val1
      let _Val3 <- «largestPrime(_,_)_VERIFICATION_Int_ValSeq_Int» R _Val2
      guard _Val0
      return _Val3
    | _, _ => none

  noncomputable def «largestPrime(_,_)_VERIFICATION_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := (_62a1354 x0 x1) <|> (_963ca20 x0 x1) <|> (_f242d72 x0 x1)
end