import Klean0HasCloseElements.Inj

axiom «absFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _613283e : SortK → Option SortBool
  | K => some false

def _d74a36c : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortFloat Float) SortK.dotk => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _28a3833 : SortBool → SortFloat → SortFloat → SortInt → SortInt → SortValSeq → Option SortBool
  | B, _Gen0, _Gen1, _Gen2, _Gen3, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some B
  | _, _, _, _, _, _ => none

def _3477407 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

axiom «_-Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «_<Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

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

def _a94d8df : SortVal → Option SortFloat
  | SortVal.inj_SortFloat F => some F
  | _ => none

def _ad812ac : SortBool → SortValSeq → SortFloat → SortInt → SortValSeq → Option SortBool
  | B, _Gen0, _Gen1, _Gen2, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some B
  | _, _, _, _, _ => none

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

noncomputable def _00d63fc : SortFloat → Option SortFloat
  | F => do
    let _Val0 <- «absFloat(_)_FLOAT_Float_Float» F
    return _Val0

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def isFloat (x0 : SortK) : Option SortBool := (_d74a36c x0) <|> (_613283e x0)

noncomputable def _fabe8f9 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_-Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _5667141 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_<Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def absF (x0 : SortFloat) : Option SortFloat := _00d63fc x0

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def _16f2e42 : SortVal → Option SortFloat
  | V => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return (0.0 : Float)

noncomputable def subF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _fabe8f9 x0 x1

noncomputable def floatLt (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _5667141 x0 x1

mutual
  def _9b6cbdf : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allFloats(_)_VERIFICATION_Bool_ValSeq» R
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allFloats(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_3477407 x0) <|> (_9b6cbdf x0)
end

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def «asFloat(_)_VERIFICATION_Float_Val» (x0 : SortVal) : Option SortFloat := (_16f2e42 x0) <|> (_a94d8df x0)

noncomputable def _4720d69 : SortFloat → SortFloat → SortFloat → Option SortBool
  | A, B, T => do
    let _Val0 <- subF A B
    let _Val1 <- absF _Val0
    let _Val2 <- floatLt _Val1 T
    return _Val2

noncomputable def «pairNear(_,_,_)_VERIFICATION_Bool_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) (x2 : SortFloat) : Option SortBool := _4720d69 x0 x1 x2

mutual
  noncomputable def «rowAcc(_,_,_,_,_,_)_VERIFICATION_Bool_Bool_Float_Float_Int_Int_ValSeq» (x0 : SortBool) (x1 : SortFloat) (x2 : SortFloat) (x3 : SortInt) (x4 : SortInt) (x5 : SortValSeq) : Option SortBool := (_28a3833 x0 x1 x2 x3 x4 x5) <|> (_ffdfae5 x0 x1 x2 x3 x4 x5)

  noncomputable def _ffdfae5 : SortBool → SortFloat → SortFloat → SortInt → SortInt → SortValSeq → Option SortBool
    | B, A, T, I, J, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- «_<Int_» I J
      let _Val1 <- «asFloat(_)_VERIFICATION_Float_Val» V
      let _Val2 <- «pairNear(_,_,_)_VERIFICATION_Bool_Float_Float_Float» A _Val1 T
      let _Val3 <- _orBool_ B _Val2
      let _Val4 <- kite _Val0 _Val3 B
      let _Val5 <- «_+Int_» J 1
      let _Val6 <- «rowAcc(_,_,_,_,_,_)_VERIFICATION_Bool_Bool_Float_Float_Int_Int_ValSeq» _Val4 A T I _Val5 R
      return _Val6
    | _, _, _, _, _, _ => none
end

mutual
  noncomputable def _84c09d9 : SortBool → SortValSeq → SortFloat → SortInt → SortValSeq → Option SortBool
    | B, VS, T, I, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A R => do
      let _Val0 <- «asFloat(_)_VERIFICATION_Float_Val» A
      let _Val1 <- «rowAcc(_,_,_,_,_,_)_VERIFICATION_Bool_Bool_Float_Float_Int_Int_ValSeq» B _Val0 T I 0 VS
      let _Val2 <- «_+Int_» I 1
      let _Val3 <- «outerAcc(_,_,_,_,_)_VERIFICATION_Bool_Bool_ValSeq_Float_Int_ValSeq» _Val1 VS T _Val2 R
      return _Val3
    | _, _, _, _, _ => none

  noncomputable def «outerAcc(_,_,_,_,_)_VERIFICATION_Bool_Bool_ValSeq_Float_Int_ValSeq» (x0 : SortBool) (x1 : SortValSeq) (x2 : SortFloat) (x3 : SortInt) (x4 : SortValSeq) : Option SortBool := (_84c09d9 x0 x1 x2 x3 x4) <|> (_ad812ac x0 x1 x2 x3 x4)
end