import Klean6ParseNestedParens.Inj

noncomputable def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

noncomputable def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

noncomputable def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

noncomputable def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def _19d6d55 : SortIntSeq → SortInt → SortInt → SortValSeq → Option SortValSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _D, _M, OUT => some OUT
  | _, _, _, _ => none

noncomputable def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

noncomputable def _3cc9d82 : SortIntSeq → SortStr → Option SortStr
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», CH => some CH
  | _, _ => none

noncomputable def _d00a451 : SortIntSeq → SortInt → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _D, M => some M
  | _, _, _ => none

noncomputable def _8c00c55 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», D => some D
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

noncomputable def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _4d015e3 : SortInt → Option SortInt
  | M => do
    let _Val0 <- «_>Int_» M 0
    guard _Val0
    return 0

noncomputable def _13bbbb9 : SortInt → SortInt → SortInt → Option SortInt
  | C, _D, M => do
    let _Val0 <- «_==Int_» C 41
    guard _Val0
    return M

noncomputable def _22df52f : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», D => do
    let _Val0 <- «_==Int_» D 0
    return _Val0
  | _, _ => none

noncomputable def _61ead3b : SortInt → SortInt → SortValSeq → Option SortValSeq
  | C, _M, OUT => do
    let _Val0 <- «_==Int_» C 40
    guard _Val0
    return OUT

noncomputable def _a3387b2 : SortInt → SortInt → SortValSeq → Option SortValSeq
  | C, _M, OUT => do
    let _Val0 <- «_==Int_» C 41
    guard _Val0
    return OUT

noncomputable def _bb15e0b : SortInt → SortInt → Option SortInt
  | C, D => do
    let _Val0 <- «_==Int_» C 41
    let _Val1 <- «_-Int_» D 1
    guard _Val0
    return _Val1

noncomputable def _92de859 : SortInt → SortInt → Option SortInt
  | D, M => do
    let _Val0 <- «_+Int_» D 1
    let _Val1 <- «_>Int_» _Val0 M
    let _Val2 <- «_+Int_» D 1
    guard _Val1
    return _Val2

noncomputable def _af22d05 : SortInt → SortInt → Option SortInt
  | C, D => do
    let _Val0 <- «_==Int_» C 40
    let _Val1 <- «_+Int_» D 1
    guard _Val0
    return _Val1

noncomputable def _32598b7 : SortInt → Option SortInt
  | M => do
    let _Val0 <- «_<=Int_» M 0
    guard _Val0
    return M

noncomputable def _72c64f8 : SortInt → SortValSeq → Option SortValSeq
  | M, OUT => do
    let _Val0 <- «_<=Int_» M 0
    guard _Val0
    return OUT

noncomputable def _7e0adfe : SortInt → SortInt → Option SortInt
  | D, M => do
    let _Val0 <- «_+Int_» D 1
    let _Val1 <- «_<=Int_» _Val0 M
    guard _Val1
    return M

mutual
  noncomputable def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  noncomputable def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

mutual
  noncomputable def «scanChar(_,_)_VERIFICATION_Str_IntSeq_Str» (x0 : SortIntSeq) (x1 : SortStr) : Option SortStr := (_3cc9d82 x0 x1) <|> (_ac46fab x0 x1)

  noncomputable def _ac46fab : SortIntSeq → SortStr → Option SortStr
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, _CH => do
      let _Val0 <- «scanChar(_,_)_VERIFICATION_Str_IntSeq_Str» R (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))
      return _Val0
    | _, _ => none
end

noncomputable def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def «delimiterDeepest(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_32598b7 x0) <|> (_4d015e3 x0)

noncomputable def «openDeepest(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_7e0adfe x0 x1) <|> (_92de859 x0 x1)

noncomputable def _2bbe4ad : SortInt → SortValSeq → Option SortValSeq
  | M, OUT => do
    let _Val0 <- «_>Int_» M 0
    let _Val1 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» OUT (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) M) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    guard _Val0
    return _Val1

noncomputable def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def _0410df7 : SortInt → SortInt → SortInt → Option SortInt
  | C, D, M => do
    let _Val0 <- «_==Int_» C 40
    let _Val1 <- «openDeepest(_,_)_VERIFICATION_Int_Int_Int» D M
    guard _Val0
    return _Val1

noncomputable def «delimiterOutput(_,_)_VERIFICATION_ValSeq_Int_ValSeq» (x0 : SortInt) (x1 : SortValSeq) : Option SortValSeq := (_2bbe4ad x0 x1) <|> (_72c64f8 x0 x1)

noncomputable def _4b26634 : SortInt → SortIntSeq → SortInt → Option SortBool
  | C, _R, _D => do
    let _Val0 <- «_=/=Int_» C 40
    let _Val1 <- «_=/=Int_» C 41
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_=/=Int_» C 32
    let _Val4 <- _andBool_ _Val2 _Val3
    guard _Val4
    return false

noncomputable def _74c055e : SortInt → SortInt → Option SortInt
  | C, D => do
    let _Val0 <- «_=/=Int_» C 40
    let _Val1 <- «_=/=Int_» C 41
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return D

noncomputable def _b6c265d : SortInt → SortInt → SortInt → Option SortInt
  | C, _D, M => do
    let _Val0 <- «_=/=Int_» C 40
    let _Val1 <- «_=/=Int_» C 41
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «delimiterDeepest(_)_VERIFICATION_Int_Int» M
    guard _Val2
    return _Val3

noncomputable def _9f67189 : SortInt → SortInt → SortValSeq → Option SortValSeq
  | C, M, OUT => do
    let _Val0 <- «_=/=Int_» C 40
    let _Val1 <- «_=/=Int_» C 41
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «delimiterOutput(_,_)_VERIFICATION_ValSeq_Int_ValSeq» M OUT
    guard _Val2
    return _Val3

