import Klean141FileNameCheck.Inj

noncomputable def _0092bdb : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

noncomputable def _076da9f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

noncomputable def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

noncomputable def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

noncomputable def _fd49342 : SortValSeq → SortVal → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some false
  | _, _ => none

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

noncomputable def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

noncomputable def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

noncomputable def _28a37d3 : SortOptInt → Option SortInt
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» S => some S
  | _ => none

noncomputable def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

noncomputable def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

noncomputable def _d9b4697 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _Gen0, 0 => some C
  | _, _ => none

noncomputable def _daab430 : SortOptInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» => some 1
  | _ => none

axiom «_==Float_» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortFloat

noncomputable def _218dc3a : SortString → Option SortIntSeq
  | "" => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

axiom «_>Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «_==Bool_» (x0 : SortBool) (x1 : SortBool) : Option SortBool

noncomputable def _4154192 : SortIntSeq → SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some 0
  | _, _ => none

noncomputable def _4183651 : SortIntSeq → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _, _ => none

axiom «_<Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

noncomputable def _4613fdc : SortValSeq → SortValSeq → SortValSeq → SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, _Gen1 => some true
  | _, _, _, _ => none

noncomputable def _80a1ae7 : SortInt → SortIntSeq → Option SortBool
  | _Gen0, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

noncomputable def _a66427b : SortValSeq → SortInt → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0, 0 => some V
  | _, _ => none

noncomputable def _b662ad7 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

noncomputable def _c71764f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

noncomputable def _f3f7875 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1 => some true
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

noncomputable def _03e60c5 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) B) SortK.dotk)
    return _Val0
  | _, _, _ => none

noncomputable def _220c8a2 : SortString → SortVal → SortVal → Option SortBool
  | "is", V, SortVal.«noneV_MPY-CORE_Val» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) SortVal.«noneV_MPY-CORE_Val») SortK.dotk)
    return _Val0
  | _, _, _ => none

noncomputable def _57afa07 : SortString → SortVal → SortVal → Option SortBool
  | "==", V, SortVal.«noneV_MPY-CORE_Val» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) SortVal.«noneV_MPY-CORE_Val») SortK.dotk)
    return _Val0
  | _, _, _ => none

noncomputable def _6b7e0d4 : SortString → SortVal → SortVal → Option SortBool
  | "==", _Pat0, _Pat1 => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» B) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) B) SortK.dotk)
      return _Val0
    | _, _ => none
  | _, _, _ => none

noncomputable def _78864a2 : SortValSeq → SortVal → Option SortBool
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A _Gen0, K => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
    guard _Val0
    return true
  | _, _ => none

noncomputable def _dbd242d : SortValSeq → SortValSeq → SortVal → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» B _Gen1, K => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
    guard _Val0
    return B
  | _, _, _ => none

noncomputable def _f64794f : SortString → SortVal → SortVal → Option SortBool
  | "==", _Pat0, _Pat1 => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» B) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) B) SortK.dotk)
      return _Val0
    | _, _ => none
  | _, _, _ => none

noncomputable def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _0ae23e4 : SortString → SortVal → SortVal → Option SortBool
  | ">=", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_>=Int_» I1 I2
    return _Val0
  | _, _, _ => none

noncomputable def _2500272 : SortInt → SortInt → Option SortInt
  | J, _STEP => do
    let _Val0 <- «_>=Int_» J 0
    guard _Val0
    return J

noncomputable def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _b37e75d : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_==Int_» I1 I2
    return _Val0
  | _, _, _ => none

noncomputable def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def _6b454b2 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_>Int_» I1 I2
    return _Val0
  | _, _, _ => none

noncomputable def _cc09b1d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_>Int_» A B
    guard _Val0
    return false
  | _, _ => none

noncomputable def _41490e6 : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_<Int_» I1 I2
    return _Val0
  | _, _, _ => none

