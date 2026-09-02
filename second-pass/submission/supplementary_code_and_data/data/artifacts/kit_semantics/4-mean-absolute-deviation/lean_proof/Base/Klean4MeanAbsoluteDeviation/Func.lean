import Klean4MeanAbsoluteDeviation.Inj

axiom «absFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _7c84698 : SortValSeq → SortFloat → SortFloat → Option SortFloat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, A => some A
  | _, _, _ => none

axiom «_-Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «_+Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom projectFloat (x0 : SortVal) : Option SortFloat

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _613283e : SortK → Option SortBool
  | K => some false

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _bcb822b : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _d74a36c : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortFloat Float) SortK.dotk => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _b662ad7 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

def _d06165d : SortValSeq → SortFloat → Option SortFloat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», A => some A
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

axiom «_/Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortFloat

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

noncomputable def _00d63fc : SortFloat → Option SortFloat
  | F => do
    let _Val0 <- «absFloat(_)_FLOAT_Float_Float» F
    return _Val0

noncomputable def _fabe8f9 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_-Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _dc1bc34 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_+Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isFloat (x0 : SortK) : Option SortBool := (_d74a36c x0) <|> (_613283e x0)

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _5d69a53 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «vsLen(_)_MPY-CORE_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_5d69a53 x0) <|> (_b662ad7 x0)
end

noncomputable def _ca2a05d : SortFloat → SortInt → Option SortFloat
  | F, I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    let _Val1 <- «_/Float__FLOAT_Float_Float_Float» F _Val0
    return _Val1

noncomputable def absF (x0 : SortFloat) : Option SortFloat := _00d63fc x0

noncomputable def subF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _fabe8f9 x0 x1

noncomputable def addF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _dc1bc34 x0 x1

mutual
  def _27920c1 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allFloatVS(_)_VERIFICATION-SYNTAX_Bool_ValSeq» R
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allFloatVS(_)_VERIFICATION-SYNTAX_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_27920c1 x0) <|> (_bcb822b x0)
end

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def _d56128c : SortValSeq → Option SortFloat
  | VS => do
    let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
    let _Val1 <- «_==Int_» _Val0 0
    guard _Val1
    return (0.0 : Float)

noncomputable def divFloatIntV (x0 : SortFloat) (x1 : SortInt) : Option SortFloat := _ca2a05d x0 x1

mutual
  noncomputable def _27400b5 : SortValSeq → SortFloat → SortFloat → Option SortFloat
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R, M, A => do
      let _Val0 <- projectFloat V
      let _Val1 <- subF _Val0 M
      let _Val2 <- absF _Val1
      let _Val3 <- addF A _Val2
      let _Val4 <- «deviationFloatVS(_,_,_)_VERIFICATION-SYNTAX_Float_ValSeq_Float_Float» R M _Val3
      return _Val4
    | _, _, _ => none

  noncomputable def «deviationFloatVS(_,_,_)_VERIFICATION-SYNTAX_Float_ValSeq_Float_Float» (x0 : SortValSeq) (x1 : SortFloat) (x2 : SortFloat) : Option SortFloat := (_27400b5 x0 x1 x2) <|> (_7c84698 x0 x1 x2)
end

mutual
  noncomputable def _6b24d12 : SortValSeq → SortFloat → Option SortFloat
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R, A => do
      let _Val0 <- projectFloat V
      let _Val1 <- addF A _Val0
      let _Val2 <- «sumFloatVS(_,_)_VERIFICATION-SYNTAX_Float_ValSeq_Float» R _Val1
      return _Val2
    | _, _ => none

  noncomputable def «sumFloatVS(_,_)_VERIFICATION-SYNTAX_Float_ValSeq_Float» (x0 : SortValSeq) (x1 : SortFloat) : Option SortFloat := (_6b24d12 x0 x1) <|> (_d06165d x0 x1)
end

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def _aa06f3b : SortValSeq → Option SortFloat
  | VS => do
    let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
    let _Val1 <- «_=/=Int_» _Val0 0
    let _Val2 <- «sumFloatVS(_,_)_VERIFICATION-SYNTAX_Float_ValSeq_Float» VS (0.0 : Float)
    let _Val3 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
    let _Val4 <- divFloatIntV _Val2 _Val3
    let _Val5 <- «deviationFloatVS(_,_,_)_VERIFICATION-SYNTAX_Float_ValSeq_Float_Float» VS _Val4 (0.0 : Float)
    let _Val6 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
    let _Val7 <- divFloatIntV _Val5 _Val6
    guard _Val1
    return _Val7

noncomputable def «madResult(_)_VERIFICATION-SYNTAX_Float_ValSeq» (x0 : SortValSeq) : Option SortFloat := (_aa06f3b x0) <|> (_d56128c x0)