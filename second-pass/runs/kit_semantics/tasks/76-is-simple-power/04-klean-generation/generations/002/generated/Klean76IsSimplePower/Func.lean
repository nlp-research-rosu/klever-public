import Klean76IsSimplePower.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _90fdcb1 : SortInt → SortInt → Option SortBool
  | 1, _N => some true
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

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def _7fce7dc : SortInt → SortInt → Option SortBool
  | 0, N => do
    let _Val0 <- «_<=Int_» N (-2)
    let _Val1 <- «_>=Int_» N 2
    let _Val2 <- _orBool_ _Val0 _Val1
    guard _Val2
    return false
  | _, _ => none

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def _3d2395d : SortInt → SortInt → Option SortBool
  | X, N => do
    let _Val0 <- «_=/=Int_» X 0
    let _Val1 <- «_=/=Int_» X 1
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<=Int_» N (-2)
    let _Val4 <- «_>=Int_» N 2
    let _Val5 <- _orBool_ _Val3 _Val4
    let _Val6 <- _andBool_ _Val2 _Val5
    let _Val7 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» X N
    let _Val8 <- «_=/=Int_» _Val7 0
    let _Val9 <- _andBool_ _Val6 _Val8
    guard _Val9
    return false

def _9bc1db6 : SortInt → SortInt → Option SortBool
  | X, (-1) => do
    let _Val0 <- «_=/=Int_» X 1
    let _Val1 <- «_==Int_» X (-1)
    guard _Val0
    return _Val1
  | _, _ => none

def _b22da15 : SortInt → SortInt → Option SortBool
  | X, 1 => do
    let _Val0 <- «_=/=Int_» X 1
    guard _Val0
    return false
  | _, _ => none

def _d268469 : SortInt → SortInt → Option SortBool
  | X, 0 => do
    let _Val0 <- «_=/=Int_» X 1
    let _Val1 <- «_==Int_» X 0
    guard _Val0
    return _Val1
  | _, _ => none

axiom «simplePower(_,_)_VERIFICATION_Bool_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortBool
axiom _cd8f068 : SortInt → SortInt → Option SortBool