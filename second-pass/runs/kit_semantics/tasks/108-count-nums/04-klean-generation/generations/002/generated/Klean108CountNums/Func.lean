import Klean108CountNums.Inj

def _105572a : SortK → Option SortBool
  | K => some false

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _d0a8392 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _ccd5389 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _3a84976 : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

def _9d5b71b : SortInt → SortIntSeq → Option SortInt
  | F, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some F
  | _, _ => none

axiom «decimalCodes(_)_VERIFICATION_IntSeq_Int» (x0 : SortInt) : Option SortIntSeq

axiom projectIntTotal (x0 : SortVal) : Option SortInt

def _d427c90 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

def _5d28b94 : SortInt → SortIntSeq → Option SortInt
  | C, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some C
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

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _0d0e2a1 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_>=Int_» I 0
    guard _Val0
    return I

mutual
  def _2c40c5a : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «_-Int_» C 48
      let _Val1 <- «codeDigitSum(_)_VERIFICATION_Int_IntSeq» R
      let _Val2 <- «_+Int_» _Val0 _Val1
      return _Val2
    | _ => none

  def «codeDigitSum(_)_VERIFICATION_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_2c40c5a x0) <|> (_ccd5389 x0)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _4cdf918 : SortInt → SortIntSeq → Option SortInt
    | 0, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «_-Int_» C 48
      let _Val1 <- «chooseFirst(_,_)_VERIFICATION_Int_Int_IntSeq» _Val0 R
      return _Val1
    | _, _ => none

  def «chooseFirst(_,_)_VERIFICATION_Int_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortInt := (_4cdf918 x0 x1) <|> (_9d5b71b x0 x1)
end

def _e67a041 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_-Int_» 0 I
    guard _Val0
    return _Val1

mutual
  def «lastCode(_,_)_VERIFICATION_Int_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortInt := (_5d28b94 x0 x1) <|> (_ad17ed2 x0 x1)

  def _ad17ed2 : SortInt → SortIntSeq → Option SortInt
    | _Gen0, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «lastCode(_,_)_VERIFICATION_Int_Int_IntSeq» C R
      return _Val0
    | _, _ => none
end

mutual
  def «allDigitCodes(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_3a84976 x0) <|> (_ea60090 x0)

  def _ea60090 : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «_<=Int_» 48 C
      let _Val1 <- «_<=Int_» C 57
      let _Val2 <- _andBool_ _Val0 _Val1
      let _Val3 <- «allDigitCodes(_)_VERIFICATION_Bool_IntSeq» R
      let _Val4 <- _andBool_ _Val2 _Val3
      return _Val4
    | _ => none
end

mutual
  def _01539d8 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allInts(_)_VERIFICATION_Bool_ValSeq» R
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allInts(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_01539d8 x0) <|> (_d0a8392 x0)
end

def _21add3b : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def «magnitude(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_0d0e2a1 x0) <|> (_e67a041 x0)

def «definedProjectInt(_)_VERIFICATION_Bool_Val» (x0 : SortVal) : Option SortBool := _21add3b x0

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def _bbbbcdf : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «magnitude(_)_VERIFICATION_Int_Int» I
    let _Val2 <- «decimalCodes(_)_VERIFICATION_IntSeq_Int» _Val1
    let _Val3 <- «codeDigitSum(_)_VERIFICATION_Int_IntSeq» _Val2
    guard _Val0
    return _Val3

noncomputable def _c5c1b85 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «magnitude(_)_VERIFICATION_Int_Int» I
    let _Val2 <- «decimalCodes(_)_VERIFICATION_IntSeq_Int» _Val1
    let _Val3 <- «codeDigitSum(_)_VERIFICATION_Int_IntSeq» _Val2
    let _Val4 <- «magnitude(_)_VERIFICATION_Int_Int» I
    let _Val5 <- «decimalCodes(_)_VERIFICATION_IntSeq_Int» _Val4
    let _Val6 <- «chooseFirst(_,_)_VERIFICATION_Int_Int_IntSeq» 0 _Val5
    let _Val7 <- «_*Int_» 2 _Val6
    let _Val8 <- «_-Int_» _Val3 _Val7
    guard _Val0
    return _Val8

noncomputable def «signedDigitSum(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_bbbbcdf x0) <|> (_c5c1b85 x0)

mutual
  noncomputable def _503a789 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «countNumsSpec(_)_VERIFICATION_Int_ValSeq» R
      guard _Val1
      return _Val2
    | _ => none

  noncomputable def _712328d : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- projectIntTotal V
      let _Val2 <- «signedDigitSum(_)_VERIFICATION_Int_Int» _Val1
      let _Val3 <- «_>Int_» _Val2 0
      let _Val4 <- kite _Val3 1 0
      let _Val5 <- «countNumsSpec(_)_VERIFICATION_Int_ValSeq» R
      let _Val6 <- «_+Int_» _Val4 _Val5
      guard _Val0
      return _Val6
    | _ => none

  noncomputable def «countNumsSpec(_)_VERIFICATION_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_503a789 x0) <|> (_712328d x0) <|> (_d427c90 x0)
end