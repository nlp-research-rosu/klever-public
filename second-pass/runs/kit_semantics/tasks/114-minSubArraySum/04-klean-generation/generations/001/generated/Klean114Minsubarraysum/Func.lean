import Klean114Minsubarraysum.Inj

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

def _d9c6ec1 : SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», C => some C
  | _, _ => none

def _f316b87 : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt K) SortK.dotk => some K
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

def _e993c16 : SortValSeq → SortInt → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _C, B => some B
  | _, _, _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _e1effea : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_>=Int_» I1 I2
    guard _Val0
    return I2

def _5615d55 : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_<Int_» I1 I2
    guard _Val0
    return I1

def «project:Int» (x0 : SortK) : Option SortInt := _f316b87 x0

mutual
  def _01539d8 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V XS => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allInts(_)_VERIFICATION_Bool_ValSeq» XS
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allInts(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_01539d8 x0) <|> (_d0a8392 x0)
end

def «minInt(_,_)_INT-COMMON_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_5615d55 x0 x1) <|> (_e1effea x0 x1)

mutual
  def _432fced : SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V XS, C => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val2 <- «project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val3 <- «_+Int_» C _Val2
      let _Val4 <- «minInt(_,_)_INT-COMMON_Int_Int_Int» _Val1 _Val3
      let _Val5 <- «kadaneCurrent(_,_)_VERIFICATION_Int_ValSeq_Int» XS _Val4
      guard _Val0
      return _Val5
    | _, _ => none

  def «kadaneCurrent(_,_)_VERIFICATION_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := (_432fced x0 x1) <|> (_d9c6ec1 x0 x1)
end

mutual
  def «kadaneMinimum(_,_,_)_VERIFICATION_Int_ValSeq_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_e735bcb x0 x1 x2) <|> (_e993c16 x0 x1 x2)

  def _e735bcb : SortValSeq → SortInt → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V XS, C, B => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val2 <- «project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val3 <- «_+Int_» C _Val2
      let _Val4 <- «minInt(_,_)_INT-COMMON_Int_Int_Int» _Val1 _Val3
      let _Val5 <- «project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val6 <- «project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val7 <- «_+Int_» C _Val6
      let _Val8 <- «minInt(_,_)_INT-COMMON_Int_Int_Int» _Val5 _Val7
      let _Val9 <- «minInt(_,_)_INT-COMMON_Int_Int_Int» B _Val8
      let _Val10 <- «kadaneMinimum(_,_,_)_VERIFICATION_Int_ValSeq_Int_Int» XS _Val4 _Val9
      guard _Val0
      return _Val10
    | _, _, _ => none
end