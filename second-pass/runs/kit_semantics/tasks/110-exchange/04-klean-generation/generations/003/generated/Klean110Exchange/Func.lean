import Klean110Exchange.Inj

def _08986cc : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

def _105572a : SortK → Option SortBool
  | K => some false

def _495da55 : SortK → Option SortBool
  | K => some false

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

def _d74a36c : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortFloat Float) SortK.dotk => some true
  | _ => none

def _dadad71 : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortBool Bool) SortK.dotk => some true
  | _ => none

def _f7d278b : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _218dc3a : SortString → Option SortIntSeq
  | "" => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

def _3fe3617 : SortBool → Option SortInt
  | true => some 1
  | _ => none

axiom «_-Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «_==Float_» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

axiom «_/Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «_*Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «floorFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

axiom projectBoolTotal (x0 : SortVal) : Option SortBool

axiom projectFloatTotal (x0 : SortVal) : Option SortFloat

axiom projectIntTotal (x0 : SortVal) : Option SortInt

def _fc90a9d : SortBool → Option SortInt
  | false => some 0
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

def _b662ad7 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
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

def «evenCount(_)_VERIFICATION-BASE_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := _08986cc x0

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def isFloat (x0 : SortK) : Option SortBool := (_d74a36c x0) <|> (_613283e x0)

def isBool (x0 : SortK) : Option SortBool := (_dadad71 x0) <|> (_495da55 x0)

noncomputable def _3994b91 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

noncomputable def _ea38624 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_/Float__FLOAT_Float_Float_Float» F1 F2
    let _Val1 <- «floorFloat(_)_FLOAT_Float_Float» _Val0
    let _Val2 <- «_*Float__FLOAT_Float_Float_Float» _Val1 F2
    let _Val3 <- «_-Float__FLOAT_Float_Float_Float» F1 _Val2
    return _Val3

def «boolToInt(_)_VERIFICATION-BASE_Int_Bool» (x0 : SortBool) : Option SortInt := (_3fe3617 x0) <|> (_fc90a9d x0)

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

def _352f4fa : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

def _6fad340 : SortVal → Option SortBool
  | V => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

def _4f681f3 : SortVal → Option SortBool
  | V => do
    let _Val0 <- isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

noncomputable def eqF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _3994b91 x0 x1

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

noncomputable def floatMod (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _ea38624 x0 x1

noncomputable def _f390a9b : SortString → SortString → Option SortBool
  | S1, S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «definedProjectInt(_)_VERIFICATION-BASE_Bool_Val» (x0 : SortVal) : Option SortBool := _352f4fa x0

def «definedProjectFloat(_)_VERIFICATION-BASE_Bool_Val» (x0 : SortVal) : Option SortBool := _6fad340 x0

def «definedProjectBool(_)_VERIFICATION-BASE_Bool_Val» (x0 : SortVal) : Option SortBool := _4f681f3 x0

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

noncomputable def _250687b : SortVal → Option SortBool
  | V => do
    let _Val0 <- «definedProjectInt(_)_VERIFICATION-BASE_Bool_Val» V
    let _Val1 <- projectIntTotal V
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val1 2
    let _Val3 <- «_==Int_» _Val2 0
    let _Val4 <- _andBool_ _Val0 _Val3
    let _Val5 <- «definedProjectBool(_)_VERIFICATION-BASE_Bool_Val» V
    let _Val6 <- projectBoolTotal V
    let _Val7 <- «boolToInt(_)_VERIFICATION-BASE_Int_Bool» _Val6
    let _Val8 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val7 2
    let _Val9 <- «_==Int_» _Val8 0
    let _Val10 <- _andBool_ _Val5 _Val9
    let _Val11 <- _orBool_ _Val4 _Val10
    let _Val12 <- «definedProjectFloat(_)_VERIFICATION-BASE_Bool_Val» V
    let _Val13 <- projectFloatTotal V
    let _Val14 <- floatMod _Val13 (2.0 : Float)
    let _Val15 <- eqF _Val14 (0.0 : Float)
    let _Val16 <- _andBool_ _Val12 _Val15
    let _Val17 <- _orBool_ _Val11 _Val16
    return _Val17

def _c974839 : SortVal → Option SortBool
  | V => do
    let _Val0 <- «definedProjectInt(_)_VERIFICATION-BASE_Bool_Val» V
    let _Val1 <- «definedProjectBool(_)_VERIFICATION-BASE_Bool_Val» V
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «definedProjectFloat(_)_VERIFICATION-BASE_Bool_Val» V
    let _Val4 <- _orBool_ _Val2 _Val3
    return _Val4

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

noncomputable def «numberEven(_)_VERIFICATION-BASE_Bool_Val» (x0 : SortVal) : Option SortBool := _250687b x0

def «isNumberVal(_)_VERIFICATION-BASE_Bool_Val» (x0 : SortVal) : Option SortBool := _c974839 x0

noncomputable def _457c7b9 : SortValSeq → SortValSeq → Option SortStr
  | VS1, VS2 => do
    let _Val0 <- «evenCount(_)_VERIFICATION-BASE_Int_ValSeq» VS1
    let _Val1 <- «evenCount(_)_VERIFICATION-BASE_Int_ValSeq» VS2
    let _Val2 <- «_+Int_» _Val0 _Val1
    let _Val3 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS1
    let _Val4 <- «_>=Int_» _Val2 _Val3
    let _Val5 <- «strToCodes(_)_MPY-STR_IntSeq_String» "YES"
    guard _Val4
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val5)

noncomputable def _632fef6 : SortValSeq → SortValSeq → Option SortStr
  | VS1, VS2 => do
    let _Val0 <- «evenCount(_)_VERIFICATION-BASE_Int_ValSeq» VS1
    let _Val1 <- «evenCount(_)_VERIFICATION-BASE_Int_ValSeq» VS2
    let _Val2 <- «_+Int_» _Val0 _Val1
    let _Val3 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS1
    let _Val4 <- «_<Int_» _Val2 _Val3
    let _Val5 <- «strToCodes(_)_MPY-STR_IntSeq_String» "NO"
    guard _Val4
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val5)

mutual
  def _0ebcdca : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- «isNumberVal(_)_VERIFICATION-BASE_Bool_Val» V
      let _Val1 <- «allNumbers(_)_VERIFICATION-BASE_Bool_ValSeq» VS
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allNumbers(_)_VERIFICATION-BASE_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_0ebcdca x0) <|> (_f7d278b x0)
end

noncomputable def «exchangeResult(_,_)_VERIFICATION-BASE_Str_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortStr := (_457c7b9 x0 x1) <|> (_632fef6 x0 x1)