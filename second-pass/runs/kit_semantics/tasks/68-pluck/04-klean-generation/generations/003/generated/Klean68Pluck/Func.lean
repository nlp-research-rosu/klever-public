import Klean68Pluck.Inj

def _105572a : SortK → Option SortBool
  | K => some false

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _399d0a1 : SortValSeq → SortInt → SortInt → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _I, _B, J => some J
  | _, _, _, _ => none

def _4886931 : SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», I => some I
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

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom projectIntTotal (x0 : SortVal) : Option SortInt

def _a1ad7f9 : SortValSeq → SortInt → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _I, B => some B
  | _, _, _ => none

def _7300c95 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
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

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

mutual
  def «afterIndex(_,_)_VERIFICATION_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := (_4886931 x0 x1) <|> (_f1b0c8b x0 x1)

  def _f1b0c8b : SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _V R, I => do
      let _Val0 <- «_+Int_» I 1
      let _Val1 <- «afterIndex(_,_)_VERIFICATION_Int_ValSeq_Int» R _Val0
      return _Val1
    | _, _ => none
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _cd4e346 : SortInt → SortInt → Option SortVal
  | B, _J => do
    let _Val0 <- «_<Int_» B 0
    guard _Val0
    return ((@inj SortIterable SortVal) (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _a12d9b0 : SortInt → SortInt → Option SortVal
  | B, J => do
    let _Val0 <- «_>=Int_» B 0
    guard _Val0
    return ((@inj SortIterable SortVal) (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) B) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) J) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))))

def _21add3b : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def «resultList(_,_)_VERIFICATION_Val_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortVal := (_a12d9b0 x0 x1) <|> (_cd4e346 x0 x1)

def «definedProjectInt(_)_VERIFICATION_Bool_Val» (x0 : SortVal) : Option SortBool := _21add3b x0

noncomputable def _b706ea3 : SortInt → SortInt → Option SortBool
  | B, V => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» V 2
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «_<Int_» B 0
    let _Val3 <- «_<Int_» V B
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- _andBool_ _Val1 _Val4
    return _Val5

mutual
  noncomputable def _9b7e3cb : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- «definedProjectInt(_)_VERIFICATION_Bool_Val» V
      let _Val1 <- projectIntTotal V
      let _Val2 <- «_>=Int_» _Val1 0
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «allNonNegative(_)_VERIFICATION_Bool_ValSeq» R
      let _Val5 <- _andBool_ _Val3 _Val4
      return _Val5
    | _ => none

  noncomputable def «allNonNegative(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_7300c95 x0) <|> (_9b7e3cb x0)
end

noncomputable def «shouldTake(_,_)_VERIFICATION_Bool_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _b706ea3 x0 x1

noncomputable def _4c0b22f : SortInt → SortInt → Option SortInt
  | B, V => do
    let _Val0 <- «shouldTake(_,_)_VERIFICATION_Bool_Int_Int» B V
    guard _Val0
    return V

noncomputable def _93e22fa : SortInt → SortInt → SortInt → SortInt → Option SortInt
  | B, _J, V, I => do
    let _Val0 <- «shouldTake(_,_)_VERIFICATION_Bool_Int_Int» B V
    guard _Val0
    return I

noncomputable def _975a72b : SortInt → SortInt → SortInt → SortInt → Option SortInt
  | B, J, V, _I => do
    let _Val0 <- «shouldTake(_,_)_VERIFICATION_Bool_Int_Int» B V
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return J

noncomputable def _ff6bc1e : SortInt → SortInt → Option SortInt
  | B, V => do
    let _Val0 <- «shouldTake(_,_)_VERIFICATION_Bool_Int_Int» B V
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return B

noncomputable def «nextBestIndex(_,_,_,_)_VERIFICATION_Int_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortInt := (_93e22fa x0 x1 x2 x3) <|> (_975a72b x0 x1 x2 x3)

noncomputable def «nextBest(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_4c0b22f x0 x1) <|> (_ff6bc1e x0 x1)

mutual
  noncomputable def _6a835fd : SortValSeq → SortInt → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R, I, B => do
      let _Val0 <- «_+Int_» I 1
      let _Val1 <- projectIntTotal V
      let _Val2 <- «nextBest(_,_)_VERIFICATION_Int_Int_Int» B _Val1
      let _Val3 <- «scanBest(_,_,_)_VERIFICATION_Int_ValSeq_Int_Int» R _Val0 _Val2
      return _Val3
    | _, _, _ => none

  noncomputable def «scanBest(_,_,_)_VERIFICATION_Int_ValSeq_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_6a835fd x0 x1 x2) <|> (_a1ad7f9 x0 x1 x2)
end

mutual
  noncomputable def «scanBestIndex(_,_,_,_)_VERIFICATION_Int_ValSeq_Int_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortInt := (_399d0a1 x0 x1 x2 x3) <|> (_a48b706 x0 x1 x2 x3)

  noncomputable def _a48b706 : SortValSeq → SortInt → SortInt → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R, I, B, J => do
      let _Val0 <- «_+Int_» I 1
      let _Val1 <- projectIntTotal V
      let _Val2 <- «nextBest(_,_)_VERIFICATION_Int_Int_Int» B _Val1
      let _Val3 <- projectIntTotal V
      let _Val4 <- «nextBestIndex(_,_,_,_)_VERIFICATION_Int_Int_Int_Int_Int» B J _Val3 I
      let _Val5 <- «scanBestIndex(_,_,_,_)_VERIFICATION_Int_ValSeq_Int_Int_Int» R _Val0 _Val2 _Val4
      return _Val5
    | _, _, _, _ => none
end