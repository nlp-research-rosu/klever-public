import Klean111Histogram.Inj

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

def _fd49342 : SortValSeq → SortVal → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some false
  | _, _ => none

def _08afc32 : SortIntSeq → SortIntSeq → SortInt → SortValSeq → SortValSeq → Option SortVal
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ORIG, _M, KS, VS => some (SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» KS VS)
  | _, _, _, _, _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _3a6225a : SortIntSeq → SortInt → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _TARGET, N => some N
  | _, _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _704b125 : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

def _9002890 : SortIntSeq → SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ORIG, M => some M
  | _, _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

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

noncomputable def «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=
  some ⟨[(x0, x1)]⟩

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _0a30025 : SortValSeq → SortValSeq → SortVal → SortVal → Option SortValSeq
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen1 VR, K, V => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
    guard _Val0
    return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VR)
  | _, _, _, _ => none

noncomputable def _78864a2 : SortValSeq → SortVal → Option SortBool
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A _Gen0, K => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
    guard _Val0
    return true
  | _, _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _04b6349 : SortValSeq → SortValSeq → SortVal → SortVal → Option SortValSeq
  | _KS, VS, _K, V => do
    let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» VS (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    return _Val0

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

mutual
  noncomputable def _07ab7bb : SortValSeq → SortVal → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A R, K => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» R K
      guard _Val1
      return _Val2
    | _, _ => none

  noncomputable def «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortBool := (_07ab7bb x0 x1) <|> (_78864a2 x0 x1) <|> (_fd49342 x0 x1)
end

mutual
  def _91bd7de : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «_==Int_» C 32
      let _Val1 <- «_<=Int_» 97 C
      let _Val2 <- «_<=Int_» C 122
      let _Val3 <- _andBool_ _Val1 _Val2
      let _Val4 <- _orBool_ _Val0 _Val3
      let _Val5 <- «validHistogramInput(_)_COUNT-SUMMARY_Bool_IntSeq» R
      let _Val6 <- _andBool_ _Val4 _Val5
      return _Val6
    | _ => none

  def «validHistogramInput(_)_COUNT-SUMMARY_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_704b125 x0) <|> (_91bd7de x0)
end

mutual
  noncomputable def _1a0a867 : SortValSeq → SortValSeq → SortVal → SortVal → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A KR, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» B VR, K, V => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «dPutV(_,_,_,_)_MPY-DICT_ValSeq_ValSeq_ValSeq_Val_Val» KR VR K V
      guard _Val1
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» B _Val2)
    | _, _, _, _ => none

  noncomputable def «dPutV(_,_,_,_)_MPY-DICT_ValSeq_ValSeq_ValSeq_Val_Val» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortVal) (x3 : SortVal) : Option SortValSeq := (_0a30025 x0 x1 x2 x3) <|> (_1a0a867 x0 x1 x2 x3) <|> (_04b6349 x0 x1 x2 x3)
end

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def _4a032b9 : SortValSeq → SortVal → Option SortValSeq
  | KS, K => do
    let _Val0 <- «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» KS K
    guard _Val0
    return KS

noncomputable def _4e69e6b : SortValSeq → SortVal → Option SortValSeq
  | KS, K => do
    let _Val0 <- «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» KS K
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» KS (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» K SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    guard _Val1
    return _Val2

mutual
  def _86ee2f8 : SortIntSeq → SortInt → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H R, TARGET, N => do
      let _Val0 <- «_==Int_» H TARGET
      let _Val1 <- «_+Int_» N 1
      let _Val2 <- «countHistogramCode(_,_,_)_COUNT-SUMMARY_Int_IntSeq_Int_Int» R TARGET _Val1
      let _Val3 <- «countHistogramCode(_,_,_)_COUNT-SUMMARY_Int_IntSeq_Int_Int» R TARGET N
      let _Val4 <- kite _Val0 _Val2 _Val3
      return _Val4
    | _, _, _ => none

  def «countHistogramCode(_,_,_)_COUNT-SUMMARY_Int_IntSeq_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_3a6225a x0 x1 x2) <|> (_86ee2f8 x0 x1 x2)
end

