import Klean74TotalMatch.Inj

def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _816b593 : SortInt → SortValSeq → Option SortInt
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some ACC
  | _, _ => none

def _8978072 : SortVal → Option SortBool
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Gen0) => some true
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

def _c788a4b : SortVal → Option SortBool
  | _Gen0 => some false

def _f8785d0 : SortValSeq → SortVal → Option SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», OLD => some OLD
  | _, _ => none

def _e77e681 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _cf33b9e : SortVal → Option SortIntSeq
  | _V => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def _e6bcb3c : SortVal → Option SortIntSeq
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS) => some CS
  | _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

def «isStrV(_)_MPY-BUILTINS_Bool_Val» (x0 : SortVal) : Option SortBool := (_8978072 x0) <|> (_c788a4b x0)

mutual
  def «lastLoopValue(_,_)_VERIFICATION_Val_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortVal := (_df2e2e5 x0 x1) <|> (_f8785d0 x0 x1)

  def _df2e2e5 : SortValSeq → SortVal → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, _OLD => do
      let _Val0 <- «lastLoopValue(_,_)_VERIFICATION_Val_ValSeq_Val» REST V
      return _Val0
    | _, _ => none
end

def «stringCodes(_)_VERIFICATION_IntSeq_Val» (x0 : SortVal) : Option SortIntSeq := (_e6bcb3c x0) <|> (_cf33b9e x0)

mutual
  def «onlyStrings(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_dd81058 x0) <|> (_e77e681 x0)

  def _dd81058 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «isStrV(_)_MPY-BUILTINS_Bool_Val» V
      let _Val1 <- «onlyStrings(_)_VERIFICATION_Bool_ValSeq» REST
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none
end

mutual
  def «totalLenFrom(_,_)_VERIFICATION_Int_Int_ValSeq» (x0 : SortInt) (x1 : SortValSeq) : Option SortInt := (_816b593 x0 x1) <|> (_d3ca825 x0 x1)

  def _d3ca825 : SortInt → SortValSeq → Option SortInt
    | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «stringCodes(_)_VERIFICATION_IntSeq_Val» V
      let _Val1 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val0
      let _Val2 <- «_+Int_» ACC _Val1
      let _Val3 <- «totalLenFrom(_,_)_VERIFICATION_Int_Int_ValSeq» _Val2 REST
      return _Val3
    | _, _ => none
end

def _cf47cb5 : SortValSeq → Option SortInt
  | ITEMS => do
    let _Val0 <- «totalLenFrom(_,_)_VERIFICATION_Int_Int_ValSeq» 0 ITEMS
    return _Val0

def «totalLen(_)_VERIFICATION_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := _cf47cb5 x0