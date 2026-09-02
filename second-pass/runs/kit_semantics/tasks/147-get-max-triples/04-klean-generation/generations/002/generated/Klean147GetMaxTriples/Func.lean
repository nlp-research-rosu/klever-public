import Klean147GetMaxTriples.Inj

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

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

noncomputable def _1a3a690 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_+Int_» N 1
    let _Val1 <- «_+Int_» N 1
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val1 3
    let _Val3 <- «_-Int_» _Val0 _Val2
    let _Val4 <- «_/Int_» _Val3 3
    return _Val4

noncomputable def _c3e336f : SortInt → Option SortInt
  | X => do
    let _Val0 <- «_-Int_» X 1
    let _Val1 <- «_*Int_» X _Val0
    let _Val2 <- «_-Int_» X 2
    let _Val3 <- «_*Int_» _Val1 _Val2
    let _Val4 <- «_-Int_» X 1
    let _Val5 <- «_*Int_» X _Val4
    let _Val6 <- «_-Int_» X 2
    let _Val7 <- «_*Int_» _Val5 _Val6
    let _Val8 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val7 6
    let _Val9 <- «_-Int_» _Val3 _Val8
    let _Val10 <- «_/Int_» _Val9 6
    return _Val10

noncomputable def «zeroResidueCount(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : Option SortInt := _1a3a690 x0

noncomputable def «chooseThree(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : Option SortInt := _c3e336f x0

noncomputable def _2918c22 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «zeroResidueCount(_)_VERIFICATION-SYNTAX_Int_Int» N
    let _Val1 <- «chooseThree(_)_VERIFICATION-SYNTAX_Int_Int» _Val0
    let _Val2 <- «zeroResidueCount(_)_VERIFICATION-SYNTAX_Int_Int» N
    let _Val3 <- «_-Int_» N _Val2
    let _Val4 <- «chooseThree(_)_VERIFICATION-SYNTAX_Int_Int» _Val3
    let _Val5 <- «_+Int_» _Val1 _Val4
    return _Val5

noncomputable def «expectedTriples(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : Option SortInt := _2918c22 x0