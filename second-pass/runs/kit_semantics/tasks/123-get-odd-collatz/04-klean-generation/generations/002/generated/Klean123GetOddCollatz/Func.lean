import Klean123GetOddCollatz.Inj

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _a5500da : SortValSeq → Option SortBool
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt _Gen0) SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _a604870 : SortValSeq → Option SortBool
  | _Gen0 => some false

def _cc21e6e : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some false
  | _ => none

def _05d9cc7 : SortValSeq → Option SortInt
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) _Gen0 => some I
  | _ => none

def _0855855 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

def _65d87dc : SortValSeq → Option SortInt
  | _Gen0 => some 0

def _9bb6898 : SortValSeq → Option SortInt
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some I
  | _ => none

def _7d95541 : SortValSeq → Option SortValSeq
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

def _9e71a5e : SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

def _8026998 : SortValSeq → Option SortInt
  | _Gen0 => some 0

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

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

mutual
  def _354ba9b : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R) => do
      let _Val0 <- «traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R)
      return _Val0
    | _ => none

  def «traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_0855855 x0) <|> (_354ba9b x0) <|> (_9bb6898 x0) <|> (_65d87dc x0)
end

def «traceFirstInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_05d9cc7 x0) <|> (_8026998 x0)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

mutual
  noncomputable def _379d958 : SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R) => do
      let _Val0 <- «oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R)
      return _Val0
    | _ => none

  noncomputable def _4cd3375 : SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R) => do
      let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
      let _Val1 <- «_==Int_» _Val0 0
      let _Val2 <- «oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R)
      guard _Val1
      return _Val2
    | _ => none

  noncomputable def _9482b52 : SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R) => do
      let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
      let _Val1 <- «_==Int_» _Val0 1
      let _Val2 <- «oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R)
      guard _Val1
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) I) _Val2)
    | _ => none

  noncomputable def «oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» (x0 : SortValSeq) : Option SortValSeq := (_4cd3375 x0) <|> (_7d95541 x0) <|> (_9482b52 x0) <|> (_9e71a5e x0) <|> (_379d958 x0)
end

noncomputable def _3d5bc16 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N 2
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N 2
    let _Val3 <- «_-Int_» N _Val2
    let _Val4 <- «_/Int_» _Val3 2
    guard _Val1
    return _Val4

noncomputable def _78d3437 : SortInt → Option SortValSeq
  | N => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N 2
    let _Val1 <- «_==Int_» _Val0 1
    guard _Val1
    return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) N) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)

noncomputable def _a91dd75 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N 2
    let _Val1 <- «_==Int_» _Val0 1
    let _Val2 <- «_*Int_» 3 N
    let _Val3 <- «_+Int_» _Val2 1
    guard _Val1
    return _Val3

noncomputable def _f2356f7 : SortInt → Option SortValSeq
  | N => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N 2
    let _Val1 <- «_==Int_» _Val0 0
    guard _Val1
    return SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

noncomputable def «collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : Option SortInt := (_3d5bc16 x0) <|> (_a91dd75 x0)

noncomputable def «maybeOdd(_)_VERIFICATION-SYNTAX_ValSeq_Int» (x0 : SortInt) : Option SortValSeq := (_78d3437 x0) <|> (_f2356f7 x0)

axiom _0077de7 : SortValSeq → Option SortBool
axiom «validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool