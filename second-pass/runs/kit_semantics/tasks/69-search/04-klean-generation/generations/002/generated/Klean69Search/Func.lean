import Klean69Search.Inj

def _9fa7030 : SortVal → Option SortBool
  | SortVal.inj_SortInt _Gen0 => some true
  | _ => none

def _d8f051f : SortVal → Option SortBool
  | _Gen0 => some false

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1923b3a : SortValSeq → SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, A => some A
  | _, _, _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom projectIntTotal (x0 : SortVal) : Option SortInt

def _fc083e7 : SortInt → SortValSeq → Option SortInt
  | _Gen0, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _aa40960 : SortValSeq → Option SortBool
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

def «isIntVal(_)_VERIFICATION_Bool_Val» (x0 : SortVal) : Option SortBool := (_9fa7030 x0) <|> (_d8f051f x0)

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _c0c179d : SortInt → SortInt → SortInt → Option SortInt
  | A, X, N => do
    let _Val0 <- «_<Int_» N X
    guard _Val0
    return A

def _0ed2521 : SortVal → Option SortBool
  | V => do
    let _Val0 <- «isIntVal(_)_VERIFICATION_Bool_Val» V
    return _Val0

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def _52af9f2 : SortInt → SortInt → SortInt → Option SortInt
  | A, X, N => do
    let _Val0 <- «_>=Int_» N X
    let _Val1 <- «_<=Int_» X A
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return A

mutual
  noncomputable def _52c5d68 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- «isIntVal(_)_VERIFICATION_Bool_Val» V
      let _Val1 <- projectIntTotal V
      let _Val2 <- «_>Int_» _Val1 0
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «allPositive(_)_VERIFICATION_Bool_ValSeq» VS
      let _Val5 <- _andBool_ _Val3 _Val4
      return _Val5
    | _ => none

  noncomputable def «allPositive(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_52c5d68 x0) <|> (_aa40960 x0)
end

def _e95b289 : SortInt → SortInt → SortInt → Option SortInt
  | A, X, N => do
    let _Val0 <- «_>=Int_» N X
    let _Val1 <- «_>Int_» X A
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return X

def «definedProjectInt(_)_VERIFICATION_Bool_Val» (x0 : SortVal) : Option SortBool := _0ed2521 x0

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def «updateAnswer(_,_,_)_VERIFICATION_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_52af9f2 x0 x1 x2) <|> (_c0c179d x0 x1 x2) <|> (_e95b289 x0 x1 x2)

mutual
  noncomputable def _1b31985 : SortInt → SortValSeq → Option SortInt
    | X, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- «isIntVal(_)_VERIFICATION_Bool_Val» V
      let _Val1 <- projectIntTotal V
      let _Val2 <- «_==Int_» X _Val1
      let _Val3 <- kite _Val2 1 0
      let _Val4 <- «frequencyOf(_,_)_VERIFICATION_Int_Int_ValSeq» X VS
      let _Val5 <- «_+Int_» _Val3 _Val4
      guard _Val0
      return _Val5
    | _, _ => none

  noncomputable def «frequencyOf(_,_)_VERIFICATION_Int_Int_ValSeq» (x0 : SortInt) (x1 : SortValSeq) : Option SortInt := (_1b31985 x0 x1) <|> (_d3209dc x0 x1) <|> (_fc083e7 x0 x1)

  noncomputable def _d3209dc : SortInt → SortValSeq → Option SortInt
    | X, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- «isIntVal(_)_VERIFICATION_Bool_Val» V
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «frequencyOf(_,_)_VERIFICATION_Int_Int_ValSeq» X VS
      guard _Val1
      return _Val2
    | _, _ => none
end

mutual
  noncomputable def «searchSummary(_,_,_)_VERIFICATION_Int_ValSeq_ValSeq_Int» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortInt) : Option SortInt := (_1923b3a x0 x1 x2) <|> (_cb2c3e9 x0 x1 x2) <|> (_f72e694 x0 x1 x2)

  noncomputable def _cb2c3e9 : SortValSeq → SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, FULL, A => do
      let _Val0 <- «isIntVal(_)_VERIFICATION_Bool_Val» V
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «searchSummary(_,_,_)_VERIFICATION_Int_ValSeq_ValSeq_Int» REST FULL A
      guard _Val1
      return _Val2
    | _, _, _ => none

  noncomputable def _f72e694 : SortValSeq → SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, FULL, A => do
      let _Val0 <- «isIntVal(_)_VERIFICATION_Bool_Val» V
      let _Val1 <- projectIntTotal V
      let _Val2 <- projectIntTotal V
      let _Val3 <- «frequencyOf(_,_)_VERIFICATION_Int_Int_ValSeq» _Val2 FULL
      let _Val4 <- «updateAnswer(_,_,_)_VERIFICATION_Int_Int_Int_Int» A _Val1 _Val3
      let _Val5 <- «searchSummary(_,_,_)_VERIFICATION_Int_ValSeq_ValSeq_Int» REST FULL _Val4
      guard _Val0
      return _Val5
    | _, _, _ => none
end