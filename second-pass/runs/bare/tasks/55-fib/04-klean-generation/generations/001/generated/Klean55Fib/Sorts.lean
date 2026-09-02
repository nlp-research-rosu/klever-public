import Klean55Fib.Prelude

structure SortArgCell : Type where
  val : SortInt

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
end

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_String» (x0 : SortString) : SortParams

mutual
  inductive SortStmt : Type where
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

mutual
  structure SortEnvCell : Type where
    val : SortMap

  structure SortFunctionsCell : Type where
    val : SortMap

  structure SortGeneratedTopCell : Type where
    python : SortPythonCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortArgCell (x : SortArgCell) : SortKItem
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPythonCell (x : SortPythonCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «applyBin(_,_)_SEMANTIC_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «applyCompare(_,_)_SEMANTIC_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «eval(_)_SEMANTIC_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «evalRight(_,_)_SEMANTIC_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «exec(_)_SEMANTIC_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «finishCompare(_,_)_SEMANTIC_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «finishIf(_,_)_SEMANTIC_KItem_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) : SortKItem
    | «functionEnd(_)_SEMANTIC_KItem_Map» (x0 : SortMap) : SortKItem
    | «invoke(_,_)_SEMANTIC_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | makeReturn_SEMANTIC_KItem : SortKItem
    | «prepareCall(_)_SEMANTIC_KItem_String» (x0 : SortString) : SortKItem
    | «returned(_)_SEMANTIC_KItem_Int» (x0 : SortInt) : SortKItem
    | topCall_SEMANTIC_KItem : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortPythonCell : Type where
    k : SortKCell
    arg : SortArgCell
    env : SortEnvCell
    functions : SortFunctionsCell
end