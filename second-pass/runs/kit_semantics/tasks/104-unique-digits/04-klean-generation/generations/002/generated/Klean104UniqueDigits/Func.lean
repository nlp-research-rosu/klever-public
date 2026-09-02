import Klean104UniqueDigits.Inj

def _0c0ff37 : SortValSeq → SortVal → Option SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», V => some V
  | _, _ => none

def _105572a : SortK → Option SortBool
  | K => some false

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

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7513d07 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _9f02755 : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

def _a2f7e4a : SortValSeq → SortValSeq → Option SortValSeq
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some ACC
  | _, _ => none

def _75a43a8 : SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», B => some B
  | _, _ => none

def _766bea6 : SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», N => some N
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
  def _464e0d3 : SortValSeq → SortVal → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS, _Gen0 => do
      let _Val0 <- «afterValue(_,_)_VERIFICATION-SYNTAX_Val_ValSeq_Val» VS V
      return _Val0
    | _, _ => none

  def «afterValue(_,_)_VERIFICATION-SYNTAX_Val_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortVal := (_0c0ff37 x0 x1) <|> (_464e0d3 x0 x1)
end

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _726d769 : SortInt → SortInt → Option SortInt
  | B, N => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return B

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

mutual
  def _2602d8c : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «integerVals(_)_VERIFICATION-SYNTAX_Bool_ValSeq» VS
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «integerVals(_)_VERIFICATION-SYNTAX_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_2602d8c x0) <|> (_7513d07 x0)
end

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

axiom _246492d : SortInt → SortInt → Option SortInt
axiom «scanBad(_,_)_VERIFICATION-SYNTAX_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _2ef3bf4 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_>Int_» N 0
    let _Val1 <- kite _Val0 0 N
    return _Val1

def _4865897 : SortVal → Option SortInt
  | SortVal.inj_SortBool B => do
    let _Val0 <- kite B 1 0
    return _Val0
  | _ => none

def «scanNumber(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : Option SortInt := _2ef3bf4 x0

def «intOf(_)_MPY-BUILTINS_Int_Val» (x0 : SortVal) : Option SortInt := (_4865897 x0) <|> (_9f02755 x0)

noncomputable def _74adbab : SortValSeq → SortVal → Option SortValSeq
  | VS, V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- «intOf(_)_MPY-BUILTINS_Int_Val» V
    let _Val2 <- «scanBad(_,_)_VERIFICATION-SYNTAX_Int_Int_Int» 0 _Val1
    let _Val3 <- «_==Int_» _Val2 0
    let _Val4 <- _andBool_ _Val0 _Val3
    let _Val5 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» VS (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    guard _Val4
    return _Val5

mutual
  noncomputable def _7f7bae2 : SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS, _Gen0 => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «intOf(_)_MPY-BUILTINS_Int_Val» V
      let _Val2 <- «scanBad(_,_)_VERIFICATION-SYNTAX_Int_Int_Int» 0 _Val1
      let _Val3 <- «afterBad(_,_)_VERIFICATION-SYNTAX_Int_ValSeq_Int» VS _Val2
      guard _Val0
      return _Val3
    | _, _ => none

  noncomputable def «afterBad(_,_)_VERIFICATION-SYNTAX_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := (_75a43a8 x0 x1) <|> (_7f7bae2 x0 x1)
end

mutual
  def _93d8adc : SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS, _Gen0 => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «intOf(_)_MPY-BUILTINS_Int_Val» V
      let _Val2 <- «scanNumber(_)_VERIFICATION-SYNTAX_Int_Int» _Val1
      let _Val3 <- «afterNumber(_,_)_VERIFICATION-SYNTAX_Int_ValSeq_Int» VS _Val2
      guard _Val0
      return _Val3
    | _, _ => none

  def «afterNumber(_,_)_VERIFICATION-SYNTAX_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := (_766bea6 x0 x1) <|> (_93d8adc x0 x1)
end

noncomputable def _af69c96 : SortValSeq → SortVal → Option SortValSeq
  | VS, V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- «intOf(_)_MPY-BUILTINS_Int_Val» V
    let _Val2 <- «scanBad(_,_)_VERIFICATION-SYNTAX_Int_Int_Int» 0 _Val1
    let _Val3 <- «_=/=Int_» _Val2 0
    let _Val4 <- _andBool_ _Val0 _Val3
    guard _Val4
    return VS

noncomputable def «appendCandidate(_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortValSeq := (_74adbab x0 x1) <|> (_af69c96 x0 x1)

mutual
  noncomputable def _55d048a : SortValSeq → SortValSeq → Option SortValSeq
    | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «appendCandidate(_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_Val» ACC V
      let _Val2 <- «collect(_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_ValSeq» _Val1 VS
      guard _Val0
      return _Val2
    | _, _ => none

  noncomputable def «collect(_,_)_VERIFICATION-SYNTAX_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_55d048a x0 x1) <|> (_a2f7e4a x0 x1)
end