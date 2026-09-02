import Klean113OddCount.Inj

axiom «_*Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

noncomputable def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

noncomputable def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «_^Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortFloat

noncomputable def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

noncomputable def _218dc3a : SortString → Option SortIntSeq
  | "" => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

noncomputable def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

axiom «_-Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «_/Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «floorFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

noncomputable def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

noncomputable def _5a819d8 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

noncomputable def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

noncomputable def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def _f69553d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

noncomputable def _4154192 : SortIntSeq → SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some 0
  | _, _ => none

noncomputable def _4183651 : SortIntSeq → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _, _ => none

noncomputable def _41a8e65 : SortVal → Option SortBool
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Gen0) => some true
  | _ => none

noncomputable def _4b7fd38 : SortBool → Option SortInt
  | false => some 0
  | _ => none

axiom «_^Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

noncomputable def _56c8f18 : SortValSeq → SortValSeq → Option SortValSeq
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some ACC
  | _, _ => none

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

noncomputable def _e321d7c : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

noncomputable def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

noncomputable def _73f627a : SortBool → Option SortInt
  | true => some 1
  | _ => none

noncomputable def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

noncomputable def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

axiom «_+Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «Int2String(_)_STRING-COMMON_String_Int» (x0 : SortInt) : Option SortString

axiom stringCodes (x0 : SortVal) : Option SortIntSeq

noncomputable def _ed6e9ce : SortVal → Option SortBool
  | _Gen0 => some false

noncomputable def _fabb789 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
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

noncomputable def _List_ (x0 : SortList) (x1 : SortList) : Option SortList := some ⟨x0.coll ++ x1.coll⟩

noncomputable def _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap :=
  if kleanMapDisjointModel x0.coll x1.coll then
    some ⟨x0.coll ++ x1.coll⟩
  else none

noncomputable def «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=
  some ⟨[(x0, x1)]⟩

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

noncomputable def _07c1bf0 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_*Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _13d6ee6 : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_*Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

noncomputable def _16468f1 : SortIntSeq → SortInt → Option SortIntSeq
  | S, N => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return S

noncomputable def _9daeaea : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_^Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _e5f1d08 : SortInt → Option SortFloat
  | I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    return _Val0

mutual
  noncomputable def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  noncomputable def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
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

mutual
  noncomputable def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  noncomputable def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

noncomputable def _bc844c7 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_+Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

noncomputable def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _4f03d42 : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_>=Int_» I2 0
    let _Val1 <- «_^Int_» I1 I2
    guard _Val0
    return ((@inj SortInt SortVal) _Val1)
  | _, _, _ => none

noncomputable def «boolAsInt(_)_MPY-CORE_Int_Bool» (x0 : SortBool) : Option SortInt := (_4b7fd38 x0) <|> (_73f627a x0)

mutual
  noncomputable def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  noncomputable def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

noncomputable def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def _614d946 : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_-Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

noncomputable def _dc1bc34 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_+Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def «isStringVal(_)_VERIFICATION-SYNTAX_Bool_Val» (x0 : SortVal) : Option SortBool := (_41a8e65 x0) <|> (_ed6e9ce x0)

noncomputable def mulF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _07c1bf0 x0 x1

mutual
  noncomputable def «dropIS(_,_)_MPY-METHODS_IntSeq_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortIntSeq := (_16468f1 x0 x1) <|> (_aa907da x0 x1) <|> (_4183651 x0 x1)

  noncomputable def _aa907da : SortIntSeq → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 R, N => do
      let _Val0 <- «_>Int_» N 0
      let _Val1 <- «_-Int_» N 1
      let _Val2 <- «dropIS(_,_)_MPY-METHODS_IntSeq_IntSeq_Int» R _Val1
      guard _Val0
      return _Val2
    | _, _ => none
end

noncomputable def powF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _9daeaea x0 x1

noncomputable def intToF (x0 : SortInt) : Option SortFloat := _e5f1d08 x0