noncomputable def _c875e09 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_<Int_» A B
    guard _Val0
    return true
  | _, _ => none

noncomputable def _ffe5f5d : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, _STEP => do
    let _Val0 <- «_<Int_» I LEN
    guard _Val0
    return I

mutual
  noncomputable def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  noncomputable def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

mutual
  noncomputable def _24a45bb : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S, I => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» S _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  noncomputable def «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_24a45bb x0 x1) <|> (_d9b4697 x0 x1)
end

noncomputable def «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» (x0 : SortOptInt) : Option SortInt := (_28a37d3 x0) <|> (_daab430 x0)

noncomputable def _16468f1 : SortIntSeq → SortInt → Option SortIntSeq
  | S, N => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return S

noncomputable def _1c34a14 : SortString → SortVal → SortVal → Option SortBool
  | "<=", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_<=Int_» I1 I2
    return _Val0
  | _, _, _ => none

noncomputable def _3994b91 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0

noncomputable def _b558675 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0
  | _, _, _ => none

noncomputable def _e5f1d08 : SortInt → Option SortFloat
  | I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    return _Val0

noncomputable def _fee1f6e : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_>Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

noncomputable def _9e5ad0c : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortBool B1, SortVal.inj_SortBool B2 => do
    let _Val0 <- «_==Bool_» B1 B2
    return _Val0
  | _, _, _ => none

noncomputable def _5667141 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_<Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

mutual
  noncomputable def _86fc1c7 : SortValSeq → SortInt → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S, I => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» S _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  noncomputable def «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortVal := (_86fc1c7 x0 x1) <|> (_a66427b x0 x1)
end

mutual
  noncomputable def _5d69a53 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  noncomputable def «vsLen(_)_MPY-CORE_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_5d69a53 x0) <|> (_b662ad7 x0)
end

mutual
  noncomputable def _07ab7bb : SortValSeq → SortVal → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A R, K => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» R K
      guard _Val1
      return _Val2
    | _, _ => none

  noncomputable def «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortBool := (_07ab7bb x0 x1) <|> (_78864a2 x0 x1) <|> (_fd49342 x0 x1)
end

noncomputable def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

noncomputable def _31fe72e : SortBool → SortBool → Option SortBool
  | B1, B2 => do
    let _Val0 <- «_==Bool_» B1 B2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def _57f520f : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) B) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _7a57b51 : SortString → SortVal → SortVal → Option SortBool
  | "!=", _Pat0, _Pat1 => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» B) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) B) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      return _Val1
    | _, _ => none
  | _, _, _ => none

noncomputable def _882c519 : SortString → SortVal → SortVal → Option SortBool
  | "!=", V, SortVal.«noneV_MPY-CORE_Val» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) SortVal.«noneV_MPY-CORE_Val») SortK.dotk)
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _9f9c54d : SortString → SortVal → SortVal → Option SortBool
  | "!=", _Pat0, _Pat1 => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» B) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) B) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      return _Val1
    | _, _ => none
  | _, _, _ => none

mutual
  noncomputable def «dGet(_,_,_)_MPY-DICT_Val_ValSeq_ValSeq_Val» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortVal) : Option SortVal := (_a22e93c x0 x1 x2) <|> (_dbd242d x0 x1 x2)

  noncomputable def _a22e93c : SortValSeq → SortValSeq → SortVal → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A KR, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 VR, K => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «dGet(_,_,_)_MPY-DICT_Val_ValSeq_ValSeq_Val» KR VR K
      guard _Val1
      return _Val2
    | _, _, _ => none
end

noncomputable def _c0092c8 : SortString → SortVal → SortVal → Option SortBool
  | "is not", V, SortVal.«noneV_MPY-CORE_Val» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) SortVal.«noneV_MPY-CORE_Val») SortK.dotk)
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _c91e9fa : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- «_==Float_» F1 F2
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

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

