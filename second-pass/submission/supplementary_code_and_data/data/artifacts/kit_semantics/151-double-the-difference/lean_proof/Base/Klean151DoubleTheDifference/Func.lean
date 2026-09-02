import Klean151DoubleTheDifference.Inj

def _e49baf7 : SortValSeq → SortVal → Option SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», OLD => some OLD
  | _, _ => none

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

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _37fd059 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

def _613283e : SortK → Option SortBool
  | K => some false

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

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

def _d74a36c : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortFloat Float) SortK.dotk => some true
  | _ => none

def _fca73ab : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

axiom projectIntTotal (x0 : SortVal) : Option SortInt

mutual
  def _0771a75 : SortValSeq → SortVal → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS, _OLD => do
      let _Val0 <- «lastNumber(_,_)_VERIFICATION-SYNTAX_Val_ValSeq_Val» VS V
      return _Val0
    | _, _ => none

  def «lastNumber(_,_)_VERIFICATION-SYNTAX_Val_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortVal := (_0771a75 x0 x1) <|> (_e49baf7 x0 x1)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def isFloat (x0 : SortK) : Option SortBool := (_d74a36c x0) <|> (_613283e x0)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _c73d4a8 : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

mutual
  def «numericVals(_)_VERIFICATION-SYNTAX_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_c722e91 x0) <|> (_fca73ab x0)

  def _c722e91 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val2 <- _orBool_ _Val0 _Val1
      let _Val3 <- «numericVals(_)_VERIFICATION-SYNTAX_Bool_ValSeq» VS
      let _Val4 <- _andBool_ _Val2 _Val3
      return _Val4
    | _ => none
end

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» (x0 : SortVal) : Option SortBool := _c73d4a8 x0

noncomputable def _1b34a52 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_>Int_» I 0
    let _Val1 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
    let _Val2 <- «_==Int_» _Val1 1
    let _Val3 <- _andBool_ _Val0 _Val2
    let _Val4 <- «_*Int_» I I
    let _Val5 <- kite _Val3 _Val4 0
    return _Val5

noncomputable def «oddIntSquare(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : Option SortInt := _1b34a52 x0

mutual
  noncomputable def _5a41276 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) VS => do
      let _Val0 <- «oddIntSquare(_)_VERIFICATION-SYNTAX_Int_Int» I
      let _Val1 <- «dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» VS
      let _Val2 <- «_+Int_» _Val0 _Val1
      return _Val2
    | _ => none

  noncomputable def _96cd29b : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _V VS => do
      let _Val0 <- «dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» VS
      return _Val0
    | _ => none

  noncomputable def «dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_37fd059 x0) <|> (_5a41276 x0) <|> (_a3c2677 x0) <|> (_96cd29b x0)

  noncomputable def _a3c2677 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortFloat _F) VS => do
      let _Val0 <- «dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» VS
      return _Val0
    | _ => none
end