noncomputable def «dPutK(_,_)_MPY-DICT_ValSeq_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortValSeq := (_4a032b9 x0 x1) <|> (_4e69e6b x0 x1)

mutual
  def _71242b2 : SortIntSeq → SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, ORIG, M => do
      let _Val0 <- «_==Int_» C 32
      let _Val1 <- «maxHistogramCount(_,_,_)_VERIFICATION_Int_IntSeq_IntSeq_Int» R ORIG M
      let _Val2 <- «countHistogramCode(_,_,_)_COUNT-SUMMARY_Int_IntSeq_Int_Int» ORIG C 0
      let _Val3 <- «_>Int_» _Val2 M
      let _Val4 <- «countHistogramCode(_,_,_)_COUNT-SUMMARY_Int_IntSeq_Int_Int» ORIG C 0
      let _Val5 <- «maxHistogramCount(_,_,_)_VERIFICATION_Int_IntSeq_IntSeq_Int» R ORIG _Val4
      let _Val6 <- «maxHistogramCount(_,_,_)_VERIFICATION_Int_IntSeq_IntSeq_Int» R ORIG M
      let _Val7 <- kite _Val3 _Val5 _Val6
      let _Val8 <- kite _Val0 _Val1 _Val7
      return _Val8
    | _, _, _ => none

  def «maxHistogramCount(_,_,_)_VERIFICATION_Int_IntSeq_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortInt) : Option SortInt := (_71242b2 x0 x1 x2) <|> (_9002890 x0 x1 x2)
end

mutual
  noncomputable def «buildHistogram(_,_,_,_,_)_VERIFICATION_Val_IntSeq_IntSeq_Int_ValSeq_ValSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortInt) (x3 : SortValSeq) (x4 : SortValSeq) : Option SortVal := (_08afc32 x0 x1 x2 x3 x4) <|> (_b4d2532 x0 x1 x2 x3 x4)

  noncomputable def _b4d2532 : SortIntSeq → SortIntSeq → SortInt → SortValSeq → SortValSeq → Option SortVal
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, ORIG, M, KS, VS => do
      let _Val0 <- «_==Int_» C 32
      let _Val1 <- «buildHistogram(_,_,_,_,_)_VERIFICATION_Val_IntSeq_IntSeq_Int_ValSeq_ValSeq» R ORIG M KS VS
      let _Val2 <- «countHistogramCode(_,_,_)_COUNT-SUMMARY_Int_IntSeq_Int_Int» ORIG C 0
      let _Val3 <- «_==Int_» _Val2 M
      let _Val4 <- «dPutK(_,_)_MPY-DICT_ValSeq_ValSeq_Val» KS ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
      let _Val5 <- «countHistogramCode(_,_,_)_COUNT-SUMMARY_Int_IntSeq_Int_Int» ORIG C 0
      let _Val6 <- «dPutV(_,_,_,_)_MPY-DICT_ValSeq_ValSeq_ValSeq_Val_Val» KS VS ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) ((@inj SortInt SortVal) _Val5)
      let _Val7 <- «buildHistogram(_,_,_,_,_)_VERIFICATION_Val_IntSeq_IntSeq_Int_ValSeq_ValSeq» R ORIG M _Val4 _Val6
      let _Val8 <- «buildHistogram(_,_,_,_,_)_VERIFICATION_Val_IntSeq_IntSeq_Int_ValSeq_ValSeq» R ORIG M KS VS
      let _Val9 <- kite _Val3 _Val7 _Val8
      let _Val10 <- kite _Val0 _Val1 _Val9
      return _Val10
    | _, _, _, _, _ => none
end

noncomputable def _9b7c0d0 : SortIntSeq → Option SortVal
  | CS => do
    let _Val0 <- «maxHistogramCount(_,_,_)_VERIFICATION_Int_IntSeq_IntSeq_Int» CS CS 0
    let _Val1 <- «buildHistogram(_,_,_,_,_)_VERIFICATION_Val_IntSeq_IntSeq_Int_ValSeq_ValSeq» CS CS _Val0 SortValSeq.«.ValSeq_MPY-CORE_ValSeq» SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    return _Val1

noncomputable def «histogramResult(_)_VERIFICATION_Val_IntSeq» (x0 : SortIntSeq) : Option SortVal := _9b7c0d0 x0