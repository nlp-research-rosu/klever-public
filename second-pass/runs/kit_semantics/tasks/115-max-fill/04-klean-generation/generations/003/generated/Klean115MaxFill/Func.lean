import Klean115MaxFill.Inj

def _105572a : SortK → Option SortBool
  | K => some false

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5bd6926 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

def _9f02755 : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

def _b09dba7 : SortValSeq → SortVal → Option SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», PREV => some PREV
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _71b34c9 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

noncomputable local instance : DecidableEq SortK :=
  Classical.typeDecidableEq SortK
noncomputable def «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool :=
  some (decide (x0 = x1))

axiom maxFillRowVals (x0 : SortVal) : Option SortValSeq

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

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

axiom maxFillProjectInt (x0 : SortVal) : Option SortInt

def _d11ea27 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _fcbb2bd : SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _C => some 0
  | _, _ => none

def _0d89bcd : SortValSeq → SortInt → Option SortInt
  | _VS, C => do
    let _Val0 <- «_<=Int_» C 0
    guard _Val0
    return 0

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _3c4038f : SortValSeq → SortVal → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS, _PREV => do
      let _Val0 <- «finalRow(_,_)_MAX-FILL-SUMMARY_Val_ValSeq_Val» VS V
      return _Val0
    | _, _ => none

  def «finalRow(_,_)_MAX-FILL-SUMMARY_Val_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortVal := (_3c4038f x0 x1) <|> (_b09dba7 x0 x1)
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _91fd10f : SortVal → Option SortBool
  | V => do
    let _Val0 <- maxFillRowVals V
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortIterable SortKItem) (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» _Val0)) SortK.dotk)
    return _Val1

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

noncomputable def «isListVal(_)_MAX-FILL-SUMMARY_Bool_Val» (x0 : SortVal) : Option SortBool := _91fd10f x0

def _c982a02 : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

mutual
  noncomputable def «allBinary(_)_MAX-FILL-SUMMARY_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_71b34c9 x0) <|> (_b2401cf x0)

  noncomputable def _b2401cf : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- maxFillProjectInt V
      let _Val2 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortInt SortKItem) _Val1) SortK.dotk)
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- maxFillProjectInt V
      let _Val5 <- «_==Int_» _Val4 0
      let _Val6 <- maxFillProjectInt V
      let _Val7 <- «_==Int_» _Val6 1
      let _Val8 <- _orBool_ _Val5 _Val7
      let _Val9 <- _andBool_ _Val3 _Val8
      let _Val10 <- «allBinary(_)_MAX-FILL-SUMMARY_Bool_ValSeq» VS
      let _Val11 <- _andBool_ _Val9 _Val10
      return _Val11
    | _ => none
end

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def «definedProjectInt(_)_MAX-FILL-SUMMARY_Bool_Val» (x0 : SortVal) : Option SortBool := _c982a02 x0

mutual
  noncomputable def «allRows(_)_MAX-FILL-SUMMARY_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_d11ea27 x0) <|> (_f9e73fc x0)

  noncomputable def _f9e73fc : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- «isListVal(_)_MAX-FILL-SUMMARY_Bool_Val» V
      let _Val1 <- maxFillRowVals V
      let _Val2 <- «allBinary(_)_MAX-FILL-SUMMARY_Bool_ValSeq» _Val1
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «allRows(_)_MAX-FILL-SUMMARY_Bool_ValSeq» VS
      let _Val5 <- _andBool_ _Val3 _Val4
      return _Val5
    | _ => none
end

def _4865897 : SortVal → Option SortInt
  | SortVal.inj_SortBool B => do
    let _Val0 <- kite B 1 0
    return _Val0
  | _ => none

def «intOf(_)_MPY-BUILTINS_Int_Val» (x0 : SortVal) : Option SortInt := (_4865897 x0) <|> (_9f02755 x0)

mutual
  def _36cb354 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- «intOf(_)_MPY-BUILTINS_Int_Val» V
      let _Val1 <- «rowSum(_)_MAX-FILL-SUMMARY_Int_ValSeq» VS
      let _Val2 <- «_+Int_» _Val0 _Val1
      return _Val2
    | _ => none

  def «rowSum(_)_MAX-FILL-SUMMARY_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_36cb354 x0) <|> (_5bd6926 x0)
end

noncomputable def _4a49597 : SortValSeq → SortInt → Option SortInt
  | VS, C => do
    let _Val0 <- «_>Int_» C 0
    let _Val1 <- «rowSum(_)_MAX-FILL-SUMMARY_Int_ValSeq» VS
    let _Val2 <- «_+Int_» _Val1 C
    let _Val3 <- «_-Int_» _Val2 1
    let _Val4 <- «rowSum(_)_MAX-FILL-SUMMARY_Int_ValSeq» VS
    let _Val5 <- «_+Int_» _Val4 C
    let _Val6 <- «_-Int_» _Val5 1
    let _Val7 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val6 C
    let _Val8 <- «_-Int_» _Val3 _Val7
    let _Val9 <- «_/Int_» _Val8 C
    guard _Val0
    return _Val9

noncomputable def «bucketCost(_,_)_MAX-FILL-SUMMARY_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := (_0d89bcd x0 x1) <|> (_4a49597 x0 x1)

mutual
  noncomputable def «gridCost(_,_)_MAX-FILL-SUMMARY_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := (_a4a4f9d x0 x1) <|> (_fcbb2bd x0 x1)

  noncomputable def _a4a4f9d : SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS, C => do
      let _Val0 <- maxFillRowVals V
      let _Val1 <- «bucketCost(_,_)_MAX-FILL-SUMMARY_Int_ValSeq_Int» _Val0 C
      let _Val2 <- «gridCost(_,_)_MAX-FILL-SUMMARY_Int_ValSeq_Int» VS C
      let _Val3 <- «_+Int_» _Val1 _Val2
      return _Val3
    | _, _ => none
end