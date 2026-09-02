import Klean153StrongestExtension.Inj

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1a63577 : SortVal → Option SortIntSeq
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS) => some CS
  | _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _3eaa2c0 : SortStr → Option SortIntSeq
  | SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS => some CS

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _c9bf9f2 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _f0c740b : SortValSeq → SortIntSeq → SortInt → Option SortIntSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», BEST, _BESTSCORE => some BEST
  | _, _, _ => none

def _4e9380a : SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», BESTSCORE => some BESTSCORE
  | _, _ => none

def _c3ab0c8 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», OLD => some OLD
  | _, _ => none

def _8e783e8 : SortValSeq → SortIntSeq → Option SortIntSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», OLD => some OLD
  | _, _ => none

def _91cd706 : SortValSeq → SortIntSeq → Option SortIntSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», OLD => some OLD
  | _, _ => none

def _dc0e917 : SortVal → Option SortBool
  | SortVal.inj_SortStr _Gen0 => some true
  | _ => none

def _e4668e9 : SortVal → Option SortBool
  | _Gen0 => some false

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

def _fb4eb32 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _b98c073 : SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», OLD => some OLD
  | _, _ => none

axiom projectStrTotal (x0 : SortVal) : Option SortStr

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def «codesProject(_)_VERIFICATION-BASE_IntSeq_Val» (x0 : SortVal) : Option SortIntSeq := _1a63577 x0

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

def «codesOf(_)_VERIFICATION-BASE_IntSeq_Str» (x0 : SortStr) : Option SortIntSeq := _3eaa2c0 x0

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def «bestCodes(_,_,_)_VERIFICATION-BASE_IntSeq_ValSeq_IntSeq_Int» (x0 : SortValSeq) (x1 : SortIntSeq) (x2 : SortInt) : Option SortIntSeq := _f0c740b x0 x1 x2

def «bestScore(_,_)_VERIFICATION-BASE_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := _4e9380a x0 x1

mutual
  def _7b754e3 : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C CS, OLD => do
      let _Val0 <- «lastCharacter(_,_)_VERIFICATION-BASE_IntSeq_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      return _Val0
    | _, _ => none

  def «lastCharacter(_,_)_VERIFICATION-BASE_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_7b754e3 x0 x1) <|> (_c3ab0c8 x0 x1)
end

def «isStringVal(_)_VERIFICATION-BASE_Bool_Val» (x0 : SortVal) : Option SortBool := (_dc0e917 x0) <|> (_e4668e9 x0)

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

def _1e0fa0e : SortIntSeq → SortValSeq → Option SortStr
  | CLASS, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => do
    let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» CLASS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val1 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» _Val0 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val1)
  | _, _ => none

mutual
  def _92b7540 : SortValSeq → SortIntSeq → Option SortIntSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS, _OLD => do
      let _Val0 <- «isStringVal(_)_VERIFICATION-BASE_Bool_Val» V
      let _Val1 <- «codesProject(_)_VERIFICATION-BASE_IntSeq_Val» V
      let _Val2 <- «lastExtension(_,_)_VERIFICATION-BASE_IntSeq_ValSeq_IntSeq» VS _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  def «lastExtension(_,_)_VERIFICATION-BASE_IntSeq_ValSeq_IntSeq» (x0 : SortValSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_91cd706 x0 x1) <|> (_92b7540 x0 x1)
end

mutual
  def _936e184 : SortValSeq → SortIntSeq → Option SortIntSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS, OLD => do
      let _Val0 <- «isStringVal(_)_VERIFICATION-BASE_Bool_Val» V
      let _Val1 <- «codesProject(_)_VERIFICATION-BASE_IntSeq_Val» V
      let _Val2 <- «lastCharacter(_,_)_VERIFICATION-BASE_IntSeq_IntSeq_IntSeq» _Val1 OLD
      let _Val3 <- «lastCharacterAcross(_,_)_VERIFICATION-BASE_IntSeq_ValSeq_IntSeq» VS _Val2
      guard _Val0
      return _Val3
    | _, _ => none

  def «lastCharacterAcross(_,_)_VERIFICATION-BASE_IntSeq_ValSeq_IntSeq» (x0 : SortValSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_8e783e8 x0 x1) <|> (_936e184 x0 x1)
