import Klean32FindZero.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _2f7a2f3 : SortNumSeq → Option SortBool
  | SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq» => some false
  | _ => none

axiom «_==Float_» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

def _912bd47 : SortNumSeq → Option SortInt
  | SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq» => some 0
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

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

axiom bisectFrom (x0 : SortNumSeq) (x1 : SortFloat) (x2 : SortFloat) : Option SortFloat

axiom bracketBegin (x0 : SortNumSeq) (x1 : SortFloat) (x2 : SortFloat) : Option SortFloat

axiom bracketEnd (x0 : SortNumSeq) (x1 : SortFloat) (x2 : SortFloat) : Option SortFloat

def _f5e2fa2 : SortNumSeq → Option SortValSeq
  | SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

axiom polyAcc (x0 : SortNumSeq) (x1 : SortFloat) (x2 : SortFloat) (x3 : SortFloat) : Option SortFloat

axiom polyLast (x0 : SortNumSeq) (x1 : SortVal) : Option SortVal

axiom polyPower (x0 : SortNumSeq) (x1 : SortFloat) (x2 : SortFloat) : Option SortFloat

axiom polyValue (x0 : SortNumSeq) (x1 : SortFloat) : Option SortFloat

axiom solveFrom (x0 : SortNumSeq) (x1 : SortFloat) (x2 : SortFloat) : Option SortFloat

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _3994b91 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0

mutual
  def _7cf73f6 : SortNumSeq → Option SortInt
    | SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq» _Gen0 NS => do
      let _Val0 <- «numLen(_)_VERIFICATION-SYNTAX_Int_NumSeq» NS
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def _9a79709 : SortNumSeq → Option SortInt
    | SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq» _Gen0 NS => do
      let _Val0 <- «numLen(_)_VERIFICATION-SYNTAX_Int_NumSeq» NS
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «numLen(_)_VERIFICATION-SYNTAX_Int_NumSeq» (x0 : SortNumSeq) : Option SortInt := (_7cf73f6 x0) <|> (_912bd47 x0) <|> (_9a79709 x0)
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  def «numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» (x0 : SortNumSeq) : Option SortValSeq := (_ef0f289 x0) <|> (_f5e2fa2 x0) <|> (_fe2b4c3 x0)

  def _ef0f289 : SortNumSeq → Option SortValSeq
    | SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq» F NS => do
      let _Val0 <- «numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» NS
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortFloat SortVal) F) _Val0)
    | _ => none

  def _fe2b4c3 : SortNumSeq → Option SortValSeq
    | SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq» I NS => do
      let _Val0 <- «numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» NS
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) I) _Val0)
    | _ => none
end

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def eqF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _3994b91 x0 x1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def _4425a91 : SortNumSeq → Option SortBool
  | SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq» F SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq» => do
    let _Val0 <- eqF F (0.0 : Float)
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _ => none

def _255e7c8 : SortNumSeq → Option SortBool
  | SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq» I SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq» => do
    let _Val0 <- «_=/=Int_» I 0
    return _Val0
  | _ => none

mutual
  noncomputable def _48c19f4 : SortNumSeq → Option SortBool
    | SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq» _Gen0 NS => do
      let _Val0 <- «numLen(_)_VERIFICATION-SYNTAX_Int_NumSeq» NS
      let _Val1 <- «_>Int_» _Val0 0
      let _Val2 <- «lastNonZero(_)_VERIFICATION-SYNTAX_Bool_NumSeq» NS
      guard _Val1
      return _Val2
    | _ => none

  noncomputable def «lastNonZero(_)_VERIFICATION-SYNTAX_Bool_NumSeq» (x0 : SortNumSeq) : Option SortBool := (_255e7c8 x0) <|> (_2f7a2f3 x0) <|> (_4425a91 x0) <|> (_48c19f4 x0) <|> (_d82a476 x0)

  noncomputable def _d82a476 : SortNumSeq → Option SortBool
    | SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq» _Gen0 NS => do
      let _Val0 <- «numLen(_)_VERIFICATION-SYNTAX_Int_NumSeq» NS
      let _Val1 <- «_>Int_» _Val0 0
      let _Val2 <- «lastNonZero(_)_VERIFICATION-SYNTAX_Bool_NumSeq» NS
      guard _Val1
      return _Val2
    | _ => none
end

noncomputable def _6aa256e : SortNumSeq → Option SortBool
  | NS => do
    let _Val0 <- «numLen(_)_VERIFICATION-SYNTAX_Int_NumSeq» NS
    let _Val1 <- «_>=Int_» _Val0 2
    let _Val2 <- «numLen(_)_VERIFICATION-SYNTAX_Int_NumSeq» NS
    let _Val3 <- «_%Int_» _Val2 2
    let _Val4 <- «_==Int_» _Val3 0
    let _Val5 <- _andBool_ _Val1 _Val4
    let _Val6 <- «lastNonZero(_)_VERIFICATION-SYNTAX_Bool_NumSeq» NS
    let _Val7 <- _andBool_ _Val5 _Val6
    return _Val7

noncomputable def «validCoeffs(_)_VERIFICATION-SYNTAX_Bool_NumSeq» (x0 : SortNumSeq) : Option SortBool := _6aa256e x0