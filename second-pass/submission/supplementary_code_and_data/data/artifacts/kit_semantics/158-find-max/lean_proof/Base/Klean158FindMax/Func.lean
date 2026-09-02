import Klean158FindMax.Inj

def _0092bdb : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _010fe30 : SortVal → Option SortBool
  | _Gen0 => some false

def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _153a092 : SortValSeq → SortVal → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _BEST, SCORE => some SCORE
  | _, _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _28cc140 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», ACC => some ACC
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _5e2c753 : SortIntSeq → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», C => some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _80a1ae7 : SortInt → SortIntSeq → Option SortBool
  | _Gen0, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

axiom projectStrTotal (x0 : SortVal) : Option SortStr

def _b83254f : SortStr → Option SortIntSeq
  | SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS => some CS

def _c71764f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _f3f7875 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1 => some true
  | _, _ => none

def _8a57e16 : SortValSeq → SortVal → SortInt → Option SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», BEST, _SCORE => some BEST
  | _, _, _ => none

def _c4ecad8 : SortValSeq → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», SCORE => some SCORE
  | _, _ => none

def _6206d78 : SortVal → Option SortBool
  | SortVal.«ref(_)_MPY-CORE_Val_Int» _Gen0 => some true
  | _ => none

def _95cb29f : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortStr Str) SortK.dotk => some true
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

def _d5113df : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _e10ded0 : SortK → Option SortBool
  | K => some false

def _c5cf4d2 : SortValSeq → SortVal → Option SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», WORD => some WORD
  | _, _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def «snocCode(_,_)_MPY-SET_IntSeq_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortIntSeq := (_5e2c753 x0 x1) <|> (_cd5036e x0 x1)

  def _cd5036e : SortIntSeq → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H T, C => do
      let _Val0 <- «snocCode(_,_)_MPY-SET_IntSeq_IntSeq_Int» T C
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H _Val0)
    | _, _ => none
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _cc09b1d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_>Int_» A B
    guard _Val0
    return false
  | _, _ => none

def _c875e09 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_<Int_» A B
    guard _Val0
    return true
  | _, _ => none

mutual
  def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

def «codesOf(_)_VERIFICATION_IntSeq_Str» (x0 : SortStr) : Option SortIntSeq := _b83254f x0

def «isRefV(_)_MPY-CORE_Bool_Val» (x0 : SortVal) : Option SortBool := (_6206d78 x0) <|> (_010fe30 x0)

def isStr (x0 : SortK) : Option SortBool := (_95cb29f x0) <|> (_e10ded0 x0)

mutual
  def «lastWord(_,_)_VERIFICATION_Val_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortVal := (_ad18628 x0 x1) <|> (_c5cf4d2 x0 x1)

  def _ad18628 : SortValSeq → SortVal → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, _WORD => do
      let _Val0 <- «lastWord(_,_)_VERIFICATION_Val_ValSeq_Val» REST V
      return _Val0
    | _, _ => none
end

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

mutual
  def «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortBool := (_80a1ae7 x0 x1) <|> (_c27c6a9 x0 x1)

  def _c27c6a9 : SortInt → SortIntSeq → Option SortBool
    | C, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H T => do
      let _Val0 <- «_==Int_» C H
      let _Val1 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C T
      let _Val2 <- _orBool_ _Val0 _Val1
      return _Val2
    | _, _ => none
end

mutual
  def _6a28f31 : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      guard _Val0
      return _Val1
    | _, _ => none

  def «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_0092bdb x0 x1) <|> (_6a28f31 x0 x1) <|> (_c71764f x0 x1) <|> (_c875e09 x0 x1) <|> (_cc09b1d x0 x1) <|> (_f3f7875 x0 x1)
end

def _ae14dc5 : SortVal → Option SortBool
  | V => do
    let _Val0 <- isStr (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    return _Val0

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

mutual
  def _37448bb : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S, ACC => do
      let _Val0 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C ACC
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «snocCode(_,_)_MPY-SET_IntSeq_IntSeq_Int» ACC C
      let _Val3 <- «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» S _Val2
      guard _Val1
      return _Val3
    | _, _ => none

  def _5d1e314 : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S, ACC => do
      let _Val0 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C ACC
      let _Val1 <- «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» S ACC
      guard _Val0
      return _Val1
    | _, _ => none

  def «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_28cc140 x0 x1) <|> (_37448bb x0 x1) <|> (_5d1e314 x0 x1)
end

def «definedProjectStr(_)_VERIFICATION_Bool_Val» (x0 : SortVal) : Option SortBool := _ae14dc5 x0

def _a8c9961 : SortIntSeq → Option SortIntSeq
  | CS => do
    let _Val0 <- «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» CS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return _Val0