noncomputable def _1c1496e : SortValSeq → SortInt → SortInt → SortInt → Option SortValSeq
  | _Gen0, I, STOP, STEP => do
    let _Val0 <- «_>Int_» STEP 0
    let _Val1 <- «_<Int_» I STOP
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» STEP 0
    let _Val4 <- «_>Int_» I STOP
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    let _Val7 <- notBool_ _Val6
    guard _Val7
    return SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

noncomputable def _2928123 : SortIntSeq → SortInt → SortInt → SortInt → Option SortIntSeq
  | _Gen0, I, STOP, STEP => do
    let _Val0 <- «_>Int_» STEP 0
    let _Val1 <- «_<Int_» I STOP
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» STEP 0
    let _Val4 <- «_>Int_» I STOP
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    let _Val7 <- notBool_ _Val6
    guard _Val7
    return SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

mutual
  noncomputable def «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortBool := (_80a1ae7 x0 x1) <|> (_c27c6a9 x0 x1)

  noncomputable def _c27c6a9 : SortInt → SortIntSeq → Option SortBool
    | C, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H T => do
      let _Val0 <- «_==Int_» C H
      let _Val1 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C T
      let _Val2 <- _orBool_ _Val0 _Val1
      return _Val2
    | _, _ => none
end

mutual
  noncomputable def _6a28f31 : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      guard _Val0
      return _Val1
    | _, _ => none

  noncomputable def «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_0092bdb x0 x1) <|> (_6a28f31 x0 x1) <|> (_c71764f x0 x1) <|> (_c875e09 x0 x1) <|> (_cc09b1d x0 x1) <|> (_f3f7875 x0 x1)
end

noncomputable def _396b61d : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, _LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_>Int_» _Val0 0
    guard _Val1
    return 0
  | _, _, _ => none

noncomputable def _3cb3e9b : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_<Int_» _Val0 0
    let _Val2 <- «_-Int_» LEN 1
    guard _Val1
    return _Val2
  | _, _, _ => none

noncomputable def _6ddca9b : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, _LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_<Int_» _Val0 0
    guard _Val1
    return (-1)
  | _, _, _ => none

noncomputable def _72787fe : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_>Int_» _Val0 0
    guard _Val1
    return LEN
  | _, _, _ => none

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

noncomputable def eqF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _3994b91 x0 x1

noncomputable def intToF (x0 : SortInt) : Option SortFloat := _e5f1d08 x0

noncomputable def gtF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _fee1f6e x0 x1

noncomputable def floatLt (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _5667141 x0 x1

noncomputable def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def «_=/=Bool_» (x0 : SortBool) (x1 : SortBool) : Option SortBool := _31fe72e x0 x1

noncomputable def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

mutual
  noncomputable def «dSubset(_,_,_,_)_MPY-DICT_Bool_ValSeq_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortValSeq) (x3 : SortValSeq) : Option SortBool := (_4613fdc x0 x1 x2 x3) <|> (_e2b14d5 x0 x1 x2 x3)

  noncomputable def _e2b14d5 : SortValSeq → SortValSeq → SortValSeq → SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» K KR, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VR, KS2, VS2 => do
      let _Val0 <- «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» KS2 K
      let _Val1 <- «dGet(_,_,_)_MPY-DICT_Val_ValSeq_ValSeq_Val» KS2 VS2 K
      let _Val2 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) _Val1) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «dSubset(_,_,_,_)_MPY-DICT_Bool_ValSeq_ValSeq_ValSeq_ValSeq» KR VR KS2 VS2
      let _Val5 <- _andBool_ _Val3 _Val4
      return _Val5
    | _, _, _, _ => none
end

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

noncomputable def _38142ad : SortIntSeq → SortIntSeq → Option SortBool
  | P, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => do
    let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return false
  | _, _ => none

noncomputable def _56a27c9 : SortIntSeq → SortIntSeq → Option SortBool
  | P, X => do
    let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P X
    guard _Val0
    return true

