import Klean145OrderByPoints.Inj

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _105572a : SortK → Option SortBool
  | K => some false

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _e2c5587 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
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

axiom sortKeyVS (x0 : SortValSeq) (x1 : SortVal) : Option SortValSeq

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _2b5f6ad : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_>=Int_» N 0
    guard _Val0
    return N

def _e174f4d : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<Int_» N 0
    let _Val1 <- «_-Int_» 0 N
    guard _Val0
    return _Val1

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

noncomputable def _e3e9bc0 : SortValSeq → Option SortValSeq
  | VS => do
    let _Val0 <- sortKeyVS VS (SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int» (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "number" SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "number") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 0))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "sign") (SortExpr.«UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» "-" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "number") (SortExpr.«UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» "-" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "number"))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "sign") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "total") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 0)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "number") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» ">=" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 10))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "total") "+" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "%" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "number") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 10))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "number") "//" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 10)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "total") (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "sign") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "number")))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)))) 0)
    return _Val0

def _6a65a9e : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» 0 N
    let _Val1 <- «_<Int_» N 10
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return N

def _f83acaf : SortInt → SortInt → Option SortInt
  | N, S => do
    let _Val0 <- «_<=Int_» 0 N
    let _Val1 <- «_<Int_» N 10
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return S

def «magnitude(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : Option SortInt := (_2b5f6ad x0) <|> (_e174f4d x0)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _72cabb6 : SortValSeq → Option SortBool
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0 => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return false
  | _ => none

noncomputable def «expectedOrder(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» (x0 : SortValSeq) : Option SortValSeq := _e3e9bc0 x0

axiom _05b79d3 : SortInt → SortInt → Option SortInt
axiom «lowerDigitSumAcc(_,_)_VERIFICATION-SYNTAX_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt
axiom _d39a443 : SortInt → SortInt → Option SortInt

axiom _1e0a26a : SortInt → Option SortInt
axiom «leadingDigit(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : Option SortInt
axiom _d8f5a48 : SortInt → Option SortInt

mutual
  def _34bae68 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt _Gen0) REST => do
      let _Val0 <- «allInts(_)_VERIFICATION-SYNTAX_Bool_ValSeq» REST
      return _Val0
    | _ => none

  def «allInts(_)_VERIFICATION-SYNTAX_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_34bae68 x0) <|> (_72cabb6 x0) <|> (_e2c5587 x0)
end

noncomputable def _4c340b5 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<Int_» N 0
    let _Val1 <- «_-Int_» 0 N
    let _Val2 <- «lowerDigitSumAcc(_,_)_VERIFICATION-SYNTAX_Int_Int_Int» _Val1 0
    guard _Val0
    return _Val2

noncomputable def _b5dab08 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_>=Int_» N 0
    let _Val1 <- «lowerDigitSumAcc(_,_)_VERIFICATION-SYNTAX_Int_Int_Int» N 0
    guard _Val0
    return _Val1

noncomputable def «lowerDigitSum(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : Option SortInt := (_4c340b5 x0) <|> (_b5dab08 x0)

noncomputable def _3fa37a0 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<Int_» N 0
    let _Val1 <- «magnitude(_)_VERIFICATION-SYNTAX_Int_Int» N
    let _Val2 <- «lowerDigitSum(_)_VERIFICATION-SYNTAX_Int_Int» _Val1
    let _Val3 <- «magnitude(_)_VERIFICATION-SYNTAX_Int_Int» N
    let _Val4 <- «leadingDigit(_)_VERIFICATION-SYNTAX_Int_Int» _Val3
    let _Val5 <- «_-Int_» _Val2 _Val4
    guard _Val0
    return _Val5

noncomputable def _be74f9b : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_>=Int_» N 0
    let _Val1 <- «magnitude(_)_VERIFICATION-SYNTAX_Int_Int» N
    let _Val2 <- «lowerDigitSum(_)_VERIFICATION-SYNTAX_Int_Int» _Val1
    let _Val3 <- «magnitude(_)_VERIFICATION-SYNTAX_Int_Int» N
    let _Val4 <- «leadingDigit(_)_VERIFICATION-SYNTAX_Int_Int» _Val3
    let _Val5 <- «_+Int_» _Val2 _Val4
    guard _Val0
    return _Val5

noncomputable def «signedDigitSum(_)_VERIFICATION-SYNTAX_Int_Int» (x0 : SortInt) : Option SortInt := (_3fa37a0 x0) <|> (_be74f9b x0)