import Klean79DecimalToBinary.Inj

noncomputable local instance : DecidableEq SortK :=
  Classical.typeDecidableEq SortK
noncomputable def «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool :=
  some (decide (x0 = x1))

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

def _af3a5b3 : SortInt → SortIntSeq → Option SortBool
  | _N, _CODES => some false

noncomputable def _1176214 : SortInt → SortIntSeq → SortIntSeq → Option SortBool
  | N, ACC, OUT => do
    let _Val0 <- «_==Int_» N 0
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) ACC) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) OUT) SortK.dotk)
    guard _Val0
    return _Val1

noncomputable def _c93b96a : SortInt → SortIntSeq → Option SortBool
  | N, TAIL => do
    let _Val0 <- «_==Int_» N 0
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) TAIL) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 100 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))) SortK.dotk)
    guard _Val0
    return _Val1

def _2ad2547 : SortInt → SortIntSeq → SortIntSeq → Option SortBool
  | N, _ACC, _OUT => do
    let _Val0 <- «_<Int_» N 0
    guard _Val0
    return false

def _8c4d643 : SortInt → SortIntSeq → Option SortBool
  | N, _TAIL => do
    let _Val0 <- «_<Int_» N 0
    guard _Val0
    return false

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

axiom _2a61685 : SortInt → SortIntSeq → SortIntSeq → Option SortBool
axiom «binRel(_,_,_)_VERIFICATION_Bool_Int_IntSeq_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) (x2 : SortIntSeq) : Option SortBool

noncomputable def _385b19a : SortInt → SortIntSeq → Option SortBool
  | N, TAIL => do
    let _Val0 <- «_>Int_» N 0
    let _Val1 <- «binRel(_,_,_)_VERIFICATION_Bool_Int_IntSeq_IntSeq» N (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 100 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)) TAIL
    guard _Val0
    return _Val1

noncomputable def «decimalTailRel(_,_)_VERIFICATION_Bool_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortBool := (_385b19a x0 x1) <|> (_8c4d643 x0 x1) <|> (_c93b96a x0 x1)

noncomputable def _796f9cb : SortInt → SortIntSeq → Option SortBool
  | N, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 100 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 TAIL) => do
    let _Val0 <- «decimalTailRel(_,_)_VERIFICATION_Bool_Int_IntSeq» N TAIL
    return _Val0
  | _, _ => none

noncomputable def «decimalResultRel(_,_)_VERIFICATION_Bool_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortBool := (_796f9cb x0 x1) <|> (_af3a5b3 x0 x1)