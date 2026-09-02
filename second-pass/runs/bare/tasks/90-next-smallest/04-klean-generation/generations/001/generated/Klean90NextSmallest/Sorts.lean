import Klean90NextSmallest.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortIntList : Type where
  | «cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» (x0 : SortInt) (x1 : SortIntList) : SortIntList
  | «nil_MPY-SYNTAX_IntList» : SortIntList

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «IfExp(_,_,_)_MPY-SYNTAX_Expr_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «NoneVal_MPY-SYNTAX_Expr» : SortExpr
    | «Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
end

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_String» (x0 : SortString) : SortParams

inductive SortPyVal : Type where
  | inj_SortBool (x : SortBool) : SortPyVal
  | inj_SortInt (x : SortInt) : SortPyVal
  | «invalidIndex(_)_SEMANTIC-BASE_PyVal_Int» (x0 : SortInt) : SortPyVal
  | «iteVal(_,_,_)_SEMANTIC-BASE_PyVal_Bool_PyVal_PyVal» (x0 : SortBool) (x1 : SortPyVal) (x2 : SortPyVal) : SortPyVal
  | «none_SEMANTIC-BASE_PyVal» : SortPyVal
  | «pyList(_)_SEMANTIC-BASE_PyVal_IntList» (x0 : SortIntList) : SortPyVal
  | «pySet(_)_SEMANTIC-BASE_PyVal_IntList» (x0 : SortIntList) : SortPyVal

structure SortInputCell : Type where
  val : SortIntList

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

structure SortDistinctCell : Type where
  val : SortPyVal

inductive SortOutcome : Type where
  | inj_SortBool (x : SortBool) : SortOutcome
  | inj_SortInt (x : SortInt) : SortOutcome
  | inj_SortPyVal (x : SortPyVal) : SortOutcome
  | «noResult_SEMANTIC-BASE_Outcome» : SortOutcome

structure SortResultCell : Type where
  val : SortOutcome

mutual
  structure SortGeneratedTopCell : Type where
    mpy : SortMpyCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortDistinctCell (x : SortDistinctCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortIntList (x : SortIntList) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortOutcome (x : SortOutcome) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPyVal (x : SortPyVal) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «assignDistinct_SEMANTIC-BASE_KItem» : SortKItem
    | «cmpLeft(_,_)_SEMANTIC-BASE_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «cmpRight(_,_)_SEMANTIC-BASE_KItem_String_PyVal» (x0 : SortString) (x1 : SortPyVal) : SortKItem
    | «eval(_)_SEMANTIC-BASE_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «exec(_)_SEMANTIC-BASE_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «execStmt(_)_SEMANTIC-BASE_KItem_Stmt» (x0 : SortStmt) : SortKItem
    | «ifCondition(_,_)_SEMANTIC-BASE_KItem_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortKItem
    | «ifElse(_,_)_SEMANTIC-BASE_KItem_Bool_PyVal» (x0 : SortBool) (x1 : SortPyVal) : SortKItem
    | «ifThen(_,_)_SEMANTIC-BASE_KItem_Bool_Expr» (x0 : SortBool) (x1 : SortExpr) : SortKItem
    | «lenCall_SEMANTIC-BASE_KItem» : SortKItem
    | «returnValue_SEMANTIC-BASE_KItem» : SortKItem
    | «setCall_SEMANTIC-BASE_KItem» : SortKItem
    | «sortedCall_SEMANTIC-BASE_KItem» : SortKItem
    | «subscriptLeft(_)_SEMANTIC-BASE_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «subscriptRight(_)_SEMANTIC-BASE_KItem_IntList» (x0 : SortIntList) : SortKItem

  structure SortMpyCell : Type where
    k : SortKCell
    input : SortInputCell
    distinct : SortDistinctCell
    result : SortResultCell
end