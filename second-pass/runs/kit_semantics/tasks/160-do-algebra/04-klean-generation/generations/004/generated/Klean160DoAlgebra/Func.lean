import Klean160DoAlgebra.Inj

def _4c0724c : SortStr → Option SortIntSeq
  | SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS => some CS

axiom projectStrTotal (x0 : SortVal) : Option SortStr

def _105572a : SortK → Option SortBool
  | K => some false

def _199586e : SortValSeq → SortValSeq → Option SortBool
  | _Gen0, _Gen1 => some false

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _8978072 : SortVal → Option SortBool
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Gen0) => some true
  | _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

noncomputable local instance : DecidableEq SortK :=
  Classical.typeDecidableEq SortK
noncomputable def «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool :=
  some (decide (x0 = x1))

axiom projectIntTotal (x0 : SortVal) : Option SortInt

def _c70d5d7 : SortValSeq → SortValSeq → SortVal → Option SortBool
  | _Gen0, _Gen1, _Gen2 => some false

def _c788a4b : SortVal → Option SortBool
  | _Gen0 => some false

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _218dc3a : SortString → Option SortIntSeq
  | "" => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

def _4c85819 : SortValSeq → SortValSeq → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some V
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _559e74d : SortIntSeq → SortValSeq → SortValSeq → Option SortIntSeq
  | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 _Gen1, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some ACC
  | _, _, _ => none

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

def _5f3e80b : SortIntSeq → SortValSeq → SortValSeq → Option SortIntSeq
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some ACC
  | _, _, _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _6f428b7 : SortValSeq → SortValSeq → Option SortVal
  | _Gen0, _Gen1 => some SortVal.«noneV_MPY-CORE_Val»

axiom «Int2String(_)_STRING-COMMON_String_Int» (x0 : SortInt) : Option SortString

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

def «codesOf(_)_VERIFICATION-SYNTAX_IntSeq_Str» (x0 : SortStr) : Option SortIntSeq := _4c0724c x0

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def «isStrV(_)_MPY-BUILTINS_Bool_Val» (x0 : SortVal) : Option SortBool := (_8978072 x0) <|> (_c788a4b x0)

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

def «lastPairValue(_,_)_VERIFICATION-SYNTAX_Val_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortVal := (_4c85819 x0 x1) <|> (_6f428b7 x0 x1)

noncomputable def _0060a79 : SortVal → Option SortIntSeq
  | V => do
    let _Val0 <- projectStrTotal V
    let _Val1 <- «codesOf(_)_VERIFICATION-SYNTAX_IntSeq_Str» _Val0
    return _Val1

noncomputable def _94a39fc : SortValSeq → SortValSeq → SortVal → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», OR, W => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) OR) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) SortValSeq.«.ValSeq_MPY-CORE_ValSeq») SortK.dotk)
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) W) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)) SortK.dotk)
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2
  | _, _, _ => none

def _c73d4a8 : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

noncomputable def _362c6ed : SortVal → Option SortBool
  | V => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 43 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) SortK.dotk)
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) SortK.dotk)
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) SortK.dotk)
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))) SortK.dotk)
    let _Val6 <- _orBool_ _Val4 _Val5
    let _Val7 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))) SortK.dotk)
    let _Val8 <- _orBool_ _Val6 _Val7
    return _Val8

def _66b4901 : SortVal → Option SortBool
  | V => do
    let _Val0 <- «isStrV(_)_MPY-BUILTINS_Bool_Val» V
    return _Val0

noncomputable def _f390a9b : SortString → SortString → Option SortBool
  | S1, S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def «codesProject(_)_VERIFICATION-SYNTAX_IntSeq_Val» (x0 : SortVal) : Option SortIntSeq := _0060a79 x0

def «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» (x0 : SortVal) : Option SortBool := _c73d4a8 x0

noncomputable def «allowedOperator(_)_VERIFICATION-SYNTAX_Bool_Val» (x0 : SortVal) : Option SortBool := _362c6ed x0

def «definedProjectStr(_)_VERIFICATION-SYNTAX_Bool_Val» (x0 : SortVal) : Option SortBool := _66b4901 x0

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

mutual
  noncomputable def _0709310 : SortValSeq → SortValSeq → SortVal → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V NR, OR, CURRENT => do
      let _Val0 <- «allowedOperator(_)_VERIFICATION-SYNTAX_Bool_Val» CURRENT
      let _Val1 <- «validAlgebraLists(_,_)_VERIFICATION-SYNTAX_Bool_ValSeq_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V NR) OR
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _, _ => none

  noncomputable def _1704858 : SortValSeq → SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V NR, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» W OR => do
      let _Val0 <- «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» V
      let _Val1 <- projectIntTotal V
      let _Val2 <- «_>=Int_» _Val1 0
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «definedProjectStr(_)_VERIFICATION-SYNTAX_Bool_Val» W
      let _Val5 <- _andBool_ _Val3 _Val4
      let _Val6 <- «validAlgebraRest(_,_,_)_VERIFICATION-SYNTAX_Bool_ValSeq_ValSeq_Val» NR OR W
      let _Val7 <- _andBool_ _Val5 _Val6
      return _Val7
    | _, _ => none

  noncomputable def «validAlgebraLists(_,_)_VERIFICATION-SYNTAX_Bool_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortBool := (_1704858 x0 x1) <|> (_199586e x0 x1)

  noncomputable def «validAlgebraRest(_,_,_)_VERIFICATION-SYNTAX_Bool_ValSeq_ValSeq_Val» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortVal) : Option SortBool := (_0709310 x0 x1 x2) <|> (_94a39fc x0 x1 x2) <|> (_c70d5d7 x0 x1 x2)
end

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

mutual
  noncomputable def _88843b2 : SortIntSeq → SortValSeq → SortValSeq → Option SortIntSeq
    | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V NR, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» W OR => do
      let _Val0 <- projectIntTotal V
      let _Val1 <- «Int2String(_)_STRING-COMMON_String_Int» _Val0
      let _Val2 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val1
      let _Val3 <- «codesProject(_)_VERIFICATION-SYNTAX_IntSeq_Val» W
      let _Val4 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» _Val2 _Val3
      let _Val5 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» ACC _Val4
      let _Val6 <- «runPairCodes(_,_,_)_VERIFICATION-SYNTAX_IntSeq_IntSeq_ValSeq_ValSeq» _Val5 NR OR
      return _Val6
    | _, _, _ => none

  noncomputable def «runPairCodes(_,_,_)_VERIFICATION-SYNTAX_IntSeq_IntSeq_ValSeq_ValSeq» (x0 : SortIntSeq) (x1 : SortValSeq) (x2 : SortValSeq) : Option SortIntSeq := (_559e74d x0 x1 x2) <|> (_5f3e80b x0 x1 x2) <|> (_88843b2 x0 x1 x2)
end