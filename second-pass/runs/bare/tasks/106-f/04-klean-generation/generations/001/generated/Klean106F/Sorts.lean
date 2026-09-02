import Klean106F.Prelude

structure SortInputCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «ListExpr(_)_MPY-SYNTAX_Expr_Exprs» (x0 : SortExprs) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr

  inductive SortExprs : Type where
    | «.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs» : SortExprs
    | «_,__MPY-SYNTAX_Exprs_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExprs
end

inductive SortStrings : Type where
  | «.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings» : SortStrings
  | «_,__MPY-SYNTAX_Strings_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStrings

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_Strings» (x0 : SortStrings) : SortParams

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt
    | «While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

mutual
  structure SortEnvCell : Type where
    val : SortMap

  structure SortGeneratedTopCell : Type where
    py : SortPyCell
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
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortList (x : SortList) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPyCell (x : SortPyCell) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStrings (x : SortStrings) : SortKItem
    | inj_SortValue (x : SortValue) : SortKItem
    | «binLeft(_,_)_SEMANTIC_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «binRight(_,_)_SEMANTIC_KItem_String_Value» (x0 : SortString) (x1 : SortValue) : SortKItem
    | «cmpLeft(_,_)_SEMANTIC_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «cmpRight(_,_)_SEMANTIC_KItem_String_Value» (x0 : SortString) (x1 : SortValue) : SortKItem
    | doReturn_SEMANTIC_KItem : SortKItem
    | «eval(_)_SEMANTIC_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «exec(_)_SEMANTIC_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «ifBranch(_,_)_SEMANTIC_KItem_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) : SortKItem
    | singleton_SEMANTIC_KItem : SortKItem
    | «store(_)_SEMANTIC_KItem_String» (x0 : SortString) : SortKItem
    | «whileBranch(_,_)_SEMANTIC_KItem_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortKItem

  structure SortList : Type where
    coll : List SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortPyCell : Type where
    k : SortKCell
    input : SortInputCell
    env : SortEnvCell
    result : SortResultCell

  inductive SortResult : Type where
    | «done(_)_SEMANTIC_Result_Value» (x0 : SortValue) : SortResult
    | noResult_SEMANTIC_Result : SortResult

  structure SortResultCell : Type where
    val : SortResult

  inductive SortValue : Type where
    | «boolVal(_)_SEMANTIC_Value_Bool» (x0 : SortBool) : SortValue
    | «intVal(_)_SEMANTIC_Value_Int» (x0 : SortInt) : SortValue
    | «listVal(_)_SEMANTIC_Value_List» (x0 : SortList) : SortValue
end