import Klean20FindClosestElements.Inj

axiom «absFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

axiom «_<Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1bb203a : SortValSeq → SortVal → Option SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», OLD => some OLD
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _86a8148 : SortVal → Option SortFloat
  | SortVal.inj_SortIterable (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt _Gen0) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortFloat F) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))) => some F
  | _ => none

def _9c4c9c8 : SortVal → Option SortInt
  | SortVal.inj_SortIterable (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortFloat _Gen0) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))) => some I
  | _ => none

axiom «_-Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

def _f08cce2 : SortVal → SortValSeq → SortFloat → SortFloat → Option SortFloat
  | _ITEM1, SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _A, B => some B
  | _, _, _, _ => none

def _919f7a3 : SortValSeq → SortValSeq → SortFloat → SortFloat → Option SortFloat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ALL, _A, B => some B
  | _, _, _, _ => none

def _c4cee72 : SortVal → SortValSeq → SortFloat → SortFloat → Option SortFloat
  | _ITEM1, SortValSeq.«.ValSeq_MPY-CORE_ValSeq», A, _B => some A
  | _, _, _, _ => none

def _8789ec4 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

def _e25fa3e : SortVal → Option SortFloat
  | SortVal.inj_SortFloat F => some F
  | _ => none

def _bb8678e : SortValSeq → SortValSeq → SortFloat → SortFloat → Option SortFloat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ALL, A, _B => some A
  | _, _, _, _ => none

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

def _fb25714 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

noncomputable def _00d63fc : SortFloat → Option SortFloat
  | F => do
    let _Val0 <- «absFloat(_)_FLOAT_Float_Float» F
    return _Val0

noncomputable def _5667141 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_<Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

mutual
  def _2d3e7af : SortValSeq → SortVal → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, _OLD => do
      let _Val0 <- «lastItem(_,_)_VERIFICATION-BASE_Val_ValSeq_Val» REST V
      return _Val0
    | _, _ => none

  def «lastItem(_,_)_VERIFICATION-BASE_Val_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortVal := (_1bb203a x0 x1) <|> (_2d3e7af x0 x1)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def «itemFloat(_)_VERIFICATION-BASE_Float_Val» (x0 : SortVal) : Option SortFloat := _86a8148 x0

def «itemIndex(_)_VERIFICATION-BASE_Int_Val» (x0 : SortVal) : Option SortInt := _9c4c9c8 x0

noncomputable def _fabe8f9 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_-Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

def «floatProjection(_)_VERIFICATION-BASE_Float_Val» (x0 : SortVal) : Option SortFloat := _e25fa3e x0

noncomputable def absF (x0 : SortFloat) : Option SortFloat := _00d63fc x0

noncomputable def floatLt (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _5667141 x0 x1

mutual
  noncomputable def «allFloatItems(_)_VERIFICATION-BASE_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_ef4938d x0) <|> (_fb25714 x0)

  noncomputable def _ef4938d : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «itemIndex(_)_VERIFICATION-BASE_Int_Val» V
      let _Val1 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» V
      let _Val2 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortIterable SortKItem) (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) _Val0) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortFloat SortVal) _Val1) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)))) SortK.dotk)
      let _Val3 <- «allFloatItems(_)_VERIFICATION-BASE_Bool_ValSeq» REST
      let _Val4 <- _andBool_ _Val2 _Val3
      return _Val4
    | _ => none
end

noncomputable def subF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _fabe8f9 x0 x1

mutual
  noncomputable def _8213c9d : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «floatProjection(_)_VERIFICATION-BASE_Float_Val» V
      let _Val1 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortFloat SortKItem) _Val0) SortK.dotk)
      let _Val2 <- «allFloatVS(_)_VERIFICATION-BASE_Bool_ValSeq» REST
      let _Val3 <- _andBool_ _Val1 _Val2
      return _Val3
    | _ => none

  noncomputable def «allFloatVS(_)_VERIFICATION-BASE_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_8213c9d x0) <|> (_8789ec4 x0)
end

noncomputable def _0e6f622 : SortFloat → SortFloat → Option SortFloat
  | X, Y => do
    let _Val0 <- floatLt X Y
    guard _Val0
    return X

noncomputable def _1b33d3a : SortFloat → SortFloat → Option SortFloat
  | X, Y => do
    let _Val0 <- floatLt X Y
    guard _Val0
    return Y

noncomputable def _32c5755 : SortFloat → SortFloat → Option SortFloat
  | X, Y => do
    let _Val0 <- floatLt X Y
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return X

noncomputable def _b06eae6 : SortFloat → SortFloat → Option SortFloat
  | X, Y => do
    let _Val0 <- floatLt X Y
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return Y

