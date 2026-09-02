import Klean140FixSpaces.Inj

def _08776e6 : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», R, _P => some R
  | _, _, _ => none

def _11ba933 : SortIntSeq → SortVal → Option SortVal
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», CH => some CH
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _88a0041 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», P => some P
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
  def _8179c45 : SortIntSeq → SortVal → Option SortVal
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C CS, _CH => do
      let _Val0 <- «charAfter(_,_)_VERIFICATION_Val_IntSeq_Val» CS ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
      return _Val0
    | _, _ => none

  def «charAfter(_,_)_VERIFICATION_Val_IntSeq_Val» (x0 : SortIntSeq) (x1 : SortVal) : Option SortVal := (_11ba933 x0 x1) <|> (_8179c45 x0 x1)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _82ed500 : SortIntSeq → Option SortIntSeq
  | P => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 95 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 95 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) SortK.dotk)
    guard _Val0
    return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

noncomputable def _2e13d79 : SortIntSeq → Option SortIntSeq
  | P => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)) SortK.dotk)
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 95 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 95 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) SortK.dotk)
    let _Val2 <- notBool_ _Val1
    let _Val3 <- _andBool_ _Val0 _Val2
    guard _Val3
    return P

noncomputable def _427ad08 : SortIntSeq → Option SortIntSeq
  | P => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 95 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 95 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) P) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)) SortK.dotk)
    let _Val3 <- notBool_ _Val2
    let _Val4 <- _andBool_ _Val1 _Val3
    let _Val5 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» P (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 95 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    guard _Val4
    return _Val5

noncomputable def «pendingSpace(_)_VERIFICATION_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := (_2e13d79 x0) <|> (_427ad08 x0) <|> (_82ed500 x0)

mutual
  noncomputable def _86c1ebf : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 CS, P => do
      let _Val0 <- «pendingSpace(_)_VERIFICATION_IntSeq_IntSeq» P
      let _Val1 <- «pendingAfter(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» CS _Val0
      return _Val1
    | _, _ => none

  noncomputable def «pendingAfter(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_86c1ebf x0 x1) <|> (_88a0041 x0 x1)
end

mutual
  noncomputable def _8d9d5e9 : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 CS, R, P => do
      let _Val0 <- «pendingSpace(_)_VERIFICATION_IntSeq_IntSeq» P
      let _Val1 <- «resultAfter(_,_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» CS R _Val0
      return _Val1
    | _, _, _ => none

  noncomputable def «resultAfter(_,_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortIntSeq) : Option SortIntSeq := (_08776e6 x0 x1 x2) <|> (_8d9d5e9 x0 x1 x2)
end

noncomputable def _691c1b5 : SortIntSeq → Option SortIntSeq
  | CS => do
    let _Val0 <- «resultAfter(_,_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» CS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val1 <- «pendingAfter(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» CS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» _Val0 _Val1
    return _Val2

noncomputable def «fixedSpaces(_)_VERIFICATION_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _691c1b5 x0