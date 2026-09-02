import Klean1SeparateParenGroups.Inj

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

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
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

def _bcbb9bf : SortIntSeq → SortInt → SortIntSeq → SortValSeq → Option SortValSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0, _Gen1, OUT => some OUT
  | _, _, _, _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _9f5289a : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 41 _Gen0, D => do
    let _Val0 <- «_<=Int_» D 0
    guard _Val0
    return false
  | _, _ => none

def _96f3c37 : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», D => do
    let _Val0 <- «_==Int_» D 0
    return _Val0
  | _, _ => none

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

mutual
  def «scanParenGroups(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_IntSeq_ValSeq» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortIntSeq) (x3 : SortValSeq) : Option SortValSeq := (_bcbb9bf x0 x1 x2 x3) <|> (_f97749e x0 x1 x2 x3)

  def _f97749e : SortIntSeq → SortInt → SortIntSeq → SortValSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST, D, CUR, OUT => do
      let _Val0 <- «_==Int_» C 32
      let _Val1 <- «scanParenGroups(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_IntSeq_ValSeq» REST D CUR OUT
      let _Val2 <- «_==Int_» C 40
      let _Val3 <- «_+Int_» D 1
      let _Val4 <- «_==Int_» _Val3 0
      let _Val5 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» CUR (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val6 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» OUT (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val5)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val7 <- «scanParenGroups(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_IntSeq_ValSeq» REST 0 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» _Val6
      let _Val8 <- «_+Int_» D 1
      let _Val9 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» CUR (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val10 <- «scanParenGroups(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_IntSeq_ValSeq» REST _Val8 _Val9 OUT
      let _Val11 <- kite _Val4 _Val7 _Val10
      let _Val12 <- «_-Int_» D 1
      let _Val13 <- «_==Int_» _Val12 0
      let _Val14 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» CUR (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val15 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» OUT (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val14)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val16 <- «scanParenGroups(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_IntSeq_ValSeq» REST 0 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» _Val15
      let _Val17 <- «_-Int_» D 1
      let _Val18 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» CUR (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val19 <- «scanParenGroups(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_IntSeq_ValSeq» REST _Val17 _Val18 OUT
      let _Val20 <- kite _Val13 _Val16 _Val19
      let _Val21 <- kite _Val2 _Val11 _Val20
      let _Val22 <- kite _Val0 _Val1 _Val21
      return _Val22
    | _, _, _, _ => none
end

def _c79f559 : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _Gen0, _Gen1 => do
    let _Val0 <- «_=/=Int_» C 32
    let _Val1 <- «_=/=Int_» C 40
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_=/=Int_» C 41
    let _Val4 <- _andBool_ _Val2 _Val3
    guard _Val4
    return false
  | _, _ => none

def _fe6fdc0 : SortIntSeq → Option SortValSeq
  | S => do
    let _Val0 <- «scanParenGroups(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_IntSeq_ValSeq» S 0 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    return _Val0

mutual
  def _13af0c8 : SortIntSeq → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 40 REST, D => do
      let _Val0 <- «_+Int_» D 1
      let _Val1 <- «validParenSuffix(_,_)_VERIFICATION_Bool_IntSeq_Int» REST _Val0
      return _Val1
    | _, _ => none

  def _28e7c0a : SortIntSeq → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 41 REST, D => do
      let _Val0 <- «_>Int_» D 0
      let _Val1 <- «_-Int_» D 1
      let _Val2 <- «validParenSuffix(_,_)_VERIFICATION_Bool_IntSeq_Int» REST _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  def «validParenSuffix(_,_)_VERIFICATION_Bool_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortBool := (_13af0c8 x0 x1) <|> (_28e7c0a x0 x1) <|> (_96f3c37 x0 x1) <|> (_9f5289a x0 x1) <|> (_c79f559 x0 x1) <|> (_e7ee7cb x0 x1)

  def _e7ee7cb : SortIntSeq → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 REST, D => do
      let _Val0 <- «validParenSuffix(_,_)_VERIFICATION_Bool_IntSeq_Int» REST D
      return _Val0
    | _, _ => none
end

def «separateParenGroupsSpec(_)_VERIFICATION_ValSeq_IntSeq» (x0 : SortIntSeq) : Option SortValSeq := _fe6fdc0 x0

def _239562b : SortIntSeq → Option SortBool
  | S => do
    let _Val0 <- «validParenSuffix(_,_)_VERIFICATION_Bool_IntSeq_Int» S 0
    return _Val0

def «validParenInput(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := _239562b x0