axiom _008ff34 : SortInt → SortIntSeq → SortInt → Option SortBool
axiom _26bc257 : SortInt → SortIntSeq → SortInt → Option SortBool
axiom _7566f50 : SortInt → SortIntSeq → SortInt → Option SortBool
axiom «wellFormed(_,_)_VERIFICATION_Bool_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortBool
axiom «wellFormedStep(_,_,_)_VERIFICATION_Bool_Int_IntSeq_Int» (x0 : SortInt) (x1 : SortIntSeq) (x2 : SortInt) : Option SortBool
axiom _a8f4bef : SortIntSeq → SortInt → Option SortBool

noncomputable def «nextDepth(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_74c055e x0 x1) <|> (_af22d05 x0 x1) <|> (_bb15e0b x0 x1)

noncomputable def «nextDeepest(_,_,_)_VERIFICATION_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_0410df7 x0 x1 x2) <|> (_13bbbb9 x0 x1 x2) <|> (_b6c265d x0 x1 x2)

noncomputable def «nextOutput(_,_,_)_VERIFICATION_ValSeq_Int_Int_ValSeq» (x0 : SortInt) (x1 : SortInt) (x2 : SortValSeq) : Option SortValSeq := (_61ead3b x0 x1 x2) <|> (_9f67189 x0 x1 x2) <|> (_a3387b2 x0 x1 x2)

noncomputable def _a006ae4 : SortIntSeq → Option SortBool
  | CS => do
    let _Val0 <- «wellFormed(_,_)_VERIFICATION_Bool_IntSeq_Int» CS 0
    return _Val0

mutual
  noncomputable def _578c487 : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, D => do
      let _Val0 <- «nextDepth(_,_)_VERIFICATION_Int_Int_Int» C D
      let _Val1 <- «scanDepth(_,_)_VERIFICATION_Int_IntSeq_Int» R _Val0
      return _Val1
    | _, _ => none

  noncomputable def «scanDepth(_,_)_VERIFICATION_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_578c487 x0 x1) <|> (_8c00c55 x0 x1)
end

mutual
  noncomputable def «scanDeepest(_,_,_)_VERIFICATION_Int_IntSeq_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_ad85f42 x0 x1 x2) <|> (_d00a451 x0 x1 x2)

  noncomputable def _ad85f42 : SortIntSeq → SortInt → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, D, M => do
      let _Val0 <- «nextDepth(_,_)_VERIFICATION_Int_Int_Int» C D
      let _Val1 <- «nextDeepest(_,_,_)_VERIFICATION_Int_Int_Int_Int» C D M
      let _Val2 <- «scanDeepest(_,_,_)_VERIFICATION_Int_IntSeq_Int_Int» R _Val0 _Val1
      return _Val2
    | _, _, _ => none
end

mutual
  noncomputable def _08114e4 : SortIntSeq → SortInt → SortInt → SortValSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, D, M, OUT => do
      let _Val0 <- «nextDepth(_,_)_VERIFICATION_Int_Int_Int» C D
      let _Val1 <- «nextDeepest(_,_,_)_VERIFICATION_Int_Int_Int_Int» C D M
      let _Val2 <- «nextOutput(_,_,_)_VERIFICATION_ValSeq_Int_Int_ValSeq» C M OUT
      let _Val3 <- «scanOutput(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_Int_ValSeq» R _Val0 _Val1 _Val2
      return _Val3
    | _, _, _, _ => none

  noncomputable def «scanOutput(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_Int_ValSeq» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortValSeq) : Option SortValSeq := (_08114e4 x0 x1 x2 x3) <|> (_19d6d55 x0 x1 x2 x3)
end

noncomputable def «validInput(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := _a006ae4 x0

noncomputable def _565ad05 : SortIntSeq → SortInt → SortInt → SortValSeq → Option SortValSeq
  | CS, D, M, OUT => do
    let _Val0 <- «scanDeepest(_,_,_)_VERIFICATION_Int_IntSeq_Int_Int» CS D M
    let _Val1 <- «_<=Int_» _Val0 0
    let _Val2 <- «scanOutput(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_Int_ValSeq» CS D M OUT
    guard _Val1
    return _Val2

noncomputable def _9038a3d : SortIntSeq → SortInt → SortInt → SortValSeq → Option SortValSeq
  | CS, D, M, OUT => do
    let _Val0 <- «scanDeepest(_,_,_)_VERIFICATION_Int_IntSeq_Int_Int» CS D M
    let _Val1 <- «_>Int_» _Val0 0
    let _Val2 <- «scanOutput(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_Int_ValSeq» CS D M OUT
    let _Val3 <- «scanDeepest(_,_,_)_VERIFICATION_Int_IntSeq_Int_Int» CS D M
    let _Val4 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Val2 (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) _Val3) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    guard _Val1
    return _Val4

noncomputable def «finishOutput(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_Int_ValSeq» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortValSeq) : Option SortValSeq := (_565ad05 x0 x1 x2 x3) <|> (_9038a3d x0 x1 x2 x3)

noncomputable def _9249c77 : SortIntSeq → Option SortValSeq
  | CS => do
    let _Val0 <- «finishOutput(_,_,_,_)_VERIFICATION_ValSeq_IntSeq_Int_Int_ValSeq» CS 0 0 SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    return _Val0

noncomputable def «expectedDepths(_)_VERIFICATION_ValSeq_IntSeq» (x0 : SortIntSeq) : Option SortValSeq := _9249c77 x0