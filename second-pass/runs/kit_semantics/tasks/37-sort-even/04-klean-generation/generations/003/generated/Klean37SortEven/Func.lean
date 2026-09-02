import Klean37SortEven.Inj

def _0092bdb : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _49a8097 : SortValSeq → SortInt → SortVal → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, _Gen1 => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _, _, _ => none

def _fdfd33a : SortValSeq → SortInt → SortVal → Option SortValSeq
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S, 0, V => some (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S)
  | _, _, _ => none

def _611c5b2 : SortInt → SortValSeq → Option SortValSeq
  | X, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) X) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _4725bc2 : SortIntSeq → SortValSeq → Option SortValSeq
  | A, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _7e4861f : SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

noncomputable local instance : DecidableEq SortK :=
  Classical.typeDecidableEq SortK
noncomputable def «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool :=
  some (decide (x0 = x1))

def _c71764f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _f3f7875 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1 => some true
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _a66427b : SortValSeq → SortInt → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0, 0 => some V
  | _, _ => none

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

def _cc09b1d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_>Int_» A B
    guard _Val0
    return false
  | _, _ => none

def _c875e09 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_<Int_» A B
    guard _Val0
    return true
  | _, _ => none

def _ef1735c : SortValSeq → SortInt → SortVal → Option SortValSeq
  | VS, I, _Gen0 => do
    let _Val0 <- «_<Int_» I 0
    guard _Val0
    return VS

def _2c9e949 : SortInt → SortValSeq → Option SortValSeq
  | X, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt Y) R => do
    let _Val0 <- «_<=Int_» X Y
    guard _Val0
    return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) X) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) Y) R))
  | _, _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _19421b8 : SortValSeq → SortValSeq → SortInt → SortInt → Option SortValSeq
  | VS, _SORTED, I, STOP => do
    let _Val0 <- «_>=Int_» I STOP
    guard _Val0
    return VS

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

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

mutual
  def _5d69a53 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «vsLen(_)_MPY-CORE_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_5d69a53 x0) <|> (_b662ad7 x0)
end

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

mutual
  def _06c5fb7 : SortValSeq → SortInt → SortVal → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» W S, I, V => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «setVSAt(_,_,_)_MPY-CORE_ValSeq_ValSeq_Int_Val» S _Val1 V
      guard _Val0
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» W _Val2)
    | _, _, _ => none

  def «setVSAt(_,_,_)_MPY-CORE_ValSeq_ValSeq_Int_Val» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortVal) : Option SortValSeq := (_06c5fb7 x0 x1 x2) <|> (_49a8097 x0 x1 x2) <|> (_ef1735c x0 x1 x2) <|> (_fdfd33a x0 x1 x2)
end

mutual
  def _1422124 : SortInt → SortValSeq → Option SortValSeq
    | X, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt Y) R => do
      let _Val0 <- «_>Int_» X Y
      let _Val1 <- «insVS(_,_)_MPY-SORT_ValSeq_Int_ValSeq» X R
      guard _Val0
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) Y) _Val1)
    | _, _ => none

  def «insVS(_,_)_MPY-SORT_ValSeq_Int_ValSeq» (x0 : SortInt) (x1 : SortValSeq) : Option SortValSeq := (_1422124 x0 x1) <|> (_2c9e949 x0 x1) <|> (_611c5b2 x0 x1)
end

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

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

noncomputable def _ffbdc85 : SortIntSeq → SortValSeq → Option SortValSeq
  | A, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B)) R => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» A B
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) B) SortK.dotk)
    let _Val2 <- _orBool_ _Val0 _Val1
    guard _Val2
    return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B)) R))
  | _, _ => none

axiom «fillEven(_,_,_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_ValSeq_Int_Int» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortInt) (x3 : SortInt) : Option SortValSeq
axiom _a1c0ca1 : SortValSeq → SortValSeq → SortInt → SortInt → Option SortValSeq

axiom «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortValSeq
axiom _fefa459 : SortValSeq → SortInt → SortInt → SortInt → Option SortValSeq

noncomputable def _d6d21c7 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_+Int_» N 1
    let _Val1 <- «_+Int_» N 1
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val1 2
    let _Val3 <- «_-Int_» _Val0 _Val2
    let _Val4 <- «_/Int_» _Val3 2
    return _Val4

mutual
  noncomputable def _92629aa : SortIntSeq → SortValSeq → Option SortValSeq
    | A, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B)) R => do
      let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» A B
      let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) B) SortK.dotk)
      let _Val2 <- _orBool_ _Val0 _Val1
      let _Val3 <- notBool_ _Val2
      let _Val4 <- «insVSs(_,_)_MPY-SORT_ValSeq_IntSeq_ValSeq» A R
      guard _Val3
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B)) _Val4)
    | _, _ => none

  noncomputable def «insVSs(_,_)_MPY-SORT_ValSeq_IntSeq_ValSeq» (x0 : SortIntSeq) (x1 : SortValSeq) : Option SortValSeq := (_4725bc2 x0 x1) <|> (_92629aa x0 x1) <|> (_ffbdc85 x0 x1)
end

noncomputable def «evenCount(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : Option SortInt := _d6d21c7 x0

mutual
  noncomputable def _185c4a4 : SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) R => do
      let _Val0 <- sortVS R
      let _Val1 <- «insVSs(_,_)_MPY-SORT_ValSeq_IntSeq_ValSeq» CS _Val0
      return _Val1
    | _ => none

  noncomputable def _57346fe : SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt X) R => do
      let _Val0 <- sortVS R
      let _Val1 <- «insVS(_,_)_MPY-SORT_ValSeq_Int_ValSeq» X _Val0
      return _Val1
    | _ => none

  noncomputable def sortVS (x0 : SortValSeq) : Option SortValSeq := (_185c4a4 x0) <|> (_57346fe x0) <|> (_7e4861f x0)
end

noncomputable def _2dd8ed8 : SortValSeq → Option SortValSeq
  | VS => do
    let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
    let _Val1 <- «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» VS 0 _Val0 2
    let _Val2 <- sortVS _Val1
    let _Val3 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
    let _Val4 <- «evenCount(_)_VERIFICATION-SYNTAX_Int_Int» _Val3
    let _Val5 <- «fillEven(_,_,_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_ValSeq_Int_Int» VS _Val2 0 _Val4
    return _Val5

noncomputable def «sortEvenResult(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» (x0 : SortValSeq) : Option SortValSeq := _2dd8ed8 x0