axiom «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortValSeq
axiom _fefa459 : SortValSeq → SortInt → SortInt → SortInt → Option SortValSeq

private def kleanIntSeqLengthModel : SortIntSeq → Nat
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      kleanIntSeqLengthModel rest + 1

private def kleanIntSeqAtNatModel : SortIntSeq → Nat → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» value _, 0 =>
      some value
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest, index + 1 =>
      kleanIntSeqAtNatModel rest index
  | _, _ => none

private def kleanIntSeqAtModel
    (input : SortIntSeq) (index : SortInt) : Option SortInt :=
  if index < 0 then none else kleanIntSeqAtNatModel input index.toNat

private def kleanBuildISContinueModel
    (index stop step : SortInt) : Bool :=
  (step > 0 && index < stop) || (step < 0 && index > stop)

private def kleanBuildISFuelModel :
    Nat → SortIntSeq → SortInt → SortInt → SortInt → Option SortIntSeq
  | 0, _, index, stop, step =>
      if kleanBuildISContinueModel index stop step then none
      else some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | fuel + 1, input, index, stop, step =>
      if kleanBuildISContinueModel index stop step then
        match kleanIntSeqAtModel input index with
        | none => none
        | some value =>
            match kleanBuildISFuelModel fuel input (index + step) stop step with
            | none => none
            | some rest =>
                some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                  value rest)
      else some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

private def kleanBuildISModel
    (x0 : SortIntSeq) (x1 x2 x3 : SortInt) : Option SortIntSeq :=
  kleanBuildISFuelModel (kleanIntSeqLengthModel x0 + 1) x0 x1 x2 x3

noncomputable def _5bd0f09 :
    SortIntSeq → SortInt → SortInt → SortInt → Option SortIntSeq :=
  kleanBuildISModel

noncomputable def «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int»
    (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) :
    Option SortIntSeq :=
  kleanBuildISModel x0 x1 x2 x3

mutual
  noncomputable def _9bcb96b : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S, B => do
      let _Val0 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C B
      let _Val1 <- «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» S B
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  noncomputable def «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_076da9f x0 x1) <|> (_9bcb96b x0 x1)
end

noncomputable def _758418c : SortString → SortVal → SortVal → Option SortBool
  | ">=", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» A B
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _8a4564e : SortString → SortVal → SortVal → Option SortBool
  | "<=", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» B A
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _9b4e435 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» B A
    return _Val0
  | _, _, _ => none

noncomputable def _f10cf1b : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» A B
    return _Val0
  | _, _, _ => none

axiom «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortInt
axiom _b153473 : SortIntSeq → SortIntSeq → Option SortInt
axiom _f1b90b3 : SortIntSeq → SortIntSeq → Option SortInt

noncomputable def _1eb1e83 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- eqF _Val0 F
    return _Val1
  | _, _, _ => none

noncomputable def _31a7ce9 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- eqF F _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _9ec2057 : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- eqF _Val0 F
    let _Val2 <- notBool_ _Val1
    return _Val2
  | _, _, _ => none

noncomputable def _b076352 : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- eqF F _Val0
    let _Val2 <- notBool_ _Val1
    return _Val2
  | _, _, _ => none

noncomputable def _21c3768 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- gtF F _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _3762d3f : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- gtF F1 F2
    return _Val0
  | _, _, _ => none

noncomputable def _641b30a : SortString → SortVal → SortVal → Option SortBool
  | "<=", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- gtF F1 F2
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _f5cd646 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- gtF _Val0 F
    return _Val1
  | _, _, _ => none

noncomputable def _42db81d : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- floatLt _Val0 F
    return _Val1
  | _, _, _ => none

noncomputable def _b69f73f : SortString → SortVal → SortVal → Option SortBool
  | ">=", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- floatLt F1 F2
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _beb7b49 : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- floatLt F _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _f53e67b : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- floatLt F1 F2
    return _Val0
  | _, _, _ => none

