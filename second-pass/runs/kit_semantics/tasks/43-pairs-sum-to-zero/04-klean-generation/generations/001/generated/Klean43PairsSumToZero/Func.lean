import Klean43PairsSumToZero.Inj

def _105572a : SortK → Option SortBool
  | K => some false

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _d0a8392 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

def _e4ff78f : SortValSeq → SortVal → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some 0
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _788d050 : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
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

def _bd296a8 : SortValSeq → SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _FULL => some false
  | _, _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

mutual
  def _01539d8 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» X REM => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) X) SortK.dotk)
      let _Val1 <- «allInts(_)_VERIFICATION_Bool_ValSeq» REM
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allInts(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_01539d8 x0) <|> (_d0a8392 x0)
end

mutual
  noncomputable def _2b96129 : SortValSeq → SortVal → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A R, V => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «cntOccVS(_,_)_MPY-METHODS_Int_ValSeq_Val» R V
      guard _Val1
      return _Val2
    | _, _ => none

  noncomputable def _8f0e06e : SortValSeq → SortVal → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A R, V => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «cntOccVS(_,_)_MPY-METHODS_Int_ValSeq_Val» R V
      let _Val2 <- «_+Int_» 1 _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  noncomputable def «cntOccVS(_,_)_MPY-METHODS_Int_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortInt := (_2b96129 x0 x1) <|> (_8f0e06e x0 x1) <|> (_e4ff78f x0 x1)
end

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def _769f569 : SortVal → Option SortInt
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return 0

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

def «intProj(_)_INT-PROJECTION_Int_Val» (x0 : SortVal) : Option SortInt := (_769f569 x0) <|> (_788d050 x0)

noncomputable def _656c469 : SortInt → SortValSeq → Option SortBool
  | X, FULL => do
    let _Val0 <- «_==Int_» X 0
    let _Val1 <- «cntOccVS(_,_)_MPY-METHODS_Int_ValSeq_Val» FULL ((@inj SortInt SortVal) 0)
    let _Val2 <- «_>Int_» _Val1 1
    let _Val3 <- _andBool_ _Val0 _Val2
    let _Val4 <- «_=/=Int_» X 0
    let _Val5 <- «_-Int_» 0 X
    let _Val6 <- «cntOccVS(_,_)_MPY-METHODS_Int_ValSeq_Val» FULL ((@inj SortInt SortVal) _Val5)
    let _Val7 <- «_>Int_» _Val6 0
    let _Val8 <- _andBool_ _Val4 _Val7
    let _Val9 <- _orBool_ _Val3 _Val8
    return _Val9

noncomputable def «hasInverse(_,_)_VERIFICATION_Bool_Int_ValSeq» (x0 : SortInt) (x1 : SortValSeq) : Option SortBool := _656c469 x0 x1

mutual
  noncomputable def «anyInverse(_,_)_VERIFICATION_Bool_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortBool := (_bd296a8 x0 x1) <|> (_d43717b x0 x1)

  noncomputable def _d43717b : SortValSeq → SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» X REM, FULL => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) X) SortK.dotk)
      let _Val1 <- «intProj(_)_INT-PROJECTION_Int_Val» X
      let _Val2 <- «hasInverse(_,_)_VERIFICATION_Bool_Int_ValSeq» _Val1 FULL
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «anyInverse(_,_)_VERIFICATION_Bool_ValSeq_ValSeq» REM FULL
      let _Val5 <- _orBool_ _Val3 _Val4
      return _Val5
    | _, _ => none
end