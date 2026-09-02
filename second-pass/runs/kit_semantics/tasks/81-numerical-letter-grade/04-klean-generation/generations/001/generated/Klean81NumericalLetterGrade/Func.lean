import Klean81NumericalLetterGrade.Inj

def _105572a : SortK → Option SortBool
  | K => some false

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _218dc3a : SortString → Option SortIntSeq
  | "" => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _613283e : SortK → Option SortBool
  | K => some false

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

axiom «_>Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «_==Float_» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortFloat

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

def _ca37525 : SortValSeq → SortValSeq → Option SortValSeq
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some ACC
  | _, _ => none

def _d74a36c : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortFloat Float) SortK.dotk => some true
  | _ => none

def _186a6e8 : SortValSeq → Option SortBool
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

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def _fee1f6e : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_>Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

noncomputable def _30697d0 : SortVal → SortFloat → Option SortBool
  | SortVal.inj_SortFloat G, F => do
    let _Val0 <- «_==Float_» G F
    return _Val0
  | _, _ => none

noncomputable def _3994b91 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0

noncomputable def _e5f1d08 : SortInt → Option SortFloat
  | I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    return _Val0

def isFloat (x0 : SortK) : Option SortBool := (_d74a36c x0) <|> (_613283e x0)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

noncomputable def _f390a9b : SortString → SortString → Option SortBool
  | S1, S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def gtF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _fee1f6e x0 x1

noncomputable def eqF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _3994b91 x0 x1

noncomputable def intToF (x0 : SortInt) : Option SortFloat := _e5f1d08 x0

def _8627818 : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val2 <- _orBool_ _Val0 _Val1
    return _Val2

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

noncomputable def _c474681 : SortVal → SortFloat → Option SortBool
  | SortVal.inj_SortFloat G, F => do
    let _Val0 <- gtF G F
    return _Val0
  | _, _ => none

noncomputable def _42dd0ae : SortVal → SortFloat → Option SortBool
  | SortVal.inj_SortInt I, F => do
    let _Val0 <- intToF I
    let _Val1 <- gtF _Val0 F
    return _Val1
  | _, _ => none

noncomputable def _9928554 : SortVal → SortFloat → Option SortBool
  | SortVal.inj_SortInt I, F => do
    let _Val0 <- intToF I
    let _Val1 <- eqF _Val0 F
    return _Val1
  | _, _ => none

def «isGradeNumber(_)_VERIFICATION_Bool_Val» (x0 : SortVal) : Option SortBool := _8627818 x0

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

def _2568117 : SortVal → SortFloat → Option SortBool
  | V, _Gen0 => do
    let _Val0 <- «isGradeNumber(_)_VERIFICATION_Bool_Val» V
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return false

mutual
  def «allGradeNumbers(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_186a6e8 x0) <|> (_ef0cc3c x0)

  def _ef0cc3c : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «isGradeNumber(_)_VERIFICATION_Bool_Val» V
      let _Val1 <- «allGradeNumbers(_)_VERIFICATION_Bool_ValSeq» REST
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none
end

def _d6c333f : SortVal → SortFloat → Option SortBool
  | V, _Gen0 => do
    let _Val0 <- «isGradeNumber(_)_VERIFICATION_Bool_Val» V
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return false

noncomputable def «gradeEq(_,_)_VERIFICATION_Bool_Val_Float» (x0 : SortVal) (x1 : SortFloat) : Option SortBool := (_2568117 x0 x1) <|> (_30697d0 x0 x1) <|> (_9928554 x0 x1)

noncomputable def «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» (x0 : SortVal) (x1 : SortFloat) : Option SortBool := (_42dd0ae x0 x1) <|> (_c474681 x0 x1) <|> (_d6c333f x0 x1)

noncomputable def _85065d6 : SortVal → Option SortVal
  | V => do
    let _Val0 <- «gradeEq(_,_)_VERIFICATION_Bool_Val_Float» V (4.0 : Float)
    let _Val1 <- «strToCodes(_)_MPY-STR_IntSeq_String» "A+"
    let _Val2 <- «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V (3.7 : Float)
    let _Val3 <- «strToCodes(_)_MPY-STR_IntSeq_String» "A"
    let _Val4 <- «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V (3.3 : Float)
    let _Val5 <- «strToCodes(_)_MPY-STR_IntSeq_String» "A-"
    let _Val6 <- «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V (3.0 : Float)
    let _Val7 <- «strToCodes(_)_MPY-STR_IntSeq_String» "B+"
    let _Val8 <- «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V (2.7 : Float)
    let _Val9 <- «strToCodes(_)_MPY-STR_IntSeq_String» "B"
    let _Val10 <- «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V (2.3 : Float)
    let _Val11 <- «strToCodes(_)_MPY-STR_IntSeq_String» "B-"
    let _Val12 <- «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V (2.0 : Float)
    let _Val13 <- «strToCodes(_)_MPY-STR_IntSeq_String» "C+"
    let _Val14 <- «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V (1.7 : Float)
    let _Val15 <- «strToCodes(_)_MPY-STR_IntSeq_String» "C"
    let _Val16 <- «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V (1.3 : Float)
    let _Val17 <- «strToCodes(_)_MPY-STR_IntSeq_String» "C-"
    let _Val18 <- «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V (1.0 : Float)
    let _Val19 <- «strToCodes(_)_MPY-STR_IntSeq_String» "D+"
    let _Val20 <- «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V (0.7 : Float)
    let _Val21 <- «strToCodes(_)_MPY-STR_IntSeq_String» "D"
    let _Val22 <- «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» V (0.0 : Float)
    let _Val23 <- «strToCodes(_)_MPY-STR_IntSeq_String» "D-"
    let _Val24 <- «strToCodes(_)_MPY-STR_IntSeq_String» "E"
    let _Val25 <- kite _Val22 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val23) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val24)
    let _Val26 <- kite _Val20 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val21) _Val25
    let _Val27 <- kite _Val18 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val19) _Val26
    let _Val28 <- kite _Val16 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val17) _Val27
    let _Val29 <- kite _Val14 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val15) _Val28
    let _Val30 <- kite _Val12 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val13) _Val29
    let _Val31 <- kite _Val10 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val11) _Val30
    let _Val32 <- kite _Val8 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val9) _Val31
    let _Val33 <- kite _Val6 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val7) _Val32
    let _Val34 <- kite _Val4 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val5) _Val33
    let _Val35 <- kite _Val2 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val3) _Val34
    let _Val36 <- kite _Val0 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val1) _Val35
    return ((@inj SortStr SortVal) _Val36)

noncomputable def «gradeValue(_)_VERIFICATION_Val_Val» (x0 : SortVal) : Option SortVal := _85065d6 x0

mutual
  noncomputable def _0b22f5e : SortValSeq → SortValSeq → Option SortValSeq
    | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «gradeValue(_)_VERIFICATION_Val_Val» V
      let _Val1 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Val0 SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val2 <- «gradeAcc(_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq» _Val1 REST
      return _Val2
    | _, _ => none

  noncomputable def «gradeAcc(_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_0b22f5e x0 x1) <|> (_ca37525 x0 x1)
end