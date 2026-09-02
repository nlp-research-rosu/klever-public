import Klean142SumSquares.Inj

def _010fe30 : SortVal → Option SortBool
  | _Gen0 => some false

def _105572a : SortK → Option SortBool
  | K => some false

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

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _1ecd2fa : SortValSeq → SortInt → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _I, ACC => some ACC
  | _, _, _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _6206d78 : SortVal → Option SortBool
  | SortVal.«ref(_)_MPY-CORE_Val_Int» _Gen0 => some true
  | _ => none

def _d0a8392 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

axiom projectIntTotal (x0 : SortVal) : Option SortInt

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

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def «isRefV(_)_MPY-CORE_Bool_Val» (x0 : SortVal) : Option SortBool := (_6206d78 x0) <|> (_010fe30 x0)

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _21add3b : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

def _a9f73dc : SortValSeq → SortInt → SortInt → Option SortInt
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _REST, _I, _ACC => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return 0
  | _, _, _ => none

mutual
  def _6c6a190 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «isRefV(_)_MPY-CORE_Bool_Val» V
      let _Val2 <- notBool_ _Val1
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «allInts(_)_VERIFICATION_Bool_ValSeq» REST
      let _Val5 <- _andBool_ _Val3 _Val4
      return _Val5
    | _ => none

  def «allInts(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_6c6a190 x0) <|> (_d0a8392 x0)
end

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def _3f3000b : SortInt → SortInt → Option SortInt
  | V, I => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 3
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «_*Int_» V V
    guard _Val1
    return _Val2

def «definedProjectInt(_)_VERIFICATION_Bool_Val» (x0 : SortVal) : Option SortBool := _21add3b x0

noncomputable def _1a2440b : SortInt → SortInt → Option SortInt
  | V, I => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 3
    let _Val1 <- «_=/=Int_» _Val0 0
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 4
    let _Val3 <- «_==Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    let _Val5 <- «_*Int_» V V
    let _Val6 <- «_*Int_» _Val5 V
    guard _Val4
    return _Val6

noncomputable def _1ef7565 : SortInt → SortInt → Option SortInt
  | V, I => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 3
    let _Val1 <- «_=/=Int_» _Val0 0
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 4
    let _Val3 <- «_=/=Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    guard _Val4
    return V

noncomputable def «squareContribution(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_1a2440b x0 x1) <|> (_1ef7565 x0 x1) <|> (_3f3000b x0 x1)

mutual
  noncomputable def _789d132 : SortValSeq → SortInt → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, I, ACC => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «_+Int_» I 1
      let _Val2 <- projectIntTotal V
      let _Val3 <- «squareContribution(_,_)_VERIFICATION_Int_Int_Int» _Val2 I
      let _Val4 <- «_+Int_» ACC _Val3
      let _Val5 <- «sumSquaresAcc(_,_,_)_VERIFICATION_Int_ValSeq_Int_Int» REST _Val1 _Val4
      guard _Val0
      return _Val5
    | _, _, _ => none

  noncomputable def «sumSquaresAcc(_,_,_)_VERIFICATION_Int_ValSeq_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_1ecd2fa x0 x1 x2) <|> (_789d132 x0 x1 x2) <|> (_a9f73dc x0 x1 x2)
end