noncomputable def _4db727f : SortVal → SortVal → SortFloat → SortFloat → Option SortBool
  | ITEM1, ITEM2, A, B => do
    let _Val0 <- «itemIndex(_)_VERIFICATION-BASE_Int_Val» ITEM1
    let _Val1 <- «itemIndex(_)_VERIFICATION-BASE_Int_Val» ITEM2
    let _Val2 <- «_<Int_» _Val0 _Val1
    let _Val3 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM2
    let _Val4 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM1
    let _Val5 <- subF _Val3 _Val4
    let _Val6 <- absF _Val5
    let _Val7 <- subF B A
    let _Val8 <- absF _Val7
    let _Val9 <- floatLt _Val6 _Val8
    let _Val10 <- _andBool_ _Val2 _Val9
    return _Val10

noncomputable def «orderedSecond(_,_)_VERIFICATION-BASE_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := (_1b33d3a x0 x1) <|> (_32c5755 x0 x1)

noncomputable def «orderedFirst(_,_)_VERIFICATION-BASE_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := (_0e6f622 x0 x1) <|> (_b06eae6 x0 x1)

noncomputable def «candidateWins(_,_,_,_)_VERIFICATION-BASE_Bool_Val_Val_Float_Float» (x0 : SortVal) (x1 : SortVal) (x2 : SortFloat) (x3 : SortFloat) : Option SortBool := _4db727f x0 x1 x2 x3

noncomputable def _1c47615 : SortVal → SortVal → SortFloat → SortFloat → Option SortFloat
  | ITEM1, ITEM2, A, B => do
    let _Val0 <- «candidateWins(_,_,_,_)_VERIFICATION-BASE_Bool_Val_Val_Float_Float» ITEM1 ITEM2 A B
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return A

noncomputable def _361014b : SortVal → SortVal → SortFloat → SortFloat → Option SortFloat
  | ITEM1, ITEM2, A, B => do
    let _Val0 <- «candidateWins(_,_,_,_)_VERIFICATION-BASE_Bool_Val_Val_Float_Float» ITEM1 ITEM2 A B
    let _Val1 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM1
    let _Val2 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM2
    let _Val3 <- floatLt _Val1 _Val2
    let _Val4 <- notBool_ _Val3
    let _Val5 <- _andBool_ _Val0 _Val4
    let _Val6 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM1
    guard _Val5
    return _Val6

noncomputable def _5260c24 : SortVal → SortVal → SortFloat → SortFloat → Option SortFloat
  | ITEM1, ITEM2, A, B => do
    let _Val0 <- «candidateWins(_,_,_,_)_VERIFICATION-BASE_Bool_Val_Val_Float_Float» ITEM1 ITEM2 A B
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return B

noncomputable def _52a8f82 : SortVal → SortVal → SortFloat → SortFloat → Option SortFloat
  | ITEM1, ITEM2, A, B => do
    let _Val0 <- «candidateWins(_,_,_,_)_VERIFICATION-BASE_Bool_Val_Val_Float_Float» ITEM1 ITEM2 A B
    let _Val1 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM1
    let _Val2 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM2
    let _Val3 <- floatLt _Val1 _Val2
    let _Val4 <- _andBool_ _Val0 _Val3
    let _Val5 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM2
    guard _Val4
    return _Val5

noncomputable def _b789015 : SortVal → SortVal → SortFloat → SortFloat → Option SortFloat
  | ITEM1, ITEM2, A, B => do
    let _Val0 <- «candidateWins(_,_,_,_)_VERIFICATION-BASE_Bool_Val_Val_Float_Float» ITEM1 ITEM2 A B
    let _Val1 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM1
    let _Val2 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM2
    let _Val3 <- floatLt _Val1 _Val2
    let _Val4 <- notBool_ _Val3
    let _Val5 <- _andBool_ _Val0 _Val4
    let _Val6 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM2
    guard _Val5
    return _Val6

noncomputable def _ba02c87 : SortVal → SortVal → SortFloat → SortFloat → Option SortFloat
  | ITEM1, ITEM2, A, B => do
    let _Val0 <- «candidateWins(_,_,_,_)_VERIFICATION-BASE_Bool_Val_Val_Float_Float» ITEM1 ITEM2 A B
    let _Val1 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM1
    let _Val2 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM2
    let _Val3 <- floatLt _Val1 _Val2
    let _Val4 <- _andBool_ _Val0 _Val3
    let _Val5 <- «itemFloat(_)_VERIFICATION-BASE_Float_Val» ITEM1
    guard _Val4
    return _Val5

noncomputable def «stepSecond(_,_,_,_)_VERIFICATION-BASE_Float_Val_Val_Float_Float» (x0 : SortVal) (x1 : SortVal) (x2 : SortFloat) (x3 : SortFloat) : Option SortFloat := (_361014b x0 x1 x2 x3) <|> (_5260c24 x0 x1 x2 x3) <|> (_52a8f82 x0 x1 x2 x3)