noncomputable def subF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _fabe8f9 x0 x1

noncomputable def intFloatDiv (x0 : SortInt) (x1 : SortFloat) : Option SortFloat := _2b8c3d8 x0 x1

noncomputable def divFloatIntV (x0 : SortFloat) (x1 : SortInt) : Option SortFloat := _ca2a05d x0 x1

noncomputable def divF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _d8a2a0c x0 x1

noncomputable def divII (x0 : SortInt) (x1 : SortInt) : Option SortFloat := _edb22f9 x0 x1

noncomputable def floatMod (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _ea38624 x0 x1

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

noncomputable def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

noncomputable def _f390a9b : SortString → SortString → Option SortBool
  | S1, S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    let _Val1 <- notBool_ _Val0
    return _Val1

mutual
  noncomputable def _3a4bf2f : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  noncomputable def «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_3a4bf2f x0 x1) <|> (_5a819d8 x0 x1) <|> (_f69553d x0 x1)
end

noncomputable def _951deed : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_>=Int_» C 48
    let _Val1 <- «_<=Int_» C 57
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

noncomputable def _c2eab84 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» A B
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _, _, _ => none

noncomputable def _d40cfb4 : SortString → Option SortBool
  | OP => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» OP "+"
    let _Val1 <- «_==String__STRING-COMMON_Bool_String_String» OP "-"
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_==String__STRING-COMMON_Bool_String_String» OP "*"
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «_==String__STRING-COMMON_Bool_String_String» OP "/"
    let _Val6 <- _orBool_ _Val4 _Val5
    let _Val7 <- «_==String__STRING-COMMON_Bool_String_String» OP "//"
    let _Val8 <- _orBool_ _Val6 _Val7
    let _Val9 <- «_==String__STRING-COMMON_Bool_String_String» OP "%"
    let _Val10 <- _orBool_ _Val8 _Val9
    let _Val11 <- «_==String__STRING-COMMON_Bool_String_String» OP "**"
    let _Val12 <- _orBool_ _Val10 _Val11
    return _Val12

noncomputable def addF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _dc1bc34 x0 x1

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

noncomputable def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

axiom «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortInt
axiom _b153473 : SortIntSeq → SortIntSeq → Option SortInt
axiom _f1b90b3 : SortIntSeq → SortIntSeq → Option SortInt

noncomputable def «isDigitC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _951deed x0

noncomputable def «isArithOp(_)_MPY-CORE_Bool_String» (x0 : SortString) : Option SortBool := _d40cfb4 x0

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

noncomputable def _7ff1b9f : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortBool B, SortVal.inj_SortInt I => do
    let _Val0 <- kite B 1 0
    let _Val1 <- «_+Int_» _Val0 I
    return ((@inj SortInt SortVal) _Val1)
  | _, _, _ => none

noncomputable def _bb59890 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortInt I, SortVal.inj_SortBool B => do
    let _Val0 <- kite B 1 0
    let _Val1 <- «_+Int_» I _Val0
    return ((@inj SortInt SortVal) _Val1)
  | _, _, _ => none

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

noncomputable def _a57af57 : SortIntSeq → Option SortInt
  | CS => do
    let _Val0 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 49 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val1 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 51 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val2 <- «_+Int_» _Val0 _Val1
    let _Val3 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 53 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val4 <- «_+Int_» _Val2 _Val3
    let _Val5 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 55 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val6 <- «_+Int_» _Val4 _Val5
    let _Val7 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 57 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val8 <- «_+Int_» _Val6 _Val7
    return _Val8

mutual
  noncomputable def _59e9bba : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S => do
      let _Val0 <- «isDigitC(_)_MPY-METHODS_Bool_Int» C
      let _Val1 <- «allDigit(_)_MPY-METHODS_Bool_IntSeq» S
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  noncomputable def «allDigit(_)_MPY-METHODS_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_59e9bba x0) <|> (_e321d7c x0)
end

