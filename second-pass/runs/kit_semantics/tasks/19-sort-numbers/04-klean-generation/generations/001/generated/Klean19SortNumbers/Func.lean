import Klean19SortNumbers.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _218dc3a : SortString → Option SortIntSeq
  | "" => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _2e9dd52 : SortIntSeq → SortValSeq → Option SortIntSeq
  | _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some CS
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _3a4ff4d : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
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

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

def _553ef43 : SortIntSeq → SortValSeq → Option SortIntSeq
  | _Gen0, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _, _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

axiom sortKeyVS (x0 : SortValSeq) (x1 : SortVal) : Option SortValSeq

def _a38c318 : SortValSeq → SortIntSeq → Option SortValSeq
  | ACC, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some ACC
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

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

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

def _ac76db8 : SortValSeq → SortIntSeq → Option SortValSeq
  | ACC, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C T => do
    let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C T))) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    return _Val0
  | _, _ => none

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

noncomputable def _f390a9b : SortString → SortString → Option SortBool
  | S1, S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    let _Val1 <- notBool_ _Val0
    return _Val1

mutual
  def _6dbca3c : SortIntSeq → SortValSeq → Option SortIntSeq
    | SEP, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R) => do
      let _Val0 <- «joinCodes(_,_)_MPY-METHODS_IntSeq_IntSeq_ValSeq» SEP (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R)
      let _Val1 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» SEP _Val0
      let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» CS _Val1
      return _Val2
    | _, _ => none

  def «joinCodes(_,_)_MPY-METHODS_IntSeq_IntSeq_ValSeq» (x0 : SortIntSeq) (x1 : SortValSeq) : Option SortIntSeq := (_2e9dd52 x0 x1) <|> (_553ef43 x0 x1) <|> (_6dbca3c x0 x1)
end

def «flushTok(_,_)_MPY-METHODS_ValSeq_ValSeq_IntSeq» (x0 : SortValSeq) (x1 : SortIntSeq) : Option SortValSeq := (_a38c318 x0 x1) <|> (_ac76db8 x0 x1)

def «isWSC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _390b355 x0

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

def _adaabae : SortIntSeq → SortIntSeq → SortValSeq → Option SortValSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», CUR, ACC => do
    let _Val0 <- «flushTok(_,_)_MPY-METHODS_ValSeq_ValSeq_IntSeq» ACC CUR
    return _Val0
  | _, _, _ => none

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

mutual
  def «splitWS(_,_,_)_MPY-METHODS_ValSeq_IntSeq_IntSeq_ValSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortValSeq) : Option SortValSeq := (_a8a9e75 x0 x1 x2) <|> (_adaabae x0 x1 x2) <|> (_ceeef05 x0 x1 x2)

  def _a8a9e75 : SortIntSeq → SortIntSeq → SortValSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, CUR, ACC => do
      let _Val0 <- «isWSC(_)_MPY-METHODS_Bool_Int» C
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» CUR (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val3 <- «splitWS(_,_,_)_MPY-METHODS_ValSeq_IntSeq_IntSeq_ValSeq» R _Val2 ACC
      guard _Val1
      return _Val3
    | _, _, _ => none

  def _ceeef05 : SortIntSeq → SortIntSeq → SortValSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, CUR, ACC => do
      let _Val0 <- «isWSC(_)_MPY-METHODS_Bool_Int» C
      let _Val1 <- «flushTok(_,_)_MPY-METHODS_ValSeq_ValSeq_IntSeq» ACC CUR
      let _Val2 <- «splitWS(_,_,_)_MPY-METHODS_ValSeq_IntSeq_IntSeq_ValSeq» R SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» _Val1
      guard _Val0
      return _Val2
    | _, _, _ => none
end

noncomputable def _56dab4a : SortVal → Option SortBool
  | V => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "zero"
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0)) SortK.dotk)
    let _Val2 <- «strToCodes(_)_MPY-STR_IntSeq_String» "one"
    let _Val3 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val2)) SortK.dotk)
    let _Val4 <- _orBool_ _Val1 _Val3
    let _Val5 <- «strToCodes(_)_MPY-STR_IntSeq_String» "two"
    let _Val6 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val5)) SortK.dotk)
    let _Val7 <- _orBool_ _Val4 _Val6
    let _Val8 <- «strToCodes(_)_MPY-STR_IntSeq_String» "three"
    let _Val9 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val8)) SortK.dotk)
    let _Val10 <- _orBool_ _Val7 _Val9
    let _Val11 <- «strToCodes(_)_MPY-STR_IntSeq_String» "four"
    let _Val12 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val11)) SortK.dotk)
    let _Val13 <- _orBool_ _Val10 _Val12
    let _Val14 <- «strToCodes(_)_MPY-STR_IntSeq_String» "five"
    let _Val15 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val14)) SortK.dotk)
    let _Val16 <- _orBool_ _Val13 _Val15
    let _Val17 <- «strToCodes(_)_MPY-STR_IntSeq_String» "six"
    let _Val18 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val17)) SortK.dotk)
    let _Val19 <- _orBool_ _Val16 _Val18
    let _Val20 <- «strToCodes(_)_MPY-STR_IntSeq_String» "seven"
    let _Val21 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val20)) SortK.dotk)
    let _Val22 <- _orBool_ _Val19 _Val21
    let _Val23 <- «strToCodes(_)_MPY-STR_IntSeq_String» "eight"
    let _Val24 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val23)) SortK.dotk)
    let _Val25 <- _orBool_ _Val22 _Val24
    let _Val26 <- «strToCodes(_)_MPY-STR_IntSeq_String» "nine"
    let _Val27 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortStr SortKItem) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val26)) SortK.dotk)
    let _Val28 <- _orBool_ _Val25 _Val27
    return _Val28

noncomputable def _834d567 : SortIntSeq → Option SortStr
  | CS => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» " "
    let _Val1 <- «splitWS(_,_,_)_MPY-METHODS_ValSeq_IntSeq_IntSeq_ValSeq» CS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val2 <- sortKeyVS _Val1 (SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int» (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "number" SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» (SortExpr.«TupleExpr(_)_MPY-SYNTAX_Expr_Exprs» (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "zero") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "one") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "two") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "three") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "four") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "five") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "six") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "seven") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "eight") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "nine") SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))))))))))) "index") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "number") SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») 0)
    let _Val3 <- «joinCodes(_,_)_MPY-METHODS_IntSeq_IntSeq_ValSeq» _Val0 _Val2
    return (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val3)

noncomputable def «isNumberWord(_)_VERIFICATION_Bool_Val» (x0 : SortVal) : Option SortBool := _56dab4a x0

noncomputable def «expectedSortNumbers(_)_VERIFICATION_Str_IntSeq» (x0 : SortIntSeq) : Option SortStr := _834d567 x0

mutual
  noncomputable def _4662643 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «isNumberWord(_)_VERIFICATION_Bool_Val» V
      let _Val1 <- «allNumberWords(_)_VERIFICATION_Bool_ValSeq» REST
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  noncomputable def «allNumberWords(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_3a4ff4d x0) <|> (_4662643 x0)
end