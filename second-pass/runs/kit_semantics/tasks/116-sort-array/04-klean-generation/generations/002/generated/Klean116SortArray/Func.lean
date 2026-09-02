import Klean116SortArray.Inj

def _0e70039 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _105572a : SortK → Option SortBool
  | K => some false

def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _37dc11b : SortInt → SortIntSeq → Option SortIntSeq
  | 0, ACC => some ACC
  | _, _ => none

def _5a819d8 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _f69553d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _4154192 : SortIntSeq → SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some 0
  | _, _ => none

def _4183651 : SortIntSeq → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _, _ => none

def _49c55eb : SortInt → Option SortIntSeq
  | 0 => some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
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

def _16468f1 : SortIntSeq → SortInt → Option SortIntSeq
  | S, N => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return S

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

mutual
  def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

mutual
  def «dropIS(_,_)_MPY-METHODS_IntSeq_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortIntSeq := (_16468f1 x0 x1) <|> (_aa907da x0 x1) <|> (_4183651 x0 x1)

  def _aa907da : SortIntSeq → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 R, N => do
      let _Val0 <- «_>Int_» N 0
      let _Val1 <- «_-Int_» N 1
      let _Val2 <- «dropIS(_,_)_MPY-METHODS_IntSeq_IntSeq_Int» R _Val1
      guard _Val0
      return _Val2
    | _, _ => none
end

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

mutual
  def _3a4bf2f : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  def «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_3a4bf2f x0 x1) <|> (_5a819d8 x0 x1) <|> (_f69553d x0 x1)
end

mutual
  def _6501b24 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allIntVS(_)_VERIFICATION_Bool_ValSeq» VS
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allIntVS(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_0e70039 x0) <|> (_6501b24 x0)
end

axiom _62d7600 : SortInt → SortIntSeq → Option SortIntSeq
axiom «binAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortIntSeq

axiom «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortInt
axiom _b153473 : SortIntSeq → SortIntSeq → Option SortInt
axiom _f1b90b3 : SortIntSeq → SortIntSeq → Option SortInt

noncomputable def _323c995 : SortInt → Option SortIntSeq
  | N => do
    let _Val0 <- «_>Int_» N 0
    let _Val1 <- «binAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» N SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    guard _Val0
    return _Val1

noncomputable def «binCodes(_)_MPY-BUILTINS_IntSeq_Int» (x0 : SortInt) : Option SortIntSeq := (_323c995 x0) <|> (_49c55eb x0)

noncomputable def _627d49d : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_-Int_» 0 I
    let _Val2 <- «binCodes(_)_MPY-BUILTINS_IntSeq_Int» _Val1
    let _Val3 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» _Val2 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 49 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    guard _Val0
    return _Val3

noncomputable def _87710f4 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «binCodes(_)_MPY-BUILTINS_IntSeq_Int» I
    let _Val2 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» _Val1 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 49 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    guard _Val0
    return _Val2

noncomputable def «popcountAbs(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_627d49d x0) <|> (_87710f4 x0)