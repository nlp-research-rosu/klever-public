import Klean28Concatenate.Inj

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

def _cf33b9e : SortVal → Option SortIntSeq
  | _Gen0 => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def _e6bcb3c : SortVal → Option SortIntSeq
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» S) => some S
  | _ => none

def _f77ed8f : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _8c12e54 : SortVal → SortValSeq → Option SortVal
  | CURRENT, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some CURRENT
  | _, _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _b68818b : SortIntSeq → SortValSeq → Option SortIntSeq
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some ACC
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

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def «stringCodes(_)_VERIFICATION_IntSeq_Val» (x0 : SortVal) : Option SortIntSeq := (_e6bcb3c x0) <|> (_cf33b9e x0)

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

mutual
  noncomputable def _3ef2c0c : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «stringCodes(_)_VERIFICATION_IntSeq_Val» V
      let _Val1 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0)) SortK.dotk)
      let _Val2 <- «isStringSeq(_)_VERIFICATION_Bool_ValSeq» REST
      let _Val3 <- _andBool_ _Val1 _Val2
      return _Val3
    | _ => none

  noncomputable def «isStringSeq(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_3ef2c0c x0) <|> (_f77ed8f x0)
end

mutual
  noncomputable def _60cf328 : SortVal → SortValSeq → Option SortVal
    | _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «stringCodes(_)_VERIFICATION_IntSeq_Val» V
      let _Val1 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0)) SortK.dotk)
      let _Val2 <- «lastFrom(_,_)_VERIFICATION_Val_Val_ValSeq» V REST
      guard _Val1
      return _Val2
    | _, _ => none

  noncomputable def «lastFrom(_,_)_VERIFICATION_Val_Val_ValSeq» (x0 : SortVal) (x1 : SortValSeq) : Option SortVal := (_60cf328 x0 x1) <|> (_8c12e54 x0 x1)
end

mutual
  noncomputable def _8c4d30b : SortIntSeq → SortValSeq → Option SortIntSeq
    | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «stringCodes(_)_VERIFICATION_IntSeq_Val» V
      let _Val1 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0)) SortK.dotk)
      let _Val2 <- «stringCodes(_)_VERIFICATION_IntSeq_Val» V
      let _Val3 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» ACC _Val2
      let _Val4 <- «concatFrom(_,_)_VERIFICATION_IntSeq_IntSeq_ValSeq» _Val3 REST
      guard _Val1
      return _Val4
    | _, _ => none

  noncomputable def «concatFrom(_,_)_VERIFICATION_IntSeq_IntSeq_ValSeq» (x0 : SortIntSeq) (x1 : SortValSeq) : Option SortIntSeq := (_8c4d30b x0 x1) <|> (_b68818b x0 x1)
end