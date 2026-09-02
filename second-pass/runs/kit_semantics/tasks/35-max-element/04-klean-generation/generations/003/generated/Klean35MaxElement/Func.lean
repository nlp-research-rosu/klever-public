import Klean35MaxElement.Inj

def _0092bdb : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _07bcf22 : SortNumericView → SortNumericView → Option SortBool
  | SortNumericView.«nOther(_)_VERIFICATION_NumericView_Val» _Gen0, _Gen1 => some false
  | _, _ => none

def _105572a : SortK → Option SortBool
  | K => some false

def _495da55 : SortK → Option SortBool
  | K => some false

def _613283e : SortK → Option SortBool
  | K => some false

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _d74a36c : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortFloat Float) SortK.dotk => some true
  | _ => none

def _dadad71 : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortBool Bool) SortK.dotk => some true
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _95cb29f : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortStr Str) SortK.dotk => some true
  | _ => none

def _e10ded0 : SortK → Option SortBool
  | K => some false

def _fb7db52 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom projectIntTotal (x0 : SortVal) : Option SortInt

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _2830db5 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom «_>Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «_<Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «--Float__FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

axiom «Float2Int(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

axiom «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortFloat

axiom «exponentBitsFloat(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

axiom «floorFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

axiom «isNaN(_)_FLOAT_Bool_Float» (x0 : SortFloat) : Option SortBool

axiom «maxValueFloat(_,_)_FLOAT_Float_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortFloat

axiom «precisionFloat(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

axiom projectBoolTotal (x0 : SortVal) : Option SortBool

def _2fa0fd3 : SortVal → SortValSeq → Option SortVal
  | M, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some M
  | _, _ => none

def _4b7fd38 : SortBool → Option SortInt
  | false => some 0
  | _ => none

axiom «ceilFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

def _c71764f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _f3f7875 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1 => some true
  | _, _ => none

axiom projectStrTotal (x0 : SortVal) : Option SortStr

def _b83254f : SortStr → Option SortIntSeq
  | SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS => some CS

def _73f627a : SortBool → Option SortInt
  | true => some 1
  | _ => none

def _83d7bea : SortInt → SortValSeq → Option SortVal
  | M, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some ((@inj SortInt SortVal) M)
  | _, _ => none

def _8b3a69f : SortNumericView → SortNumericView → Option SortBool
  | _Gen0, SortNumericView.«nOther(_)_VERIFICATION_NumericView_Val» _Gen1 => some false
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

axiom «maxFloat(_,_)_FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

def _d0e5d77 : SortFloat → SortValSeq → Option SortVal
  | M, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some ((@inj SortFloat SortVal) M)
  | _, _ => none

axiom projectFloatTotal (x0 : SortVal) : Option SortFloat

def _afad684 : SortVal → SortValSeq → Option SortVal
  | M, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some M
  | _, _ => none

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def isFloat (x0 : SortK) : Option SortBool := (_d74a36c x0) <|> (_613283e x0)

def isBool (x0 : SortK) : Option SortBool := (_dadad71 x0) <|> (_495da55 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isStr (x0 : SortK) : Option SortBool := (_95cb29f x0) <|> (_e10ded0 x0)

def _29cb876 : SortNumericView → SortNumericView → Option SortBool
  | SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» I, SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» J => do
    let _Val0 <- «_>Int_» I J
    return _Val0
  | _, _ => none

def _cc09b1d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_>Int_» A B
    guard _Val0
    return false
  | _, _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _fee1f6e : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_>Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

noncomputable def _5667141 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_<Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

def _c875e09 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_<Int_» A B
    guard _Val0
    return true
  | _, _ => none

noncomputable def _e5f1d08 : SortInt → Option SortFloat
  | I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    return _Val0

def «codesOf(_)_VERIFICATION_IntSeq_Str» (x0 : SortStr) : Option SortIntSeq := _b83254f x0

def «boolAsInt(_)_MPY-CORE_Int_Bool» (x0 : SortBool) : Option SortInt := (_4b7fd38 x0) <|> (_73f627a x0)

def «maxIntNumericVS(_,_)_VERIFICATION_Val_Int_ValSeq» (x0 : SortInt) (x1 : SortValSeq) : Option SortVal := _83d7bea x0 x1

noncomputable def _c8974b5 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «maxFloat(_,_)_FLOAT_Float_Float_Float» F1 F2
    return _Val0

def «maxFloatNumericVS(_,_)_VERIFICATION_Val_Float_ValSeq» (x0 : SortFloat) (x1 : SortValSeq) : Option SortVal := _d0e5d77 x0 x1

noncomputable def _1aa4a61 : SortVal → Option SortNumericView
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- projectIntTotal V
    guard _Val0
    return (SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» _Val1)

noncomputable def _3cdc559 : SortFloat → Option SortBool
  | F => do
    let _Val0 <- «precisionFloat(_)_FLOAT_Int_Float» F
    let _Val1 <- «exponentBitsFloat(_)_FLOAT_Int_Float» F
    let _Val2 <- «maxValueFloat(_,_)_FLOAT_Float_Int_Int» _Val0 _Val1
    let _Val3 <- «_>Float__FLOAT_Bool_Float_Float» F _Val2
    let _Val4 <- «precisionFloat(_)_FLOAT_Int_Float» F
    let _Val5 <- «exponentBitsFloat(_)_FLOAT_Int_Float» F
    let _Val6 <- «maxValueFloat(_,_)_FLOAT_Float_Int_Int» _Val4 _Val5
    let _Val7 <- «--Float__FLOAT_Float_Float» _Val6
    let _Val8 <- «_<Float__FLOAT_Bool_Float_Float» F _Val7
    let _Val9 <- _orBool_ _Val3 _Val8
    return _Val9

noncomputable def _c319d99 : SortVal → Option SortNumericView
  | V => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- projectFloatTotal V
    guard _Val0
    return (SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» _Val1)

def _149c7b8 : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val4 <- _orBool_ _Val2 _Val3
    return _Val4

noncomputable def _2e6d04a : SortVal → Option SortNumericView
  | V => do
    let _Val0 <- isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- projectBoolTotal V
    guard _Val0
    return (SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» _Val1)

mutual
  def _1768a9e : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- isStr (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allStrVS(_)_VERIFICATION_Bool_ValSeq» REST
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allStrVS(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_1768a9e x0) <|> (_fb7db52 x0)
end

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

noncomputable def gtF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _fee1f6e x0 x1

noncomputable def floatLt (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _5667141 x0 x1

mutual
  def _6a28f31 : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      guard _Val0
      return _Val1
    | _, _ => none

  def «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_0092bdb x0 x1) <|> (_6a28f31 x0 x1) <|> (_c71764f x0 x1) <|> (_c875e09 x0 x1) <|> (_cc09b1d x0 x1) <|> (_f3f7875 x0 x1)
end

noncomputable def intToF (x0 : SortInt) : Option SortFloat := _e5f1d08 x0

def _9311d36 : SortNumericView → SortNumericView → Option SortBool
  | SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» B, SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» I => do
    let _Val0 <- «boolAsInt(_)_MPY-CORE_Int_Bool» B
    let _Val1 <- «_>Int_» _Val0 I
    return _Val1
  | _, _ => none

def _eea61ce : SortNumericView → SortNumericView → Option SortBool
  | SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» I, SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» B => do
    let _Val0 <- «boolAsInt(_)_MPY-CORE_Int_Bool» B
    let _Val1 <- «_>Int_» I _Val0
    return _Val1
  | _, _ => none

def _f78f1fa : SortNumericView → SortNumericView → Option SortBool
  | SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» B1, SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» B2 => do
    let _Val0 <- «boolAsInt(_)_MPY-CORE_Int_Bool» B1
    let _Val1 <- «boolAsInt(_)_MPY-CORE_Int_Bool» B2
    let _Val2 <- «_>Int_» _Val0 _Val1
    return _Val2
  | _, _ => none

noncomputable def maxFOpaque (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _c8974b5 x0 x1

noncomputable def «isInfinite(_)_FLOAT_Bool_Float» (x0 : SortFloat) : Option SortBool := _3cdc559 x0

def «isNumericV(_)_VERIFICATION_Bool_Val» (x0 : SortVal) : Option SortBool := _149c7b8 x0

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def _fcf8067 : SortNumericView → SortNumericView → Option SortBool
  | SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» F1, SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» F2 => do
    let _Val0 <- gtF F1 F2
    return _Val0
  | _, _ => none

noncomputable def _6a82bc3 : SortFloat → Option SortBool
  | F => do
    let _Val0 <- «isNaN(_)_FLOAT_Bool_Float» F
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «isInfinite(_)_FLOAT_Bool_Float» F
    let _Val3 <- notBool_ _Val2
    let _Val4 <- _andBool_ _Val1 _Val3
    return _Val4

def _7b93662 : SortVal → Option SortNumericView
  | V => do
    let _Val0 <- «isNumericV(_)_VERIFICATION_Bool_Val» V
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return (SortNumericView.«nOther(_)_VERIFICATION_NumericView_Val» V)

mutual
  def «allNumericVS(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_2830db5 x0) <|> (_fd9c7f6 x0)

  def _fd9c7f6 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «isNumericV(_)_VERIFICATION_Bool_Val» V
      let _Val1 <- «allNumericVS(_)_VERIFICATION_Bool_ValSeq» REST
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none
end

mutual
  noncomputable def _708394e : SortVal → SortValSeq → Option SortVal
    | M, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- projectStrTotal M
      let _Val1 <- «codesOf(_)_VERIFICATION_IntSeq_Str» _Val0
      let _Val2 <- projectStrTotal V
      let _Val3 <- «codesOf(_)_VERIFICATION_IntSeq_Str» _Val2
      let _Val4 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» _Val1 _Val3
      let _Val5 <- kite _Val4 V M
      let _Val6 <- «maxStrGeneralVS(_,_)_VERIFICATION_Val_Val_ValSeq» _Val5 REST
      return _Val6
    | _, _ => none

  noncomputable def «maxStrGeneralVS(_,_)_VERIFICATION_Val_Val_ValSeq» (x0 : SortVal) (x1 : SortValSeq) : Option SortVal := (_2fa0fd3 x0 x1) <|> (_708394e x0 x1)
end

noncomputable def floatFinite (x0 : SortFloat) : Option SortBool := _6a82bc3 x0

noncomputable def «numericView(_)_VERIFICATION_NumericView_Val» (x0 : SortVal) : Option SortNumericView := (_1aa4a61 x0) <|> (_2e6d04a x0) <|> (_7b93662 x0) <|> (_c319d99 x0)

noncomputable def _4c721dd : SortInt → SortFloat → Option SortBool
  | I, F => do
    let _Val0 <- floatFinite F
    let _Val1 <- «ceilFloat(_)_FLOAT_Float_Float» F
    let _Val2 <- «Float2Int(_)_FLOAT_Int_Float» _Val1
    let _Val3 <- «_>Int_» _Val2 I
    guard _Val0
    return _Val3

noncomputable def _5784e42 : SortFloat → SortInt → Option SortBool
  | F, I => do
    let _Val0 <- floatFinite F
    let _Val1 <- notBool_ _Val0
    let _Val2 <- intToF I
    let _Val3 <- floatLt F _Val2
    guard _Val1
    return _Val3

noncomputable def _69e2bae : SortInt → SortFloat → Option SortBool
  | I, F => do
    let _Val0 <- floatFinite F
    let _Val1 <- notBool_ _Val0
    let _Val2 <- intToF I
    let _Val3 <- floatLt _Val2 F
    guard _Val1
    return _Val3

noncomputable def _e4aab2f : SortFloat → SortInt → Option SortBool
  | F, I => do
    let _Val0 <- floatFinite F
    let _Val1 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val2 <- «Float2Int(_)_FLOAT_Int_Float» _Val1
    let _Val3 <- «_<Int_» _Val2 I
    guard _Val0
    return _Val3

noncomputable def ltIF (x0 : SortInt) (x1 : SortFloat) : Option SortBool := (_4c721dd x0 x1) <|> (_69e2bae x0 x1)

noncomputable def ltFI (x0 : SortFloat) (x1 : SortInt) : Option SortBool := (_5784e42 x0 x1) <|> (_e4aab2f x0 x1)

noncomputable def _6c8442f : SortNumericView → SortNumericView → Option SortBool
  | SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» F, SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» I => do
    let _Val0 <- ltIF I F
    return _Val0
  | _, _ => none

noncomputable def _77afd50 : SortNumericView → SortNumericView → Option SortBool
  | SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» F, SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» B => do
    let _Val0 <- «boolAsInt(_)_MPY-CORE_Int_Bool» B
    let _Val1 <- ltIF _Val0 F
    return _Val1
  | _, _ => none

noncomputable def _2e3fc30 : SortNumericView → SortNumericView → Option SortBool
  | SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» I, SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» F => do
    let _Val0 <- ltFI F I
    return _Val0
  | _, _ => none

noncomputable def _da4ee2a : SortNumericView → SortNumericView → Option SortBool
  | SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» B, SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» F => do
    let _Val0 <- «boolAsInt(_)_MPY-CORE_Int_Bool» B
    let _Val1 <- ltFI F _Val0
    return _Val1
  | _, _ => none

noncomputable def «numericGt(_,_)_VERIFICATION_Bool_NumericView_NumericView» (x0 : SortNumericView) (x1 : SortNumericView) : Option SortBool := (_07bcf22 x0 x1) <|> (_29cb876 x0 x1) <|> (_2e3fc30 x0 x1) <|> (_6c8442f x0 x1) <|> (_77afd50 x0 x1) <|> (_8b3a69f x0 x1) <|> (_9311d36 x0 x1) <|> (_da4ee2a x0 x1) <|> (_eea61ce x0 x1) <|> (_f78f1fa x0 x1) <|> (_fcf8067 x0 x1)

mutual
  noncomputable def «maxNumericGeneralVS(_,_)_VERIFICATION_Val_Val_ValSeq» (x0 : SortVal) (x1 : SortValSeq) : Option SortVal := (_afad684 x0 x1) <|> (_bb66862 x0 x1)

  noncomputable def _bb66862 : SortVal → SortValSeq → Option SortVal
    | M, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «numericView(_)_VERIFICATION_NumericView_Val» V
      let _Val1 <- «numericView(_)_VERIFICATION_NumericView_Val» M
      let _Val2 <- «numericGt(_,_)_VERIFICATION_Bool_NumericView_NumericView» _Val0 _Val1
      let _Val3 <- kite _Val2 V M
      let _Val4 <- «maxNumericGeneralVS(_,_)_VERIFICATION_Val_Val_ValSeq» _Val3 REST
      return _Val4
    | _, _ => none
end