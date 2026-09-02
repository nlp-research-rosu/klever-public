import Klean163GenerateIntegers.Inj

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

def _d3d9190 : SortBool → SortInt → SortValSeq → Option SortValSeq
  | false, _Gen0, REST => some REST
  | _, _, _ => none

def _e47590f : SortBool → SortInt → SortValSeq → Option SortValSeq
  | true, D, REST => some (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) D) REST)
  | _, _, _ => none

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

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def «keepDigit(_,_,_)_VERIFICATION_ValSeq_Bool_Int_ValSeq» (x0 : SortBool) (x1 : SortInt) (x2 : SortValSeq) : Option SortValSeq := (_d3d9190 x0 x1 x2) <|> (_e47590f x0 x1 x2)

def _5a7ed7c : SortInt → SortInt → SortInt → Option SortBool
  | A, B, D => do
    let _Val0 <- «_<=Int_» A D
    let _Val1 <- «_<=Int_» D B
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<=Int_» B D
    let _Val4 <- «_<=Int_» D A
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    return _Val6

def «inClosedSpan(_,_,_)_VERIFICATION_Bool_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortBool := _5a7ed7c x0 x1 x2

def _1ed5921 : SortInt → SortInt → Option SortValSeq
  | A, B => do
    let _Val0 <- «inClosedSpan(_,_,_)_VERIFICATION_Bool_Int_Int_Int» A B 2
    let _Val1 <- «inClosedSpan(_,_,_)_VERIFICATION_Bool_Int_Int_Int» A B 4
    let _Val2 <- «inClosedSpan(_,_,_)_VERIFICATION_Bool_Int_Int_Int» A B 6
    let _Val3 <- «inClosedSpan(_,_,_)_VERIFICATION_Bool_Int_Int_Int» A B 8
    let _Val4 <- «keepDigit(_,_,_)_VERIFICATION_ValSeq_Bool_Int_ValSeq» _Val3 8 SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val5 <- «keepDigit(_,_,_)_VERIFICATION_ValSeq_Bool_Int_ValSeq» _Val2 6 _Val4
    let _Val6 <- «keepDigit(_,_,_)_VERIFICATION_ValSeq_Bool_Int_ValSeq» _Val1 4 _Val5
    let _Val7 <- «keepDigit(_,_,_)_VERIFICATION_ValSeq_Bool_Int_ValSeq» _Val0 2 _Val6
    return _Val7

def «expectedDigits(_,_)_VERIFICATION_ValSeq_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortValSeq := _1ed5921 x0 x1