noncomputable def _3cc6493 : SortInt → SortInt → Option SortInt
  | J, STEP => do
    let _Val0 <- «_<Int_» J 0
    let _Val1 <- «_<Int_» STEP 0
    let _Val2 <- kite _Val1 (-1) 0
    guard _Val0
    return _Val2

noncomputable def _6f49a32 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_>=Int_» I LEN
    let _Val1 <- «_<Int_» STEP 0
    let _Val2 <- «_-Int_» LEN 1
    let _Val3 <- kite _Val1 _Val2 LEN
    guard _Val0
    return _Val3

noncomputable def _7031c92 : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortBool B1, SortVal.inj_SortBool B2 => do
    let _Val0 <- «_=/=Bool_» B1 B2
    return _Val0
  | _, _, _ => none

noncomputable def _c986c4d : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_=/=Int_» I1 I2
    return _Val0
  | _, _, _ => none

noncomputable def _9a8a33a : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» KS1 VS1, SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» KS2 VS2 => do
    let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» KS1
    let _Val1 <- «vsLen(_)_MPY-CORE_Int_ValSeq» KS2
    let _Val2 <- «_==Int_» _Val0 _Val1
    let _Val3 <- «dSubset(_,_,_,_)_MPY-DICT_Bool_ValSeq_ValSeq_ValSeq_ValSeq» KS1 VS1 KS2 VS2
    let _Val4 <- _andBool_ _Val2 _Val3
    return _Val4
  | _, _, _ => none

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

mutual
  noncomputable def «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_38142ad x0 x1) <|> (_56a27c9 x0 x1) <|> (_e133ba2 x0 x1)

  noncomputable def _e133ba2 : SortIntSeq → SortIntSeq → Option SortBool
    | P, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C Xs => do
      let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C Xs)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P Xs
      guard _Val1
      return _Val2
    | _, _ => none
end

noncomputable def _d3d248d : SortIntSeq → SortIntSeq → Option SortBool
  | A, B => do
    let _Val0 <- «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» A B
    let _Val1 <- «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» B A
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

noncomputable def «clampLo(_,_)_MPY-SUBSCRIPT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_2500272 x0 x1) <|> (_3cc6493 x0 x1)

noncomputable def «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_6f49a32 x0 x1 x2) <|> (_ffe5f5d x0 x1 x2)

noncomputable def _b19e075 : SortIntSeq → Option SortInt
  | CS => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "0"
    let _Val1 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS _Val0
    let _Val2 <- «strToCodes(_)_MPY-STR_IntSeq_String» "1"
    let _Val3 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS _Val2
    let _Val4 <- «_+Int_» _Val1 _Val3
    let _Val5 <- «strToCodes(_)_MPY-STR_IntSeq_String» "2"
    let _Val6 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS _Val5
    let _Val7 <- «_+Int_» _Val4 _Val6
    let _Val8 <- «strToCodes(_)_MPY-STR_IntSeq_String» "3"
    let _Val9 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS _Val8
    let _Val10 <- «_+Int_» _Val7 _Val9
    let _Val11 <- «strToCodes(_)_MPY-STR_IntSeq_String» "4"
    let _Val12 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS _Val11
    let _Val13 <- «_+Int_» _Val10 _Val12
    let _Val14 <- «strToCodes(_)_MPY-STR_IntSeq_String» "5"
    let _Val15 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS _Val14
    let _Val16 <- «_+Int_» _Val13 _Val15
    let _Val17 <- «strToCodes(_)_MPY-STR_IntSeq_String» "6"
    let _Val18 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS _Val17
    let _Val19 <- «_+Int_» _Val16 _Val18
    let _Val20 <- «strToCodes(_)_MPY-STR_IntSeq_String» "7"
    let _Val21 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS _Val20
    let _Val22 <- «_+Int_» _Val19 _Val21
    let _Val23 <- «strToCodes(_)_MPY-STR_IntSeq_String» "8"
    let _Val24 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS _Val23
    let _Val25 <- «_+Int_» _Val22 _Val24
    let _Val26 <- «strToCodes(_)_MPY-STR_IntSeq_String» "9"
    let _Val27 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS _Val26
    let _Val28 <- «_+Int_» _Val25 _Val27
    return _Val28

