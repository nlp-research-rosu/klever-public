import Klean85Add.Inj

def _105572a : SortK → Option SortBool
  | K => some false

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _7d47044 : SortValSeq → SortBool → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some 0
  | _, _ => none

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

axiom projectIntTotal (x0 : SortVal) : Option SortInt

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
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

def _e2c5587 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

mutual
  def «allInts(_)_VERIFICATION-SYNTAX_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_a540c70 x0) <|> (_e2c5587 x0)

  def _a540c70 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allInts(_)_VERIFICATION-SYNTAX_Bool_ValSeq» VS
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none
end

def _c73d4a8 : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» (x0 : SortVal) : Option SortBool := _c73d4a8 x0

mutual
  noncomputable def _23b69ae : SortValSeq → SortBool → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS, true => do
      let _Val0 <- projectIntTotal V
      let _Val1 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val0 2
      let _Val2 <- «_==Int_» _Val1 0
      let _Val3 <- projectIntTotal V
      let _Val4 <- kite _Val2 _Val3 0
      let _Val5 <- «addSummary(_,_)_VERIFICATION-SYNTAX_Int_ValSeq_Bool» VS false
      let _Val6 <- «_+Int_» _Val4 _Val5
      return _Val6
    | _, _ => none

  noncomputable def _5e5e323 : SortValSeq → SortBool → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 VS, false => do
      let _Val0 <- «addSummary(_,_)_VERIFICATION-SYNTAX_Int_ValSeq_Bool» VS true
      return _Val0
    | _, _ => none

  noncomputable def «addSummary(_,_)_VERIFICATION-SYNTAX_Int_ValSeq_Bool» (x0 : SortValSeq) (x1 : SortBool) : Option SortInt := (_23b69ae x0 x1) <|> (_5e5e323 x0 x1) <|> (_7d47044 x0 x1)
end