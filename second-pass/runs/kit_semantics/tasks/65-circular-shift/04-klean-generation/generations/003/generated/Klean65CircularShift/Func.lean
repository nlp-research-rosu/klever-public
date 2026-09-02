import Klean65CircularShift.Inj

def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

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

def _d9b4697 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _Gen0, 0 => some C
  | _, _ => none

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

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «Int2String(_)_STRING-COMMON_String_Int» (x0 : SortInt) : Option SortString

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

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
  def _24a45bb : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S, I => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» S _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  def «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_24a45bb x0 x1) <|> (_d9b4697 x0 x1)
end

def _2500272 : SortInt → SortInt → Option SortInt
  | J, _STEP => do
    let _Val0 <- «_>=Int_» J 0
    guard _Val0
    return J

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _ffe5f5d : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, _STEP => do
    let _Val0 <- «_<Int_» I LEN
    guard _Val0
    return I

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

mutual
  def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

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

def _2928123 : SortIntSeq → SortInt → SortInt → SortInt → Option SortIntSeq
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

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

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

def _3cc6493 : SortInt → SortInt → Option SortInt
  | J, STEP => do
    let _Val0 <- «_<Int_» J 0
    let _Val1 <- «_<Int_» STEP 0
    let _Val2 <- kite _Val1 (-1) 0
    guard _Val0
    return _Val2

def _6f49a32 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_>=Int_» I LEN
    let _Val1 <- «_<Int_» STEP 0
    let _Val2 <- «_-Int_» LEN 1
    let _Val3 <- kite _Val1 _Val2 LEN
    guard _Val0
    return _Val3

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

def «clampLo(_,_)_MPY-SUBSCRIPT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_2500272 x0 x1) <|> (_3cc6493 x0 x1)

def «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_6f49a32 x0 x1 x2) <|> (_ffe5f5d x0 x1 x2)

noncomputable def _8c15459 : SortInt → SortInt → Option SortStr
  | X, SHIFT => do
    let _Val0 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val1 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val0
    let _Val2 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val1
    let _Val3 <- «_>Int_» SHIFT _Val2
    let _Val4 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val5 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val4
    let _Val6 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val7 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val6
    let _Val8 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val7
    let _Val9 <- «_-Int_» _Val8 1
    let _Val10 <- «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» _Val5 _Val9 (-1) (-1)
    guard _Val3
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val10)

noncomputable def _bdfa641 : SortInt → SortInt → Option SortStr
  | X, SHIFT => do
    let _Val0 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val1 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val0
    let _Val2 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val1
    let _Val3 <- «_>Int_» SHIFT _Val2
    let _Val4 <- notBool_ _Val3
    let _Val5 <- «_<Int_» SHIFT 0
    let _Val6 <- _andBool_ _Val4 _Val5
    let _Val7 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val8 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val7
    guard _Val6
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val8)

def _e75deb6 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_+Int_» I LEN
    let _Val2 <- «clampLo(_,_)_MPY-SUBSCRIPT_Int_Int_Int» _Val1 STEP
    guard _Val0
    return _Val2

def _4b524a8 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» I LEN STEP
    guard _Val0
    return _Val1

def «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_4b524a8 x0 x1 x2) <|> (_e75deb6 x0 x1 x2)

noncomputable def _39757ff : SortInt → SortInt → Option SortStr
  | X, SHIFT => do
    let _Val0 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val1 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val0
    let _Val2 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val1
    let _Val3 <- «_>Int_» SHIFT _Val2
    let _Val4 <- notBool_ _Val3
    let _Val5 <- «_<Int_» SHIFT 0
    let _Val6 <- notBool_ _Val5
    let _Val7 <- _andBool_ _Val4 _Val6
    let _Val8 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val9 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val8
    let _Val10 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val11 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val10
    let _Val12 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» _Val9 _Val11
    let _Val13 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val14 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val13
    let _Val15 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val14
    let _Val16 <- «_-Int_» _Val15 SHIFT
    let _Val17 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val18 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val17
    let _Val19 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val20 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val19
    let _Val21 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» _Val18 _Val20
    let _Val22 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val21
    let _Val23 <- «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» _Val16 _Val22 1
    let _Val24 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val25 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val24
    let _Val26 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val25
    let _Val27 <- «_*Int_» 2 _Val26
    let _Val28 <- «_-Int_» _Val27 SHIFT
    let _Val29 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val30 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val29
    let _Val31 <- «Int2String(_)_STRING-COMMON_String_Int» X
    let _Val32 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val31
    let _Val33 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» _Val30 _Val32
    let _Val34 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val33
    let _Val35 <- «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» _Val28 _Val34 1
    let _Val36 <- «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» _Val12 _Val23 _Val35 1
    guard _Val7
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val36)

noncomputable def «circularShiftResult(_,_)_VERIFICATION_Str_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortStr := (_39757ff x0 x1) <|> (_8c15459 x0 x1) <|> (_bdfa641 x0 x1)