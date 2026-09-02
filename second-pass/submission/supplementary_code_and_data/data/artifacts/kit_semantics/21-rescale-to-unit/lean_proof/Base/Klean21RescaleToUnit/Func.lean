import Klean21RescaleToUnit.Inj

def _2cf19d6 : SortValSeq → SortVal → Option SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», CURRENT => some CURRENT
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _613283e : SortK → Option SortBool
  | K => some false

def _d74a36c : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortFloat Float) SortK.dotk => some true
  | _ => none

def _6185b24 : SortValSeq → SortFloat → Option SortFloat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», M => some M
  | _, _ => none

axiom maxFOpaque (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom projectFloatTotal (x0 : SortVal) : Option SortFloat

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _4c85ed5 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _788897a : SortValSeq → SortValSeq → SortFloat → SortFloat → Option SortValSeq
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _LO, _HI => some ACC
  | _, _, _, _ => none

axiom minFOpaque (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

def _afc8114 : SortValSeq → SortFloat → Option SortFloat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», M => some M
  | _, _ => none

def _8c03b30 : SortValSeq → Option SortFloat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some (0.0 : Float)
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

axiom «_-Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

noncomputable def _List_ (x0 : SortList) (x1 : SortList) : Option SortList := some ⟨x0.coll ++ x1.coll⟩

noncomputable def _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap :=
  if kleanMapDisjointModel x0.coll x1.coll then
    some ⟨x0.coll ++ x1.coll⟩
  else none

noncomputable def «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=
  some ⟨[(x0, x1)]⟩

axiom «_/Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

def _ae4f944 : SortValSeq → Option SortFloat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some (0.0 : Float)
  | _ => none

mutual
  def _0a4df99 : SortValSeq → SortVal → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, _CURRENT => do
      let _Val0 <- «lastVal(_,_)_VERIFICATION_Val_ValSeq_Val» REST V
      return _Val0
    | _, _ => none

  def «lastVal(_,_)_VERIFICATION_Val_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortVal := (_0a4df99 x0 x1) <|> (_2cf19d6 x0 x1)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def isFloat (x0 : SortK) : Option SortBool := (_d74a36c x0) <|> (_613283e x0)

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _fabe8f9 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_-Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _d8a2a0c : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_/Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

def _1155ac1 : SortValSeq → Option SortFloat
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _REST => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return (0.0 : Float)
  | _ => none

def _2589da7 : SortValSeq → Option SortFloat
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _REST => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return (0.0 : Float)
  | _ => none

def _29d2c76 : SortValSeq → SortFloat → Option SortFloat
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _REST, M => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return M
  | _, _ => none

def _30704ce : SortVal → Option SortBool
  | V => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

def _f754949 : SortValSeq → SortFloat → Option SortFloat
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _REST, M => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return M
  | _, _ => none

mutual
  def _59ad70c : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allFloatVS(_)_VERIFICATION_Bool_ValSeq» REST
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allFloatVS(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_4c85ed5 x0) <|> (_59ad70c x0)
end

noncomputable def subF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _fabe8f9 x0 x1

noncomputable def divF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _d8a2a0c x0 x1

mutual
  noncomputable def _20bc4ec : SortValSeq → SortFloat → Option SortFloat
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, M => do
      let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- projectFloatTotal V
      let _Val2 <- maxFOpaque M _Val1
      let _Val3 <- «maxTailF(_,_)_VERIFICATION_Float_ValSeq_Float» REST _Val2
      guard _Val0
      return _Val3
    | _, _ => none

  noncomputable def «maxTailF(_,_)_VERIFICATION_Float_ValSeq_Float» (x0 : SortValSeq) (x1 : SortFloat) : Option SortFloat := (_20bc4ec x0 x1) <|> (_29d2c76 x0 x1) <|> (_6185b24 x0 x1)
end

def «definedProjectFloat(_)_VERIFICATION_Bool_Val» (x0 : SortVal) : Option SortBool := _30704ce x0

mutual
  noncomputable def _79c4207 : SortValSeq → SortFloat → Option SortFloat
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, M => do
      let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- projectFloatTotal V
      let _Val2 <- minFOpaque M _Val1
      let _Val3 <- «minTailF(_,_)_VERIFICATION_Float_ValSeq_Float» REST _Val2
      guard _Val0
      return _Val3
    | _, _ => none

  noncomputable def «minTailF(_,_)_VERIFICATION_Float_ValSeq_Float» (x0 : SortValSeq) (x1 : SortFloat) : Option SortFloat := (_79c4207 x0 x1) <|> (_afc8114 x0 x1) <|> (_f754949 x0 x1)
end

mutual
  noncomputable def «scaleAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq_Float_Float» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortFloat) (x3 : SortFloat) : Option SortValSeq := (_788897a x0 x1 x2 x3) <|> (_c7f82a4 x0 x1 x2 x3) <|> (_de139e0 x0 x1 x2 x3)

  noncomputable def _c7f82a4 : SortValSeq → SortValSeq → SortFloat → SortFloat → Option SortValSeq
    | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, LO, HI => do
      let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- projectFloatTotal V
      let _Val2 <- subF _Val1 LO
      let _Val3 <- subF HI LO
      let _Val4 <- divF _Val2 _Val3
      let _Val5 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortFloat SortVal) _Val4) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val6 <- «scaleAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq_Float_Float» _Val5 REST LO HI
      guard _Val0
      return _Val6
    | _, _, _, _ => none

  noncomputable def _de139e0 : SortValSeq → SortValSeq → SortFloat → SortFloat → Option SortValSeq
    | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, LO, HI => do
      let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val3 <- «scaleAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq_Float_Float» _Val2 REST LO HI
      guard _Val1
      return _Val3
    | _, _, _, _ => none
end

noncomputable def _6a844c8 : SortValSeq → Option SortFloat
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- projectFloatTotal V
    let _Val2 <- «maxTailF(_,_)_VERIFICATION_Float_ValSeq_Float» REST _Val1
    guard _Val0
    return _Val2
  | _ => none

noncomputable def _d353d32 : SortValSeq → Option SortFloat
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- projectFloatTotal V
    let _Val2 <- «minTailF(_,_)_VERIFICATION_Float_ValSeq_Float» REST _Val1
    guard _Val0
    return _Val2
  | _ => none

noncomputable def «maxVF(_)_VERIFICATION_Float_ValSeq» (x0 : SortValSeq) : Option SortFloat := (_2589da7 x0) <|> (_6a844c8 x0) <|> (_8c03b30 x0)

noncomputable def «minVF(_)_VERIFICATION_Float_ValSeq» (x0 : SortValSeq) : Option SortFloat := (_1155ac1 x0) <|> (_ae4f944 x0) <|> (_d353d32 x0)