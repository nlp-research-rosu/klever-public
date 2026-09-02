import Klean31IsPrime.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

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

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _a2847c3 : SortInt → Option SortBool
  | N => do
    let _Val0 <- «_<Int_» N 2
    guard _Val0
    return false

def _d8ab886 : SortInt → SortInt → Option SortBool
  | _N, D => do
    let _Val0 <- «_<Int_» D 2
    guard _Val0
    return false

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def _4c61c83 : SortInt → SortInt → Option SortBool
  | N, D => do
    let _Val0 <- «_>=Int_» D 2
    let _Val1 <- «_>=Int_» D N
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return true

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def _5447b7e : SortInt → SortInt → Option SortBool
  | N, D => do
    let _Val0 <- «_>=Int_» D 2
    let _Val1 <- «_<Int_» D N
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N D
    let _Val4 <- «_==Int_» _Val3 0
    let _Val5 <- _andBool_ _Val2 _Val4
    guard _Val5
    return false

axiom _0d62631 : SortInt → SortInt → Option SortBool
axiom «primeScan(_,_)_VERIFICATION_Bool_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortBool

noncomputable def _f5a4ea6 : SortInt → Option SortBool
  | N => do
    let _Val0 <- «_>=Int_» N 2
    let _Val1 <- «primeScan(_,_)_VERIFICATION_Bool_Int_Int» N 2
    guard _Val0
    return _Val1

noncomputable def «primeResult(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := (_a2847c3 x0) <|> (_f5a4ea6 x0)