import Klean148Bf.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _218dc3a : SortString → Option SortIntSeq
  | "" => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

def _a66427b : SortValSeq → SortInt → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0, 0 => some V
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

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

mutual
  def _86fc1c7 : SortValSeq → SortInt → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S, I => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» S _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  def «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortVal := (_86fc1c7 x0 x1) <|> (_a66427b x0 x1)
end

noncomputable def _f390a9b : SortString → SortString → Option SortBool
  | S1, S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    let _Val1 <- notBool_ _Val0
    return _Val1

def _1c1496e : SortValSeq → SortInt → SortInt → SortInt → Option SortValSeq
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

def _8bae011 : SortInt → SortInt → Option SortValSeq
  | I, J => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_<Int_» J 0
    let _Val2 <- _orBool_ _Val0 _Val1
    guard _Val2
    return SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

axiom «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortValSeq
axiom _fefa459 : SortValSeq → SortInt → SortInt → SortInt → Option SortValSeq

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

noncomputable def _280e0cb : SortIntSeq → Option SortInt
  | P => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Saturn"
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val0) SortK.dotk)
    guard _Val1
    return 5

noncomputable def _5030168 : SortIntSeq → Option SortInt
  | P => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Uranus"
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val0) SortK.dotk)
    guard _Val1
    return 6

noncomputable def _5dc2328 : SortIntSeq → Option SortInt
  | P => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Mars"
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val0) SortK.dotk)
    guard _Val1
    return 3

noncomputable def _8e78748 : SortIntSeq → Option SortInt
  | P => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Mercury"
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val0) SortK.dotk)
    let _Val2 <- notBool_ _Val1
    let _Val3 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Venus"
    let _Val4 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val3) SortK.dotk)
    let _Val5 <- notBool_ _Val4
    let _Val6 <- _andBool_ _Val2 _Val5
    let _Val7 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Earth"
    let _Val8 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val7) SortK.dotk)
    let _Val9 <- notBool_ _Val8
    let _Val10 <- _andBool_ _Val6 _Val9
    let _Val11 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Mars"
    let _Val12 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val11) SortK.dotk)
    let _Val13 <- notBool_ _Val12
    let _Val14 <- _andBool_ _Val10 _Val13
    let _Val15 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Jupiter"
    let _Val16 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val15) SortK.dotk)
    let _Val17 <- notBool_ _Val16
    let _Val18 <- _andBool_ _Val14 _Val17
    let _Val19 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Saturn"
    let _Val20 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val19) SortK.dotk)
    let _Val21 <- notBool_ _Val20
    let _Val22 <- _andBool_ _Val18 _Val21
    let _Val23 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Uranus"
    let _Val24 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val23) SortK.dotk)
    let _Val25 <- notBool_ _Val24
    let _Val26 <- _andBool_ _Val22 _Val25
    let _Val27 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Neptune"
    let _Val28 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val27) SortK.dotk)
    let _Val29 <- notBool_ _Val28
    let _Val30 <- _andBool_ _Val26 _Val29
    guard _Val30
    return (-1)

noncomputable def _99e1ee7 : Option SortValSeq := do
  let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Mercury"
  let _Val1 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Venus"
  let _Val2 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Earth"
  let _Val3 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Mars"
  let _Val4 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Jupiter"
  let _Val5 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Saturn"
  let _Val6 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Uranus"
  let _Val7 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Neptune"
  return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val1)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val2)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val3)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val4)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val5)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val6)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val7)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))))))))

noncomputable def _d346603 : SortIntSeq → Option SortInt
  | P => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Jupiter"
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val0) SortK.dotk)
    guard _Val1
    return 4

noncomputable def _d449564 : SortIntSeq → Option SortInt
  | P => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Earth"
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val0) SortK.dotk)
    guard _Val1
    return 2

noncomputable def _ecef467 : SortIntSeq → Option SortInt
  | P => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Neptune"
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val0) SortK.dotk)
    guard _Val1
    return 7

noncomputable def _fbb7070 : SortIntSeq → Option SortInt
  | P => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Mercury"
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val0) SortK.dotk)
    guard _Val1
    return 0

noncomputable def _ffaaaa4 : SortIntSeq → Option SortInt
  | P => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Venus"
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) _Val0) SortK.dotk)
    guard _Val1
    return 1

noncomputable def planetValues_VERIFICATION_ValSeq : Option SortValSeq := _99e1ee7

noncomputable def «planetIndex(_)_VERIFICATION_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_280e0cb x0) <|> (_5030168 x0) <|> (_5dc2328 x0) <|> (_8e78748 x0) <|> (_d346603 x0) <|> (_d449564 x0) <|> (_ecef467 x0) <|> (_fbb7070 x0) <|> (_ffaaaa4 x0)

noncomputable def _2a6ed1e : SortInt → SortInt → Option SortValSeq
  | I, J => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «_>=Int_» J 0
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_>=Int_» I J
    let _Val4 <- _andBool_ _Val2 _Val3
    let _Val5 <- planetValues_VERIFICATION_ValSeq
    let _Val6 <- «_+Int_» J 1
    let _Val7 <- «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» _Val5 _Val6 I 1
    guard _Val4
    return _Val7

noncomputable def _ed9cf4e : SortInt → SortInt → Option SortValSeq
  | I, J => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «_>=Int_» J 0
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» I J
    let _Val4 <- _andBool_ _Val2 _Val3
    let _Val5 <- planetValues_VERIFICATION_ValSeq
    let _Val6 <- «_+Int_» I 1
    let _Val7 <- «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» _Val5 _Val6 J 1
    guard _Val4
    return _Val7

noncomputable def «betweenIndices(_,_)_VERIFICATION_ValSeq_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortValSeq := (_2a6ed1e x0 x1) <|> (_8bae011 x0 x1) <|> (_ed9cf4e x0 x1)

noncomputable def _26ba31c : SortIntSeq → SortIntSeq → Option SortValSeq
  | P1, P2 => do
    let _Val0 <- «planetIndex(_)_VERIFICATION_Int_IntSeq» P1
    let _Val1 <- «planetIndex(_)_VERIFICATION_Int_IntSeq» P2
    let _Val2 <- «betweenIndices(_,_)_VERIFICATION_ValSeq_Int_Int» _Val0 _Val1
    return _Val2

noncomputable def «betweenPlanets(_,_)_VERIFICATION_ValSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortValSeq := _26ba31c x0 x1