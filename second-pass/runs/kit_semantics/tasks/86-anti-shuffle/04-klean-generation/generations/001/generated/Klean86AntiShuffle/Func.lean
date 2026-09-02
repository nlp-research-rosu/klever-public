import Klean86AntiShuffle.Inj

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

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _4dc6594 : Option SortStmts := some (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«BoolOp(_,_)_MPY-SYNTAX_Expr_String_Exprs» "and" (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» "not" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "inserted")) (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "char") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "old_char"))) SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "new_word") "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "char")) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "inserted") (SortExpr.«Bool(_)_MPY-SYNTAX_Expr_Bool» true)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "new_word") "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "old_char")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))

def _6f914d6 : Option SortStmts := some (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "result") "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word")) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "result")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))

def _e7c7b88 : Option SortStmts := some (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» "not" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "inserted")) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "new_word") "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "char")) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "inserted") (SortExpr.«Bool(_)_MPY-SYNTAX_Expr_Bool» true)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "new_word")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))

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

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

def «antiInnerBody()_VERIFICATION_Stmts» : Option SortStmts := _4dc6594

def «antiTail()_VERIFICATION_Stmts» : Option SortStmts := _6f914d6

def «antiPostInsert()_VERIFICATION_Stmts» : Option SortStmts := _e7c7b88

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def _d8fc915 : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», R, W => do
    let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» R W
    return _Val0
  | _, _, _ => none

def _875e284 : Option SortStmts := do
  let _Val0 <- «antiInnerBody()_VERIFICATION_Stmts»
  let _Val1 <- «antiPostInsert()_VERIFICATION_Stmts»
  return (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "char") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» " "))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "result") "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word")) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "result") "+" (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» " ")) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word") (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "new_word") (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "")) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "inserted") (SortExpr.«Bool(_)_MPY-SYNTAX_Expr_Bool» false)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«For(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "old_char") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word") _Val0) _Val1)))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def «antiOuterBody()_VERIFICATION_Stmts» : Option SortStmts := _875e284

def _9a297ab : SortIntSeq → SortInt → SortIntSeq → SortBool → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», C, A, B => do
    let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» A (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val1 <- kite B A _Val0
    return _Val1
  | _, _, _, _ => none

mutual
  def _30d8ade : SortIntSeq → SortInt → SortIntSeq → SortBool → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» OLD IS, C, A, B => do
      let _Val0 <- notBool_ B
      let _Val1 <- «_<Int_» C OLD
      let _Val2 <- _andBool_ _Val0 _Val1
      let _Val3 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» A (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val4 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» _Val3 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» OLD SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val5 <- «insertGo(_,_,_,_)_VERIFICATION_IntSeq_IntSeq_Int_IntSeq_Bool» IS C _Val4 true
      let _Val6 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» A (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» OLD SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val7 <- «insertGo(_,_,_,_)_VERIFICATION_IntSeq_IntSeq_Int_IntSeq_Bool» IS C _Val6 B
      let _Val8 <- kite _Val2 _Val5 _Val7
      return _Val8
    | _, _, _, _ => none

  def «insertGo(_,_,_,_)_VERIFICATION_IntSeq_IntSeq_Int_IntSeq_Bool» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortIntSeq) (x3 : SortBool) : Option SortIntSeq := (_30d8ade x0 x1 x2 x3) <|> (_9a297ab x0 x1 x2 x3)
end

mutual
  def _6778ade : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S, R, W => do
      let _Val0 <- «_==Int_» C 32
      let _Val1 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» R W
      let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» _Val1 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val3 <- «antiGo(_,_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» S _Val2 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
      let _Val4 <- «insertGo(_,_,_,_)_VERIFICATION_IntSeq_IntSeq_Int_IntSeq_Bool» W C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» false
      let _Val5 <- «antiGo(_,_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» S R _Val4
      let _Val6 <- kite _Val0 _Val3 _Val5
      return _Val6
    | _, _, _ => none

  def «antiGo(_,_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortIntSeq) : Option SortIntSeq := (_6778ade x0 x1 x2) <|> (_d8fc915 x0 x1 x2)
end