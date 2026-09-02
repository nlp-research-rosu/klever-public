import Klean119MatchParens.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «nextBalance(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _abb83a5 : SortIntSeq → SortInt → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _B, M => some M
  | _, _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _ea089d4 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», B => some B
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _f7c7415 : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

def _ca87757 : SortIntSeq → SortVal → Option SortVal
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», OLD => some OLD
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

def _13745ee : SortInt → SortInt → Option SortInt
  | N, M => do
    let _Val0 <- «_<Int_» N M
    guard _Val0
    return N

def _98e343b : SortInt → SortInt → Option SortInt
  | N, M => do
    let _Val0 <- «_>=Int_» N M
    guard _Val0
    return M

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

mutual
  noncomputable def _74101af : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C CS, B => do
      let _Val0 <- «nextBalance(_,_)_VERIFICATION_Int_Int_Int» C B
      let _Val1 <- «scanBalance(_,_)_VERIFICATION_Int_IntSeq_Int» CS _Val0
      return _Val1
    | _, _ => none

  noncomputable def «scanBalance(_,_)_VERIFICATION_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_74101af x0 x1) <|> (_ea089d4 x0 x1)
end

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

mutual
  def _9d4e6c3 : SortIntSeq → SortVal → Option SortVal
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C CS, _OLD => do
      let _Val0 <- «scanLast(_,_)_VERIFICATION_Val_IntSeq_Val» CS ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
      return _Val0
    | _, _ => none

  def «scanLast(_,_)_VERIFICATION_Val_IntSeq_Val» (x0 : SortIntSeq) (x1 : SortVal) : Option SortVal := (_9d4e6c3 x0 x1) <|> (_ca87757 x0 x1)
end

def «nextMinimum(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_13745ee x0 x1) <|> (_98e343b x0 x1)

mutual
  def _8bf27ee : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C CS => do
      let _Val0 <- «_==Int_» C 40
      let _Val1 <- «_==Int_» C 41
      let _Val2 <- _orBool_ _Val0 _Val1
      let _Val3 <- «parenCodes(_)_VERIFICATION_Bool_IntSeq» CS
      let _Val4 <- _andBool_ _Val2 _Val3
      return _Val4
    | _ => none

  def «parenCodes(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_8bf27ee x0) <|> (_f7c7415 x0)
end

mutual
  noncomputable def _20cc248 : SortIntSeq → SortInt → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C CS, B, M => do
      let _Val0 <- «nextBalance(_,_)_VERIFICATION_Int_Int_Int» C B
      let _Val1 <- «nextBalance(_,_)_VERIFICATION_Int_Int_Int» C B
      let _Val2 <- «nextMinimum(_,_)_VERIFICATION_Int_Int_Int» _Val1 M
      let _Val3 <- «scanMinimum(_,_,_)_VERIFICATION_Int_IntSeq_Int_Int» CS _Val0 _Val2
      return _Val3
    | _, _, _ => none

  noncomputable def «scanMinimum(_,_,_)_VERIFICATION_Int_IntSeq_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_20cc248 x0 x1 x2) <|> (_abb83a5 x0 x1 x2)
end

noncomputable def _82c98b9 : SortIntSeq → Option SortBool
  | CS => do
    let _Val0 <- «scanBalance(_,_)_VERIFICATION_Int_IntSeq_Int» CS 0
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «scanMinimum(_,_,_)_VERIFICATION_Int_IntSeq_Int_Int» CS 0 0
    let _Val3 <- «_>=Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    return _Val4

noncomputable def «goodParens(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := _82c98b9 x0

noncomputable def _791f9a4 : SortIntSeq → SortIntSeq → Option SortBool
  | A, B => do
    let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» A B
    let _Val1 <- «goodParens(_)_VERIFICATION_Bool_IntSeq» _Val0
    let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» B A
    let _Val3 <- «goodParens(_)_VERIFICATION_Bool_IntSeq» _Val2
    let _Val4 <- _orBool_ _Val1 _Val3
    return _Val4

noncomputable def «possibleMatch(_,_)_VERIFICATION_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := _791f9a4 x0 x1

noncomputable def _81918ea : SortIntSeq → SortIntSeq → Option SortStr
  | A, B => do
    let _Val0 <- «possibleMatch(_,_)_VERIFICATION_Bool_IntSeq_IntSeq» A B
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 78 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 111 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))

noncomputable def _a8dfd6e : SortIntSeq → SortIntSeq → Option SortStr
  | A, B => do
    let _Val0 <- «possibleMatch(_,_)_VERIFICATION_Bool_IntSeq_IntSeq» A B
    guard _Val0
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 89 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 101 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 115 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))))

noncomputable def «matchAnswer(_,_)_VERIFICATION_Str_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortStr := (_81918ea x0 x1) <|> (_a8dfd6e x0 x1)