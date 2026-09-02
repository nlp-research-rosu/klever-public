import Klean155EvenOddCount.Inj

noncomputable def _554b9cb : SortInt → Option SortInt
  | 0 => some 0
  | _ => none

noncomputable def _490784b : SortInt → Option SortInt
  | 0 => some 0
  | _ => none

noncomputable def _a6870b3 : SortInt → Option SortInt
  | 0 => some 0
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

noncomputable def _d88d720 : SortInt → Option SortInt
  | 0 => some 1
  | _ => none

axiom «oddPos(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt
axiom _ea71ef8 : SortInt → Option SortInt

axiom _538d54c : SortInt → Option SortInt
axiom «evenPos(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt

noncomputable def _16cf574 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_>Int_» N 0
    let _Val1 <- «oddPos(_)_VERIFICATION_Int_Int» N
    guard _Val0
    return _Val1

noncomputable def _d0fd0a3 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<Int_» N 0
    let _Val1 <- «_-Int_» 0 N
    let _Val2 <- «oddPos(_)_VERIFICATION_Int_Int» _Val1
    guard _Val0
    return _Val2

noncomputable def _4fd9cd7 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<Int_» N 0
    let _Val1 <- «_-Int_» 0 N
    let _Val2 <- «evenPos(_)_VERIFICATION_Int_Int» _Val1
    guard _Val0
    return _Val2

noncomputable def _f3bc4fc : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_>Int_» N 0
    let _Val1 <- «evenPos(_)_VERIFICATION_Int_Int» N
    guard _Val0
    return _Val1

noncomputable def «decOdd(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_16cf574 x0) <|> (_490784b x0) <|> (_d0fd0a3 x0)

noncomputable def «decEven(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_4fd9cd7 x0) <|> (_d88d720 x0) <|> (_f3bc4fc x0)