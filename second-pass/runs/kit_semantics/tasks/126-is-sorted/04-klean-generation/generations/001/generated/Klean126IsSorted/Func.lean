import Klean126IsSorted.Inj

def _0092bdb : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _0282aac : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _0433830 : SortVal → SortValSeq → Option SortVal
  | V, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some V
  | _, _ => none

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

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

def _c71764f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _f3f7875 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1 => some true
  | _, _ => none

def _571b6be : SortValSeq → Option SortBool
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _V _R => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _3614878 : SortVal → SortValSeq → Option SortVal
  | P, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some P
  | _, _ => none

def _7060751 : SortVal → SortInt → SortValSeq → Option SortInt
  | _P, C, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some C
  | _, _, _ => none

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

def _e0da4c3 : SortVal → SortInt → SortValSeq → Option SortBool
  | _P, _C, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _, _, _ => none

mutual
  def _8f62bce : SortVal → SortValSeq → Option SortVal
    | _V, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- «scanValue(_,_)_VERIFICATION_Val_Val_ValSeq» V R
      return _Val0
    | _, _ => none

  def «scanValue(_,_)_VERIFICATION_Val_Val_ValSeq» (x0 : SortVal) (x1 : SortValSeq) : Option SortVal := (_0433830 x0 x1) <|> (_8f62bce x0 x1)
end

def _cc09b1d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_>Int_» A B
    guard _Val0
    return false
  | _, _ => none

def _2c9e949 : SortInt → SortValSeq → Option SortValSeq
  | X, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt Y) R => do
    let _Val0 <- «_<=Int_» X Y
    guard _Val0
    return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) X) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) Y) R))
  | _, _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _c875e09 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_<Int_» A B
    guard _Val0
    return true
  | _, _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  def «scanPrevious(_,_)_VERIFICATION_Val_Val_ValSeq» (x0 : SortVal) (x1 : SortValSeq) : Option SortVal := (_3614878 x0 x1) <|> (_a9314ac x0 x1)

  def _a9314ac : SortVal → SortValSeq → Option SortVal
    | _P, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- «scanPrevious(_,_)_VERIFICATION_Val_Val_ValSeq» V R
      return _Val0
    | _, _ => none
end

noncomputable def _8bbbf3f : SortVal → SortInt → SortVal → Option SortInt
  | P, C, V => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) P) SortK.dotk)
    let _Val1 <- «_+Int_» C 1
    guard _Val0
    return _Val1

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

noncomputable def _294f0a5 : SortVal → SortInt → SortVal → Option SortInt
  | P, _C, V => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) P) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return 1

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
  def _23db3eb : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) R => do
      let _Val0 <- «_>=Int_» I 0
      let _Val1 <- «nonNegativeVals(_)_VERIFICATION_Bool_ValSeq» R
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «nonNegativeVals(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_0282aac x0) <|> (_23db3eb x0) <|> (_571b6be x0)
end

noncomputable def «nextRepeated(_,_,_)_VERIFICATION_Int_Val_Int_Val» (x0 : SortVal) (x1 : SortInt) (x2 : SortVal) : Option SortInt := (_294f0a5 x0 x1 x2) <|> (_8bbbf3f x0 x1 x2)

noncomputable def _ffbdc85 : SortIntSeq → SortValSeq → Option SortValSeq
  | A, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B)) R => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» A B
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) B) SortK.dotk)
    let _Val2 <- _orBool_ _Val0 _Val1
    guard _Val2
    return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B)) R))
  | _, _ => none

mutual
  noncomputable def _54d97e5 : SortVal → SortInt → SortValSeq → Option SortInt
    | P, C, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- «nextRepeated(_,_,_)_VERIFICATION_Int_Val_Int_Val» P C V
      let _Val1 <- «scanRepeated(_,_,_)_VERIFICATION_Int_Val_Int_ValSeq» V _Val0 R
      return _Val1
    | _, _, _ => none

  noncomputable def «scanRepeated(_,_,_)_VERIFICATION_Int_Val_Int_ValSeq» (x0 : SortVal) (x1 : SortInt) (x2 : SortValSeq) : Option SortInt := (_54d97e5 x0 x1 x2) <|> (_7060751 x0 x1 x2)
end

mutual
  noncomputable def «duplicateOK(_,_,_)_VERIFICATION_Bool_Val_Int_ValSeq» (x0 : SortVal) (x1 : SortInt) (x2 : SortValSeq) : Option SortBool := (_e0da4c3 x0 x1 x2) <|> (_e160836 x0 x1 x2)

  noncomputable def _e160836 : SortVal → SortInt → SortValSeq → Option SortBool
    | P, C, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- «nextRepeated(_,_,_)_VERIFICATION_Int_Val_Int_Val» P C V
      let _Val1 <- «_>Int_» _Val0 2
      let _Val2 <- notBool_ _Val1
      let _Val3 <- «nextRepeated(_,_,_)_VERIFICATION_Int_Val_Int_Val» P C V
      let _Val4 <- «duplicateOK(_,_,_)_VERIFICATION_Bool_Val_Int_ValSeq» V _Val3 R
      let _Val5 <- _andBool_ _Val2 _Val4
      return _Val5
    | _, _, _ => none
end

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

noncomputable def _cb24707 : SortVal → SortInt → SortBool → SortValSeq → Option SortBool
  | P, C, B, VS => do
    let _Val0 <- «duplicateOK(_,_,_)_VERIFICATION_Bool_Val_Int_ValSeq» P C VS
    let _Val1 <- _andBool_ B _Val0
    return _Val1

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

noncomputable def «scanDuplicates(_,_,_,_)_VERIFICATION_Bool_Val_Int_Bool_ValSeq» (x0 : SortVal) (x1 : SortInt) (x2 : SortBool) (x3 : SortValSeq) : Option SortBool := _cb24707 x0 x1 x2 x3

noncomputable def _f2edef5 : SortValSeq → Option SortBool
  | VS => do
    let _Val0 <- «nonNegativeVals(_)_VERIFICATION_Bool_ValSeq» VS
    let _Val1 <- sortVS VS
    let _Val2 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) VS) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) _Val1) SortK.dotk)
    let _Val3 <- «scanDuplicates(_,_,_,_)_VERIFICATION_Bool_Val_Int_Bool_ValSeq» ((@inj SortInt SortVal) (-1)) 0 true VS
    let _Val4 <- _andBool_ _Val2 _Val3
    guard _Val0
    return _Val4

noncomputable def «sortedWithAtMostTwo(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := _f2edef5 x0