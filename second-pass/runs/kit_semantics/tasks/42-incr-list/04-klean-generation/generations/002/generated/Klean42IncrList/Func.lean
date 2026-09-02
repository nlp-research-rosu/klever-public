import Klean42IncrList.Inj

axiom «_*Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «_^Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortFloat

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

axiom «_-Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «_/Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «floorFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _41beda7 : SortValSeq → SortValSeq → Option SortValSeq
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some ACC
  | _, _ => none

axiom «_^Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _5362b6a : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _74e853d : SortVal → Option SortBool
  | SortVal.inj_SortInt _Gen0 => some true
  | _ => none

def _79ee8ff : SortVal → Option SortBool
  | SortVal.inj_SortBool _Gen0 => some true
  | _ => none

def _7f418f1 : SortVal → Option SortBool
  | _Gen0 => some false

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

axiom «_+Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

def _cdc4f16 : SortVal → Option SortBool
  | SortVal.inj_SortFloat _Gen0 => some true
  | _ => none

noncomputable def _07c1bf0 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_*Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

def _13d6ee6 : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_*Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

noncomputable def _9daeaea : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_^Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _e5f1d08 : SortInt → Option SortFloat
  | I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    return _Val0

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

noncomputable def _fabe8f9 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_-Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _2b8c3d8 : SortInt → SortFloat → Option SortFloat
  | I, F => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    let _Val1 <- «_/Float__FLOAT_Float_Float_Float» _Val0 F
    return _Val1

noncomputable def _ca2a05d : SortFloat → SortInt → Option SortFloat
  | F, I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    let _Val1 <- «_/Float__FLOAT_Float_Float_Float» F _Val0
    return _Val1

noncomputable def _d8a2a0c : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_/Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _edb22f9 : SortInt → SortInt → Option SortFloat
  | I1, I2 => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I1 53 11
    let _Val1 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I2 53 11
    let _Val2 <- «_/Float__FLOAT_Float_Float_Float» _Val0 _Val1
    return _Val2

noncomputable def _ea38624 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_/Float__FLOAT_Float_Float_Float» F1 F2
    let _Val1 <- «floorFloat(_)_FLOAT_Float_Float» _Val0
    let _Val2 <- «_*Float__FLOAT_Float_Float_Float» _Val1 F2
    let _Val3 <- «_-Float__FLOAT_Float_Float_Float» F1 _Val2
    return _Val3

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def _bc844c7 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_+Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _4f03d42 : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_>=Int_» I2 0
    let _Val1 <- «_^Int_» I1 I2
    guard _Val0
    return ((@inj SortInt SortVal) _Val1)
  | _, _, _ => none

def _614d946 : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_-Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

noncomputable def _dc1bc34 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_+Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

def «isNumericVal(_)_VERIFICATION_Bool_Val» (x0 : SortVal) : Option SortBool := (_74e853d x0) <|> (_79ee8ff x0) <|> (_cdc4f16 x0) <|> (_7f418f1 x0)

noncomputable def mulF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _07c1bf0 x0 x1

noncomputable def powF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _9daeaea x0 x1

noncomputable def intToF (x0 : SortInt) : Option SortFloat := _e5f1d08 x0

noncomputable def subF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _fabe8f9 x0 x1

noncomputable def intFloatDiv (x0 : SortInt) (x1 : SortFloat) : Option SortFloat := _2b8c3d8 x0 x1

noncomputable def divFloatIntV (x0 : SortFloat) (x1 : SortInt) : Option SortFloat := _ca2a05d x0 x1

noncomputable def divF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _d8a2a0c x0 x1

noncomputable def divII (x0 : SortInt) (x1 : SortInt) : Option SortFloat := _edb22f9 x0 x1

