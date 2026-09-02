import Klean143WordsInSentence.Inj

def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _3c5ecf9 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», A => some A
  | _, _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _b5f8fbb : SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
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

axiom «primeLength(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool

axiom «scanLast(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq

axiom «scanOutput(_,_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortIntSeq) : Option SortIntSeq

axiom «scanWord(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

mutual
  def «revISAcc(_,_)_MPY-METHODS_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_3c5ecf9 x0 x1) <|> (_cf6961f x0 x1)

  def _cf6961f : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, A => do
      let _Val0 <- «revISAcc(_,_)_MPY-METHODS_IntSeq_IntSeq_IntSeq» R (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C A)
      return _Val0
    | _, _ => none
end

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

mutual
  def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def _390b355 : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_==Int_» C 32
    let _Val1 <- «_==Int_» C 9
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_==Int_» C 10
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «_==Int_» C 13
    let _Val6 <- _orBool_ _Val4 _Val5
    return _Val6

def _4c429fa : SortIntSeq → Option SortIntSeq
  | S => do
    let _Val0 <- «revISAcc(_,_)_MPY-METHODS_IntSeq_IntSeq_IntSeq» S SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return _Val0

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def «isWSC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _390b355 x0

def «revIS(_)_MPY-METHODS_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _4c429fa x0

noncomputable def _cd2323b : SortIntSeq → SortIntSeq → Option SortIntSeq
  | W, O => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» W
    let _Val1 <- «primeLength(_)_VERIFICATION_Bool_Int» _Val0
    let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» O W
    let _Val3 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» _Val2 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val4 <- kite _Val1 _Val3 O
    return _Val4

def _f46896b : SortIntSeq → Option SortIntSeq
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
    let _Val0 <- «isWSC(_)_MPY-METHODS_Bool_Int» C
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R)
  | _ => none

noncomputable def «emitWord(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := _cd2323b x0 x1

mutual
  def _7b2ab54 : SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «isWSC(_)_MPY-METHODS_Bool_Int» C
      let _Val1 <- «trimWS(_)_MPY-METHODS_IntSeq_IntSeq» R
      guard _Val0
      return _Val1
    | _ => none

  def «trimWS(_)_MPY-METHODS_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := (_7b2ab54 x0) <|> (_b5f8fbb x0) <|> (_f46896b x0)
end

noncomputable def _f7873f6 : SortIntSeq → Option SortIntSeq
  | CS => do
    let _Val0 <- «scanWord(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» CS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val1 <- «scanOutput(_,_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» CS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val2 <- «emitWord(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» _Val0 _Val1
    let _Val3 <- «trimWS(_)_MPY-METHODS_IntSeq_IntSeq» _Val2
    let _Val4 <- «revIS(_)_MPY-METHODS_IntSeq_IntSeq» _Val3
    let _Val5 <- «trimWS(_)_MPY-METHODS_IntSeq_IntSeq» _Val4
    let _Val6 <- «revIS(_)_MPY-METHODS_IntSeq_IntSeq» _Val5
    return _Val6

noncomputable def «sentenceResult(_)_VERIFICATION_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _f7873f6 x0