noncomputable def _0d7d6b1 : SortString → SortVal → SortVal → Option SortBool
  | "not in", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» P), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» X) => do
    let _Val0 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P X
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _9d30e79 : SortString → SortVal → SortVal → Option SortBool
  | "in", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» P), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» X) => do
    let _Val0 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P X
    return _Val0
  | _, _, _ => none

noncomputable def «sameSet(_,_)_MPY-SET_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := _d3d248d x0 x1

noncomputable def _e75deb6 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_+Int_» I LEN
    let _Val2 <- «clampLo(_,_)_MPY-SUBSCRIPT_Int_Int_Int» _Val1 STEP
    guard _Val0
    return _Val2

noncomputable def _4b524a8 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» I LEN STEP
    guard _Val0
    return _Val1

noncomputable def «decimalDigitCount(_)_VERIFICATION_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := _b19e075 x0

noncomputable def _87bf7c6 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.«setV(_)_MPY-SET_Val_IntSeq» A, SortVal.«setV(_)_MPY-SET_Val_IntSeq» B => do
    let _Val0 <- «sameSet(_,_)_MPY-SET_Bool_IntSeq_IntSeq» A B
    return _Val0
  | _, _, _ => none

noncomputable def «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_4b524a8 x0 x1 x2) <|> (_e75deb6 x0 x1 x2)

noncomputable def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» (x0 : SortString) (x1 : SortVal) (x2 : SortVal) : Option SortBool := (_03e60c5 x0 x1 x2) <|> (_0ae23e4 x0 x1 x2) <|> (_0d7d6b1 x0 x1 x2) <|> (_1c34a14 x0 x1 x2) <|> (_1eb1e83 x0 x1 x2) <|> (_21c3768 x0 x1 x2) <|> (_21c3768 x0 x1 x2) <|> (_220c8a2 x0 x1 x2) <|> (_31a7ce9 x0 x1 x2) <|> (_3762d3f x0 x1 x2) <|> (_41490e6 x0 x1 x2) <|> (_42db81d x0 x1 x2) <|> (_42db81d x0 x1 x2) <|> (_57afa07 x0 x1 x2) <|> (_57f520f x0 x1 x2) <|> (_641b30a x0 x1 x2) <|> (_6b454b2 x0 x1 x2) <|> (_6b7e0d4 x0 x1 x2) <|> (_7031c92 x0 x1 x2) <|> (_758418c x0 x1 x2) <|> (_7a57b51 x0 x1 x2) <|> (_87bf7c6 x0 x1 x2) <|> (_882c519 x0 x1 x2) <|> (_8a4564e x0 x1 x2) <|> (_9a8a33a x0 x1 x2) <|> (_9b4e435 x0 x1 x2) <|> (_9d30e79 x0 x1 x2) <|> (_9e5ad0c x0 x1 x2) <|> (_9ec2057 x0 x1 x2) <|> (_9f9c54d x0 x1 x2) <|> (_b076352 x0 x1 x2) <|> (_b37e75d x0 x1 x2) <|> (_b558675 x0 x1 x2) <|> (_b69f73f x0 x1 x2) <|> (_beb7b49 x0 x1 x2) <|> (_beb7b49 x0 x1 x2) <|> (_c0092c8 x0 x1 x2) <|> (_c91e9fa x0 x1 x2) <|> (_c986c4d x0 x1 x2) <|> (_f10cf1b x0 x1 x2) <|> (_f53e67b x0 x1 x2) <|> (_f5cd646 x0 x1 x2) <|> (_f5cd646 x0 x1 x2) <|> (_f64794f x0 x1 x2)

