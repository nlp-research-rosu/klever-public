import Klean130Tri.Inj

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

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

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _3b10696 : SortValSeq → SortInt → SortInt → Option SortValSeq
  | P, I, N => do
    let _Val0 <- «_>Int_» I N
    guard _Val0
    return P

def _64fb26d : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_<Int_» I 0
    guard _Val0
    return 0

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

noncomputable def _4e6915f : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
    let _Val2 <- «_==Int_» _Val1 0
    let _Val3 <- _andBool_ _Val0 _Val2
    let _Val4 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
    let _Val5 <- «_-Int_» I _Val4
    let _Val6 <- «_/Int_» _Val5 2
    let _Val7 <- «_+Int_» 1 _Val6
    guard _Val3
    return _Val7

noncomputable def _858862d : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
    let _Val2 <- «_==Int_» _Val1 1
    let _Val3 <- _andBool_ _Val0 _Val2
    let _Val4 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
    let _Val5 <- «_-Int_» I _Val4
    let _Val6 <- «_/Int_» _Val5 2
    let _Val7 <- «_+Int_» _Val6 1
    let _Val8 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
    let _Val9 <- «_-Int_» I _Val8
    let _Val10 <- «_/Int_» _Val9 2
    let _Val11 <- «_+Int_» _Val10 3
    let _Val12 <- «_*Int_» _Val7 _Val11
    guard _Val3
    return _Val12

noncomputable def «triValue(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : Option SortInt := (_4e6915f x0) <|> (_64fb26d x0) <|> (_858862d x0)

axiom «triComplete(_,_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) : Option SortValSeq
axiom _a505ffb : SortValSeq → SortInt → SortInt → Option SortValSeq

noncomputable def _2b2bf7b : SortInt → Option SortValSeq
  | N => do
    let _Val0 <- «triComplete(_,_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_Int_Int» SortValSeq.«.ValSeq_MPY-CORE_ValSeq» 0 N
    return _Val0

noncomputable def «triResult(_)_VERIFICATION-SYNTAX_ValSeq_Int» (x0 : SortInt) : Option SortValSeq := _2b2bf7b x0