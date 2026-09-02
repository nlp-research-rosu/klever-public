import Klean109MoveOneBall.Inj

def _105572a : SortK → Option SortBool
  | K => some false

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _d0a8392 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

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

def _a66427b : SortValSeq → SortInt → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0, 0 => some V
  | _, _ => none

def _aef5b46 : SortVal → SortValSeq → Option SortVal
  | P, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some P
  | _, _ => none

def _f316b87 : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt K) SortK.dotk => some K
  | _ => none

def _fb428d2 : SortInt → SortVal → SortValSeq → Option SortInt
  | D, _Gen0, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some D
  | _, _, _ => none

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

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

noncomputable def _0e44bc5 : SortValSeq → Option SortBool
  | VS => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) VS) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) SortValSeq.«.ValSeq_MPY-CORE_ValSeq») SortK.dotk)
    guard _Val0
    return true

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _86fc1c7 : SortValSeq → SortInt → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S, I => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» S _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  def «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortVal := (_86fc1c7 x0 x1) <|> (_a66427b x0 x1)
end

mutual
  def «lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq» (x0 : SortVal) (x1 : SortValSeq) : Option SortVal := (_a5ec672 x0 x1) <|> (_aef5b46 x0 x1)

  def _a5ec672 : SortVal → SortValSeq → Option SortVal
    | _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- «lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq» V R
      return _Val0
    | _, _ => none
end

def «project:Int» (x0 : SortK) : Option SortInt := _f316b87 x0

mutual
  def _01539d8 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allInts(_)_VERIFICATION_Bool_ValSeq» R
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allInts(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_01539d8 x0) <|> (_d0a8392 x0)
end

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

mutual
  def _65ca7b2 : SortInt → SortVal → SortValSeq → Option SortInt
    | D, P, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) P) SortK.dotk)
      let _Val1 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val2 <- _andBool_ _Val0 _Val1
      let _Val3 <- «project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val4 <- «project:Int» (SortK.kseq ((@inj SortVal SortKItem) P) SortK.dotk)
      let _Val5 <- «_<Int_» _Val3 _Val4
      let _Val6 <- kite _Val5 1 0
      let _Val7 <- «_+Int_» D _Val6
      let _Val8 <- «scanDrops(_,_,_)_VERIFICATION_Int_Int_Val_ValSeq» _Val7 V R
      guard _Val2
      return _Val8
    | _, _, _ => none

  def «scanDrops(_,_,_)_VERIFICATION_Int_Int_Val_ValSeq» (x0 : SortInt) (x1 : SortVal) (x2 : SortValSeq) : Option SortInt := (_65ca7b2 x0 x1 x2) <|> (_fb428d2 x0 x1 x2)
end

noncomputable def _533b873 : SortValSeq → Option SortBool
  | VS => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) VS) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) SortValSeq.«.ValSeq_MPY-CORE_ValSeq») SortK.dotk)
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «allInts(_)_VERIFICATION_Bool_ValSeq» VS
    let _Val3 <- _andBool_ _Val1 _Val2
    let _Val4 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» VS 0
    let _Val5 <- «scanDrops(_,_,_)_VERIFICATION_Int_Int_Val_ValSeq» 0 _Val4 VS
    let _Val6 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» VS 0
    let _Val7 <- «project:Int» (SortK.kseq ((@inj SortVal SortKItem) _Val6) SortK.dotk)
    let _Val8 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» VS 0
    let _Val9 <- «lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq» _Val8 VS
    let _Val10 <- «project:Int» (SortK.kseq ((@inj SortVal SortKItem) _Val9) SortK.dotk)
    let _Val11 <- «_<Int_» _Val7 _Val10
    let _Val12 <- kite _Val11 1 0
    let _Val13 <- «_+Int_» _Val5 _Val12
    let _Val14 <- «_<=Int_» _Val13 1
    guard _Val3
    return _Val14

noncomputable def «moveSpec(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_0e44bc5 x0) <|> (_533b873 x0)