mutual
  def «allStrings(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_d5113df x0) <|> (_d696ab9 x0)

  def _d696ab9 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «definedProjectStr(_)_VERIFICATION_Bool_Val» V
      let _Val1 <- «isRefV(_)_MPY-CORE_Bool_Val» V
      let _Val2 <- notBool_ _Val1
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «allStrings(_)_VERIFICATION_Bool_ValSeq» REST
      let _Val5 <- _andBool_ _Val3 _Val4
      return _Val5
    | _ => none
end

def «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _a8c9961 x0

noncomputable def _71a68d9 : SortVal → Option SortInt
  | V => do
    let _Val0 <- projectStrTotal V
    let _Val1 <- «codesOf(_)_VERIFICATION_IntSeq_Str» _Val0
    let _Val2 <- «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» _Val1
    let _Val3 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val2
    return _Val3

noncomputable def «uniqueCount(_)_VERIFICATION_Int_Val» (x0 : SortVal) : Option SortInt := _71a68d9 x0

mutual
  noncomputable def _5f5c073 : SortValSeq → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, _SCORE => do
      let _Val0 <- «uniqueCount(_)_VERIFICATION_Int_Val» V
      let _Val1 <- «lastScore(_,_)_VERIFICATION_Int_ValSeq_Int» REST _Val0
      return _Val1
    | _, _ => none

  noncomputable def «lastScore(_,_)_VERIFICATION_Int_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortInt := (_5f5c073 x0 x1) <|> (_c4ecad8 x0 x1)
end

noncomputable def _e34391e : SortVal → SortVal → SortInt → Option SortBool
  | V, BEST, SCORE => do
    let _Val0 <- «uniqueCount(_)_VERIFICATION_Int_Val» V
    let _Val1 <- «_>Int_» _Val0 SCORE
    let _Val2 <- «uniqueCount(_)_VERIFICATION_Int_Val» V
    let _Val3 <- «_==Int_» _Val2 SCORE
    let _Val4 <- projectStrTotal V
    let _Val5 <- «codesOf(_)_VERIFICATION_IntSeq_Str» _Val4
    let _Val6 <- projectStrTotal BEST
    let _Val7 <- «codesOf(_)_VERIFICATION_IntSeq_Str» _Val6
    let _Val8 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» _Val5 _Val7
    let _Val9 <- _andBool_ _Val3 _Val8
    let _Val10 <- _orBool_ _Val1 _Val9
    return _Val10

noncomputable def «candidateWins(_,_,_)_VERIFICATION_Bool_Val_Val_Int» (x0 : SortVal) (x1 : SortVal) (x2 : SortInt) : Option SortBool := _e34391e x0 x1 x2

mutual
  noncomputable def _14c8c08 : SortValSeq → SortVal → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, BEST, SCORE => do
      let _Val0 <- «candidateWins(_,_,_)_VERIFICATION_Bool_Val_Val_Int» V BEST SCORE
      let _Val1 <- «uniqueCount(_)_VERIFICATION_Int_Val» V
      let _Val2 <- «bestScore(_,_,_)_VERIFICATION_Int_ValSeq_Val_Int» REST V _Val1
      let _Val3 <- «bestScore(_,_,_)_VERIFICATION_Int_ValSeq_Val_Int» REST BEST SCORE
      let _Val4 <- kite _Val0 _Val2 _Val3
      return _Val4
    | _, _, _ => none

  noncomputable def «bestScore(_,_,_)_VERIFICATION_Int_ValSeq_Val_Int» (x0 : SortValSeq) (x1 : SortVal) (x2 : SortInt) : Option SortInt := (_14c8c08 x0 x1 x2) <|> (_153a092 x0 x1 x2)
end

mutual
  noncomputable def _1be766e : SortValSeq → SortVal → SortInt → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, BEST, SCORE => do
      let _Val0 <- «candidateWins(_,_,_)_VERIFICATION_Bool_Val_Val_Int» V BEST SCORE
      let _Val1 <- «uniqueCount(_)_VERIFICATION_Int_Val» V
      let _Val2 <- «bestWord(_,_,_)_VERIFICATION_Val_ValSeq_Val_Int» REST V _Val1
      let _Val3 <- «bestWord(_,_,_)_VERIFICATION_Val_ValSeq_Val_Int» REST BEST SCORE
      let _Val4 <- kite _Val0 _Val2 _Val3
      return _Val4
    | _, _, _ => none

  noncomputable def «bestWord(_,_,_)_VERIFICATION_Val_ValSeq_Val_Int» (x0 : SortValSeq) (x1 : SortVal) (x2 : SortInt) : Option SortVal := (_1be766e x0 x1 x2) <|> (_8a57e16 x0 x1 x2)
end