import Klean161Solve.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _3c5ecf9 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», A => some A
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _6fb1c40 : SortIntSeq → SortBool → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», FOUND => some FOUND
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _6cfd1c6 : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

def _3f833fc : SortIntSeq → SortStr → Option SortStr
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», INITIAL => some INITIAL
  | _, _ => none

def _6fe8151 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», OUT => some OUT
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

mutual
  def «revISAcc(_,_)_MPY-METHODS_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_3c5ecf9 x0 x1) <|> (_cf6961f x0 x1)

  def _cf6961f : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, A => do
      let _Val0 <- «revISAcc(_,_)_MPY-METHODS_IntSeq_IntSeq_IntSeq» R (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C A)
      return _Val0
    | _, _ => none
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def «alphaAcc(_,_)_VERIFICATION_Bool_IntSeq_Bool» (x0 : SortIntSeq) (x1 : SortBool) : Option SortBool := _6fb1c40 x0 x1

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

mutual
  def _70b7a82 : SortIntSeq → SortStr → Option SortStr
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST, _Gen0 => do
      let _Val0 <- «lastChar(_,_)_VERIFICATION_Str_IntSeq_Str» REST (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))
      return _Val0
    | _, _ => none

  def «lastChar(_,_)_VERIFICATION_Str_IntSeq_Str» (x0 : SortIntSeq) (x1 : SortStr) : Option SortStr := (_3f833fc x0 x1) <|> (_70b7a82 x0 x1)
end

def «toggleAcc(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := _6fe8151 x0 x1

def _4c429fa : SortIntSeq → Option SortIntSeq
  | S => do
    let _Val0 <- «revISAcc(_,_)_MPY-METHODS_IntSeq_IntSeq_IntSeq» S SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return _Val0

def _1f3d8f0 : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_>=Int_» C 97
    let _Val1 <- «_<=Int_» C 122
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

def _b6acdbd : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_>=Int_» C 65
    let _Val1 <- «_<=Int_» C 90
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

def _a9dabe2 : SortIntSeq → Option SortStr
  | INPUT => do
    let _Val0 <- «alphaAcc(_,_)_VERIFICATION_Bool_IntSeq_Bool» INPUT false
    let _Val1 <- «toggleAcc(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» INPUT SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    guard _Val0
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val1)

def «revIS(_)_MPY-METHODS_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _4c429fa x0

def «isLowerC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _1f3d8f0 x0

def «isUpperC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _b6acdbd x0

def _0fc3a6b : SortIntSeq → Option SortStr
  | INPUT => do
    let _Val0 <- «alphaAcc(_,_)_VERIFICATION_Bool_IntSeq_Bool» INPUT false
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «revIS(_)_MPY-METHODS_IntSeq_IntSeq» INPUT
    guard _Val1
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val2)

def _d240c9a : SortInt → Option SortBool
  | C => do
    let _Val0 <- «isUpperC(_)_MPY-METHODS_Bool_Int» C
    let _Val1 <- «isLowerC(_)_MPY-METHODS_Bool_Int» C
    let _Val2 <- _orBool_ _Val0 _Val1
    return _Val2

def «solveResult(_)_VERIFICATION_Str_IntSeq» (x0 : SortIntSeq) : Option SortStr := (_0fc3a6b x0) <|> (_a9dabe2 x0)

def «isAlphaC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _d240c9a x0

mutual
  def «allAlpha(_)_MPY-METHODS_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_6cfd1c6 x0) <|> (_bbba114 x0)

  def _bbba114 : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S => do
      let _Val0 <- «isAlphaC(_)_MPY-METHODS_Bool_Int» C
      let _Val1 <- «allAlpha(_)_MPY-METHODS_Bool_IntSeq» S
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none
end

noncomputable def _3ef9c00 : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») SortK.dotk)
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «allAlpha(_)_MPY-METHODS_Bool_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val3 <- _andBool_ _Val1 _Val2
    return _Val3

noncomputable def «charAlpha(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _3ef9c00 x0