end

mutual
  def «allStrings(_)_VERIFICATION-BASE_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_f3f1772 x0) <|> (_fb4eb32 x0)

  def _f3f1772 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- «isStringVal(_)_VERIFICATION-BASE_Bool_Val» V
      let _Val1 <- «allStrings(_)_VERIFICATION-BASE_Bool_ValSeq» VS
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none
end

def _e9518ed : SortVal → Option SortBool
  | V => do
    let _Val0 <- «isStringVal(_)_VERIFICATION-BASE_Bool_Val» V
    return _Val0

def «isLowerC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _1f3d8f0 x0

def «isUpperC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _b6acdbd x0

def «definedProjectStr(_)_VERIFICATION-BASE_Bool_Val» (x0 : SortVal) : Option SortBool := _e9518ed x0

def _7c7529d : SortInt → Option SortInt
  | C => do
    let _Val0 <- «isLowerC(_)_MPY-METHODS_Bool_Int» C
    guard _Val0
    return (-1)

def _08cc4e6 : SortInt → Option SortInt
  | C => do
    let _Val0 <- «isUpperC(_)_MPY-METHODS_Bool_Int» C
    guard _Val0
    return 1

def _d8c5f8b : SortInt → Option SortInt
  | C => do
    let _Val0 <- «isUpperC(_)_MPY-METHODS_Bool_Int» C
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «isLowerC(_)_MPY-METHODS_Bool_Int» C
    let _Val3 <- notBool_ _Val2
    let _Val4 <- _andBool_ _Val1 _Val3
    guard _Val4
    return 0

def «charStrength(_)_VERIFICATION-BASE_Int_Int» (x0 : SortInt) : Option SortInt := (_08cc4e6 x0) <|> (_7c7529d x0) <|> (_d8c5f8b x0)

mutual
  def _8704036 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C CS => do
      let _Val0 <- «charStrength(_)_VERIFICATION-BASE_Int_Int» C
      let _Val1 <- «extensionStrength(_)_VERIFICATION-BASE_Int_IntSeq» CS
      let _Val2 <- «_+Int_» _Val0 _Val1
      return _Val2
    | _ => none

  def «extensionStrength(_)_VERIFICATION-BASE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_8704036 x0) <|> (_c9bf9f2 x0)
end

def _4854865 : SortIntSeq → SortValSeq → Option SortStr
  | CLASS, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) VS => do
    let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» CLASS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val1 <- «extensionStrength(_)_VERIFICATION-BASE_Int_IntSeq» CS
    let _Val2 <- «bestCodes(_,_,_)_VERIFICATION-BASE_IntSeq_ValSeq_IntSeq_Int» VS CS _Val1
    let _Val3 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» _Val0 _Val2
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val3)
  | _, _ => none

mutual
  def «lastStrength(_,_)_VERIFICATION-BASE_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := (_b98c073 x0 x1) <|> (_c7d8007 x0 x1)

  def _c7d8007 : SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS, _OLD => do
      let _Val0 <- «isStringVal(_)_VERIFICATION-BASE_Bool_Val» V
      let _Val1 <- «codesProject(_)_VERIFICATION-BASE_IntSeq_Val» V
      let _Val2 <- «extensionStrength(_)_VERIFICATION-BASE_Int_IntSeq» _Val1
      let _Val3 <- «lastStrength(_,_)_VERIFICATION-BASE_Int_ValSeq_Int» VS _Val2
      guard _Val0
      return _Val3
    | _, _ => none
end

def «expectedResult(_,_)_VERIFICATION-BASE_Str_IntSeq_ValSeq» (x0 : SortIntSeq) (x1 : SortValSeq) : Option SortStr := (_1e0fa0e x0 x1) <|> (_4854865 x0 x1)