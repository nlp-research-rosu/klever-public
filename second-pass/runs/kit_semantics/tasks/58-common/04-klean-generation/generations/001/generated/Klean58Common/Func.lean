import Klean58Common.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _81ec6e6 : SortValSeq → SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, ACC => some ACC
  | _, _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
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

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

noncomputable def «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=
  some ⟨[(x0, x1)]⟩

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

def _d30d59a : SortVal → SortValSeq → Option SortBool
  | _Gen0, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some false
  | _, _ => none

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

mutual
  noncomputable def «commonMember(_,_)_VERIFICATION_Bool_Val_ValSeq» (x0 : SortVal) (x1 : SortValSeq) : Option SortBool := (_d30d59a x0 x1) <|> (_e544cd4 x0 x1)

  noncomputable def _e544cd4 : SortVal → SortValSeq → Option SortBool
    | V, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» E R => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) E) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «commonMember(_,_)_VERIFICATION_Bool_Val_ValSeq» V R
      let _Val2 <- _orBool_ _Val0 _Val1
      return _Val2
    | _, _ => none
end

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

mutual
  noncomputable def «commonAcc(_,_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortValSeq) : Option SortValSeq := (_81ec6e6 x0 x1 x2) <|> (_b8436d5 x0 x1 x2)

  noncomputable def _b8436d5 : SortValSeq → SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R, B, ACC => do
      let _Val0 <- «commonMember(_,_)_VERIFICATION_Bool_Val_ValSeq» V B
      let _Val1 <- «commonMember(_,_)_VERIFICATION_Bool_Val_ValSeq» V ACC
      let _Val2 <- notBool_ _Val1
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val5 <- kite _Val3 _Val4 ACC
      let _Val6 <- «commonAcc(_,_,_)_VERIFICATION_ValSeq_ValSeq_ValSeq_ValSeq» R B _Val5
      return _Val6
    | _, _, _ => none
end