noncomputable def _4ae8014 : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» I, ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» I LEN _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _e2e4c93 : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» I, ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» I LEN _Val0
    return _Val1
  | _, _, _ => none

noncomputable def «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» (x0 : SortOptInt) (x1 : SortOptInt) (x2 : SortInt) : Option SortInt := (_396b61d x0 x1 x2) <|> (_3cb3e9b x0 x1 x2) <|> (_4ae8014 x0 x1 x2)

noncomputable def «slStop(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» (x0 : SortOptInt) (x1 : SortOptInt) (x2 : SortInt) : Option SortInt := (_6ddca9b x0 x1 x2) <|> (_72787fe x0 x1 x2) <|> (_e2e4c93 x0 x1 x2)

noncomputable def _13a7bb3 : SortVal → SortOptInt → SortOptInt → SortOptInt → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» IS), LO, HI, ST => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    let _Val1 <- «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» LO ST _Val0
    let _Val2 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    let _Val3 <- «slStop(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» HI ST _Val2
    let _Val4 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val5 <- «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» IS _Val1 _Val3 _Val4
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val5))
  | _, _, _, _ => none

noncomputable def _84f67ef : SortVal → SortOptInt → SortOptInt → SortOptInt → Option SortVal
  | _Pat0, LO, HI, ST => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      let _Val1 <- «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» LO ST _Val0
      let _Val2 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      let _Val3 <- «slStop(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» HI ST _Val2
      let _Val4 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
      let _Val5 <- «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» VS _Val1 _Val3 _Val4
      return ((@inj SortIterable SortVal) (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» _Val5))
    | _ => none

noncomputable def _8f16e60 : SortVal → SortOptInt → SortOptInt → SortOptInt → Option SortVal
  | _Pat0, LO, HI, ST => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      let _Val1 <- «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» LO ST _Val0
      let _Val2 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      let _Val3 <- «slStop(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» HI ST _Val2
      let _Val4 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
      let _Val5 <- «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» VS _Val1 _Val3 _Val4
      return ((@inj SortIterable SortVal) (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» _Val5))
    | _ => none

noncomputable def «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» (x0 : SortVal) (x1 : SortOptInt) (x2 : SortOptInt) (x3 : SortOptInt) : Option SortVal := (_13a7bb3 x0 x1 x2 x3) <|> (_84f67ef x0 x1 x2 x3) <|> (_8f16e60 x0 x1 x2 x3)

noncomputable def _e83faf0 : SortIntSeq → SortIntSeq → Option SortBool
  | CS, EXT => do
    let _Val0 <- «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» (-4)) SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
    let _Val1 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "==" _Val0 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» EXT))
    return _Val1

noncomputable def «fileExtensionIs(_,_)_VERIFICATION_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := _e83faf0 x0 x1

noncomputable def _4774a66 : SortIntSeq → Option SortBool
  | CS => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» ".txt"
    let _Val1 <- «fileExtensionIs(_,_)_VERIFICATION_Bool_IntSeq_IntSeq» CS _Val0
    let _Val2 <- «strToCodes(_)_MPY-STR_IntSeq_String» ".exe"
    let _Val3 <- «fileExtensionIs(_,_)_VERIFICATION_Bool_IntSeq_IntSeq» CS _Val2
    let _Val4 <- _orBool_ _Val1 _Val3
    let _Val5 <- «strToCodes(_)_MPY-STR_IntSeq_String» ".dll"
    let _Val6 <- «fileExtensionIs(_,_)_VERIFICATION_Bool_IntSeq_IntSeq» CS _Val5
    let _Val7 <- _orBool_ _Val4 _Val6
    return _Val7

noncomputable def «allowedFileExtension(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := _4774a66 x0