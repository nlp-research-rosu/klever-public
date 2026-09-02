import Klean38DecodeCyclic.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Str(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (x0 : SortExpr) (x1 : SortIndex) : SortExpr

  inductive SortIndex : Type where
    | inj_SortExpr (x : SortExpr) : SortIndex
end

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_String» (x0 : SortString) : SortParams

inductive SortVal : Type where
  | «pyBool(_)_MPY_Val_Bool» (x0 : SortBool) : SortVal
  | «pyInt(_)_MPY_Val_Int» (x0 : SortInt) : SortVal
  | «pyStr(_)_MPY_Val_String» (x0 : SortString) : SortVal

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt
    | «While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

inductive SortResult : Type where
  | inj_SortVal (x : SortVal) : SortResult
  | noResult_MPY_Result : SortResult

inductive SortPy : Type where
  | «Module(_)_MPY-SYNTAX_Py_Stmts» (x0 : SortStmts) : SortPy

structure SortResultCell : Type where
  val : SortResult

mutual
  structure SortEnvCell : Type where
    val : SortMap

  structure SortGeneratedTopCell : Type where
    k : SortKCell
    env : SortEnvCell
    result : SortResultCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortIndex (x : SortIndex) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPy (x : SortPy) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortVal (x : SortVal) : SortKItem
    | «binApply(_,_)_MPY_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem
    | «binRight(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | builtinLen_MPY_KItem : SortKItem
    | «cmpApply(_,_)_MPY_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem
    | «cmpRight(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | doReturn_MPY_KItem : SortKItem
    | «eval(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «exec(_)_MPY_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «indexApply(_)_MPY_KItem_Val» (x0 : SortVal) : SortKItem
    | «indexRight(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «run(_,_)_MPY_KItem_Py_String» (x0 : SortPy) (x1 : SortString) : SortKItem
    | «sliceApply(_,_)_MPY_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem
    | «sliceLower(_,_)_MPY_KItem_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortKItem
    | «sliceUpper(_,_)_MPY_KItem_Expr_Val» (x0 : SortExpr) (x1 : SortVal) : SortKItem
    | «store(_)_MPY_KItem_String» (x0 : SortString) : SortKItem
    | «tailApply(_)_MPY_KItem_String» (x0 : SortString) : SortKItem
    | «tailLower(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «whileGuard(_,_)_MPY_KItem_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortKItem
    | «whileLoop(_,_)_MPY_KItem_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)
end