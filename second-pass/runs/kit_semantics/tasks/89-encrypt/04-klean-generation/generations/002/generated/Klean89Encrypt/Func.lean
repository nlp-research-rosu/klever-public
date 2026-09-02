import Klean89Encrypt.Inj

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _3eb7d8c : SortIntSeq → SortVal → Option SortVal
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», V => some V
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
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

def _f49d717 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | A, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some A
  | _, _ => none

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

mutual
  def _375884d : SortIntSeq → SortVal → Option SortVal
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, _V => do
      let _Val0 <- «finalLoopChar(_,_)_VERIFICATION_Val_IntSeq_Val» R ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
      return _Val0
    | _, _ => none

  def «finalLoopChar(_,_)_VERIFICATION_Val_IntSeq_Val» (x0 : SortIntSeq) (x1 : SortVal) : Option SortVal := (_375884d x0 x1) <|> (_3eb7d8c x0 x1)
end

def _562564b : SortInt → Option SortIntSeq
  | C => do
    let _Val0 <- «_>Int_» C 122
    guard _Val0
    return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

def _e791f87 : SortInt → Option SortIntSeq
  | C => do
    let _Val0 <- «_<Int_» C 97
    guard _Val0
    return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

noncomputable def _006d001 : SortInt → Option SortInt
  | C => do
    let _Val0 <- «_-Int_» C 97
    let _Val1 <- «_+Int_» _Val0 4
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val1 26
    let _Val3 <- «_+Int_» _Val2 97
    return _Val3

noncomputable def «rot4Code(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _006d001 x0

noncomputable def _ee688aa : SortInt → Option SortIntSeq
  | C => do
    let _Val0 <- «_<=Int_» 97 C
    let _Val1 <- «_<=Int_» C 122
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «rot4Code(_)_VERIFICATION_Int_Int» C
    guard _Val2
    return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Val3 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)

noncomputable def «encryptedChar(_)_VERIFICATION_IntSeq_Int» (x0 : SortInt) : Option SortIntSeq := (_562564b x0) <|> (_e791f87 x0) <|> (_ee688aa x0)

mutual
  noncomputable def «encryptFold(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_bc1e734 x0 x1) <|> (_f49d717 x0 x1)

  noncomputable def _bc1e734 : SortIntSeq → SortIntSeq → Option SortIntSeq
    | A, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «encryptedChar(_)_VERIFICATION_IntSeq_Int» C
      let _Val1 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» A _Val0
      let _Val2 <- «encryptFold(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» _Val1 R
      return _Val2
    | _, _ => none
end

noncomputable def _fca1199 : SortIntSeq → Option SortIntSeq
  | S => do
    let _Val0 <- «encryptFold(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» S
    return _Val0

noncomputable def «encryptResult(_)_VERIFICATION_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _fca1199 x0