import Klean64VowelsCount.Inj

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

def _9f02755 : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

def _5a819d8 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _f69553d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
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

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

mutual
  def _3a4bf2f : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  def «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_3a4bf2f x0 x1) <|> (_5a819d8 x0 x1) <|> (_f69553d x0 x1)
end

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def _38142ad : SortIntSeq → SortIntSeq → Option SortBool
  | P, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => do
    let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return false
  | _, _ => none

def _56a27c9 : SortIntSeq → SortIntSeq → Option SortBool
  | P, X => do
    let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P X
    guard _Val0
    return true

def _4865897 : SortVal → Option SortInt
  | SortVal.inj_SortBool B => do
    let _Val0 <- kite B 1 0
    return _Val0
  | _ => none

mutual
  def «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_38142ad x0 x1) <|> (_56a27c9 x0 x1) <|> (_e133ba2 x0 x1)

  def _e133ba2 : SortIntSeq → SortIntSeq → Option SortBool
    | P, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C Xs => do
      let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C Xs)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P Xs
      guard _Val1
      return _Val2
    | _, _ => none
end

def «intOf(_)_MPY-BUILTINS_Int_Val» (x0 : SortVal) : Option SortInt := (_4865897 x0) <|> (_9f02755 x0)

noncomputable def _2c1e248 : SortIntSeq → SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», LAST => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) LAST) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 121 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)) SortK.dotk)
    let _Val1 <- «intOf(_)_MPY-BUILTINS_Int_Val» ((@inj SortBool SortVal) _Val0)
    let _Val2 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) LAST) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 89 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)) SortK.dotk)
    let _Val3 <- «intOf(_)_MPY-BUILTINS_Int_Val» ((@inj SortBool SortVal) _Val2)
    let _Val4 <- «_+Int_» _Val1 _Val3
    return _Val4
  | _, _ => none

mutual
  noncomputable def _57ea5c1 : SortIntSeq → SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST, _LAST => do
      let _Val0 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 97 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 101 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 105 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 111 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 117 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 65 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 69 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 73 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 79 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 85 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))))))))))
      let _Val1 <- «intOf(_)_MPY-BUILTINS_Int_Val» ((@inj SortBool SortVal) _Val0)
      let _Val2 <- «vowelsTail(_,_)_VERIFICATION_Int_IntSeq_IntSeq» REST (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val3 <- «_+Int_» _Val1 _Val2
      return _Val3
    | _, _ => none

  noncomputable def «vowelsTail(_,_)_VERIFICATION_Int_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortInt := (_2c1e248 x0 x1) <|> (_57ea5c1 x0 x1)
end