noncomputable def floatMod (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _ea38624 x0 x1

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def _c2eab84 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» A B
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _, _, _ => none

noncomputable def addF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _dc1bc34 x0 x1

mutual
  def «allNumeric(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_5362b6a x0) <|> (_e4b219f x0)

  def _e4b219f : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- «isNumericVal(_)_VERIFICATION_Bool_Val» V
      let _Val1 <- «allNumeric(_)_VERIFICATION_Bool_ValSeq» R
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none
end

noncomputable def _30456db : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- mulF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _a4f5818 : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- powF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _1909c2e : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- powF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _50f1b5a : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- mulF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _ca41a23 : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- mulF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _e0a3283 : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- powF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _a6670cb : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- subF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _d8961f0 : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- subF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _ebcc6ed : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- subF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _4f373ea : SortString → SortVal → SortVal → Option SortVal
  | "/", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intFloatDiv I F
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _3598da3 : SortString → SortVal → SortVal → Option SortVal
  | "/", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- divFloatIntV F I
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _42bfa12 : SortString → SortVal → SortVal → Option SortVal
  | "/", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- divF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _798d463 : SortString → SortVal → SortVal → Option SortVal
  | "/", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- divII I1 I2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _2acce51 : SortString → SortVal → SortVal → Option SortVal
  | "%", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- floatMod F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _7f23ecf : SortString → SortVal → SortVal → Option SortVal
  | "%", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

noncomputable def _dece19f : SortString → SortVal → SortVal → Option SortVal
  | "//", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I1 I2
    let _Val1 <- «_-Int_» I1 _Val0
    let _Val2 <- «_/Int_» _Val1 I2
    return ((@inj SortInt SortVal) _Val2)
  | _, _, _ => none

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def _a4f63fd : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- addF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _b009d60 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- addF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _f394023 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- addF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

def _7ff1b9f : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortBool B, SortVal.inj_SortInt I => do
    let _Val0 <- kite B 1 0
    let _Val1 <- «_+Int_» _Val0 I
    return ((@inj SortInt SortVal) _Val1)
  | _, _, _ => none

def _bb59890 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortInt I, SortVal.inj_SortBool B => do
    let _Val0 <- kite B 1 0
    let _Val1 <- «_+Int_» I _Val0
    return ((@inj SortInt SortVal) _Val1)
  | _, _, _ => none

noncomputable def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» (x0 : SortString) (x1 : SortVal) (x2 : SortVal) : Option SortVal := (_13d6ee6 x0 x1 x2) <|> (_1909c2e x0 x1 x2) <|> (_2acce51 x0 x1 x2) <|> (_30456db x0 x1 x2) <|> (_3598da3 x0 x1 x2) <|> (_42bfa12 x0 x1 x2) <|> (_4f03d42 x0 x1 x2) <|> (_4f373ea x0 x1 x2) <|> (_50f1b5a x0 x1 x2) <|> (_50f1b5a x0 x1 x2) <|> (_614d946 x0 x1 x2) <|> (_798d463 x0 x1 x2) <|> (_7f23ecf x0 x1 x2) <|> (_7ff1b9f x0 x1 x2) <|> (_a4f5818 x0 x1 x2) <|> (_a4f63fd x0 x1 x2) <|> (_a4f63fd x0 x1 x2) <|> (_a6670cb x0 x1 x2) <|> (_b009d60 x0 x1 x2) <|> (_bb59890 x0 x1 x2) <|> (_bc844c7 x0 x1 x2) <|> (_c2eab84 x0 x1 x2) <|> (_ca41a23 x0 x1 x2) <|> (_ca41a23 x0 x1 x2) <|> (_d8961f0 x0 x1 x2) <|> (_d8961f0 x0 x1 x2) <|> (_dece19f x0 x1 x2) <|> (_e0a3283 x0 x1 x2) <|> (_ebcc6ed x0 x1 x2) <|> (_ebcc6ed x0 x1 x2) <|> (_f394023 x0 x1 x2) <|> (_f394023 x0 x1 x2)

mutual
  noncomputable def «incrAcc(_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_41beda7 x0 x1) <|> (_d2155e9 x0 x1)

  noncomputable def _d2155e9 : SortValSeq → SortValSeq → Option SortValSeq
    | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" V ((@inj SortInt SortVal) 1)
      let _Val1 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Val0 SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val2 <- «incrAcc(_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq» _Val1 R
      return _Val2
    | _, _ => none
end