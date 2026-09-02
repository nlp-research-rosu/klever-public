import Klean127Intersection.Inj

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

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

def _a6bbad9 : SortBool → SortInt → SortInt → Option SortBool
  | true, _N, _D => some true
  | _, _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
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

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def _f390a9b : SortString → SortString → Option SortBool
  | S1, S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    let _Val1 <- notBool_ _Val0
    return _Val1

def _ee259b5 : SortBool → SortInt → SortInt → Option SortBool
  | false, N, D => do
    let _Val0 <- «_>=Int_» D 2
    let _Val1 <- «_>=Int_» D N
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return false
  | _, _, _ => none

noncomputable def _40f59b7 : SortBool → SortInt → SortInt → Option SortBool
  | false, N, D => do
    let _Val0 <- «_>=Int_» D 2
    let _Val1 <- «_<Int_» D N
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N D
    let _Val4 <- «_==Int_» _Val3 0
    let _Val5 <- _andBool_ _Val2 _Val4
    guard _Val5
    return true
  | _, _, _ => none

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

def _8de9b3f : SortInt → SortInt → SortInt → SortInt → Option SortInt
  | A0, A1, B0, B1 => do
    let _Val0 <- «_<Int_» B1 A1
    let _Val1 <- kite _Val0 B1 A1
    let _Val2 <- «_>Int_» B0 A0
    let _Val3 <- kite _Val2 B0 A0
    let _Val4 <- «_-Int_» _Val1 _Val3
    return _Val4

axiom _6564535 : SortBool → SortInt → SortInt → Option SortBool
axiom «scanHasDivisor(_,_,_)_VERIFICATION-SYNTAX_Bool_Bool_Int_Int» (x0 : SortBool) (x1 : SortInt) (x2 : SortInt) : Option SortBool
axiom _b1f975d : SortBool → SortInt → SortInt → Option SortBool

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

def «overlapLength(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortInt := _8de9b3f x0 x1 x2 x3

noncomputable def _e203049 : SortInt → Option SortVal
  | N => do
    let _Val0 <- «_<Int_» N 2
    let _Val1 <- «scanHasDivisor(_,_,_)_VERIFICATION-SYNTAX_Bool_Bool_Int_Int» false N 2
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «strToCodes(_)_MPY-STR_IntSeq_String» "NO"
    let _Val4 <- «strToCodes(_)_MPY-STR_IntSeq_String» "YES"
    let _Val5 <- kite _Val2 (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val3) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val4)
    return ((@inj SortStr SortVal) _Val5)

noncomputable def «primeResult(_)_VERIFICATION-SYNTAX_Val_Int» (x0 : SortInt) : Option SortVal := _e203049 x0