noncomputable def «stepFirst(_,_,_,_)_VERIFICATION-BASE_Float_Val_Val_Float_Float» (x0 : SortVal) (x1 : SortVal) (x2 : SortFloat) (x3 : SortFloat) : Option SortFloat := (_1c47615 x0 x1 x2 x3) <|> (_b789015 x0 x1 x2 x3) <|> (_ba02c87 x0 x1 x2 x3)

mutual
  noncomputable def _2c2ad91 : SortVal → SortValSeq → SortFloat → SortFloat → Option SortFloat
    | ITEM1, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ITEM2 REST, A, B => do
      let _Val0 <- «stepFirst(_,_,_,_)_VERIFICATION-BASE_Float_Val_Val_Float_Float» ITEM1 ITEM2 A B
      let _Val1 <- «stepSecond(_,_,_,_)_VERIFICATION-BASE_Float_Val_Val_Float_Float» ITEM1 ITEM2 A B
      let _Val2 <- «innerSecond(_,_,_,_)_VERIFICATION-BASE_Float_Val_ValSeq_Float_Float» ITEM1 REST _Val0 _Val1
      return _Val2
    | _, _, _, _ => none

  noncomputable def «innerSecond(_,_,_,_)_VERIFICATION-BASE_Float_Val_ValSeq_Float_Float» (x0 : SortVal) (x1 : SortValSeq) (x2 : SortFloat) (x3 : SortFloat) : Option SortFloat := (_2c2ad91 x0 x1 x2 x3) <|> (_f08cce2 x0 x1 x2 x3)
end

mutual
  noncomputable def «innerFirst(_,_,_,_)_VERIFICATION-BASE_Float_Val_ValSeq_Float_Float» (x0 : SortVal) (x1 : SortValSeq) (x2 : SortFloat) (x3 : SortFloat) : Option SortFloat := (_c4cee72 x0 x1 x2 x3) <|> (_e4a4da7 x0 x1 x2 x3)

  noncomputable def _e4a4da7 : SortVal → SortValSeq → SortFloat → SortFloat → Option SortFloat
    | ITEM1, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ITEM2 REST, A, B => do
      let _Val0 <- «stepFirst(_,_,_,_)_VERIFICATION-BASE_Float_Val_Val_Float_Float» ITEM1 ITEM2 A B
      let _Val1 <- «stepSecond(_,_,_,_)_VERIFICATION-BASE_Float_Val_Val_Float_Float» ITEM1 ITEM2 A B
      let _Val2 <- «innerFirst(_,_,_,_)_VERIFICATION-BASE_Float_Val_ValSeq_Float_Float» ITEM1 REST _Val0 _Val1
      return _Val2
    | _, _, _, _ => none
end

mutual
  noncomputable def _63cc615 : SortValSeq → SortValSeq → SortFloat → SortFloat → Option SortFloat
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ITEM1 REST, ALL, A, B => do
      let _Val0 <- «innerFirst(_,_,_,_)_VERIFICATION-BASE_Float_Val_ValSeq_Float_Float» ITEM1 ALL A B
      let _Val1 <- «innerSecond(_,_,_,_)_VERIFICATION-BASE_Float_Val_ValSeq_Float_Float» ITEM1 ALL A B
      let _Val2 <- «outerSecond(_,_,_,_)_VERIFICATION-BASE_Float_ValSeq_ValSeq_Float_Float» REST ALL _Val0 _Val1
      return _Val2
    | _, _, _, _ => none

  noncomputable def «outerSecond(_,_,_,_)_VERIFICATION-BASE_Float_ValSeq_ValSeq_Float_Float» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortFloat) (x3 : SortFloat) : Option SortFloat := (_63cc615 x0 x1 x2 x3) <|> (_919f7a3 x0 x1 x2 x3)
end

mutual
  noncomputable def _8fbb0fc : SortValSeq → SortValSeq → SortFloat → SortFloat → Option SortFloat
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ITEM1 REST, ALL, A, B => do
      let _Val0 <- «innerFirst(_,_,_,_)_VERIFICATION-BASE_Float_Val_ValSeq_Float_Float» ITEM1 ALL A B
      let _Val1 <- «innerSecond(_,_,_,_)_VERIFICATION-BASE_Float_Val_ValSeq_Float_Float» ITEM1 ALL A B
      let _Val2 <- «outerFirst(_,_,_,_)_VERIFICATION-BASE_Float_ValSeq_ValSeq_Float_Float» REST ALL _Val0 _Val1
      return _Val2
    | _, _, _, _ => none

  noncomputable def «outerFirst(_,_,_,_)_VERIFICATION-BASE_Float_ValSeq_ValSeq_Float_Float» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortFloat) (x3 : SortFloat) : Option SortFloat := (_8fbb0fc x0 x1 x2 x3) <|> (_bb8678e x0 x1 x2 x3)
end