axiom _60e6213 : SortString → SortVal → SortVal → Option SortVal
axiom _6b2bff4 : SortString → SortVal → SortVal → Option SortVal
axiom _7346d9f : SortString → SortVal → SortVal → Option SortVal
axiom «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» (x0 : SortString) (x1 : SortVal) (x2 : SortVal) : Option SortVal
axiom _fc81955 : SortString → SortVal → SortVal → Option SortVal
axiom _ff208f3 : SortString → SortVal → SortVal → Option SortVal

noncomputable def «oddDigitCount(_)_VERIFICATION-SYNTAX_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := _a57af57 x0

mutual
  noncomputable def _96fb6b5 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «isStringVal(_)_VERIFICATION-SYNTAX_Bool_Val» V
      let _Val1 <- stringCodes V
      let _Val2 <- «allDigit(_)_MPY-METHODS_Bool_IntSeq» _Val1
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «allDigitStrings(_)_VERIFICATION-SYNTAX_Bool_ValSeq» REST
      let _Val5 <- _andBool_ _Val3 _Val4
      return _Val5
    | _ => none

  noncomputable def «allDigitStrings(_)_VERIFICATION-SYNTAX_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_96fb6b5 x0) <|> (_fabb789 x0)
end

noncomputable def _65660d5 : SortIntSeq → Option SortVal
  | CS => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "the number of odd elements "
    let _Val1 <- «oddDigitCount(_)_VERIFICATION-SYNTAX_Int_IntSeq» CS
    let _Val2 <- «Int2String(_)_STRING-COMMON_String_Int» _Val1
    let _Val3 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val2
    let _Val4 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0)) ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val3))
    let _Val5 <- «strToCodes(_)_MPY-STR_IntSeq_String» "n the str"
    let _Val6 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" _Val4 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val5))
    let _Val7 <- «oddDigitCount(_)_VERIFICATION-SYNTAX_Int_IntSeq» CS
    let _Val8 <- «Int2String(_)_STRING-COMMON_String_Int» _Val7
    let _Val9 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val8
    let _Val10 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" _Val6 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val9))
    let _Val11 <- «strToCodes(_)_MPY-STR_IntSeq_String» "ng "
    let _Val12 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" _Val10 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val11))
    let _Val13 <- «oddDigitCount(_)_VERIFICATION-SYNTAX_Int_IntSeq» CS
    let _Val14 <- «Int2String(_)_STRING-COMMON_String_Int» _Val13
    let _Val15 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val14
    let _Val16 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" _Val12 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val15))
    let _Val17 <- «strToCodes(_)_MPY-STR_IntSeq_String» " of the "
    let _Val18 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" _Val16 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val17))
    let _Val19 <- «oddDigitCount(_)_VERIFICATION-SYNTAX_Int_IntSeq» CS
    let _Val20 <- «Int2String(_)_STRING-COMMON_String_Int» _Val19
    let _Val21 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val20
    let _Val22 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" _Val18 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val21))
    let _Val23 <- «strToCodes(_)_MPY-STR_IntSeq_String» "nput."
    let _Val24 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" _Val22 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val23))
    return _Val24

noncomputable def «oddLine(_)_VERIFICATION-SYNTAX_Val_IntSeq» (x0 : SortIntSeq) : Option SortVal := _65660d5 x0

mutual
  noncomputable def _705d54d : SortValSeq → SortValSeq → Option SortValSeq
    | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- stringCodes V
      let _Val1 <- «oddLine(_)_VERIFICATION-SYNTAX_Val_IntSeq» _Val0
      let _Val2 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Val1 SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val3 <- «oddLinesAcc(_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_ValSeq» _Val2 REST
      return _Val3
    | _, _ => none

  noncomputable def «oddLinesAcc(_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_56c8f18 x0 x1) <|> (_705d54d x0 x1)
end