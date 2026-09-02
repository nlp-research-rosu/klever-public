import Klean156IntToMiniRoman.Prelude

structure SortInputCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MINI-PYTHON-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Int(_)_MINI-PYTHON-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MINI-PYTHON-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Str(_)_MINI-PYTHON-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Subscript(_,_)_MINI-PYTHON-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
    | «TupleExpr(_)_MINI-PYTHON-SYNTAX_Expr_Exprs» (x0 : SortExprs) : SortExpr

  inductive SortExprs : Type where
    | «.List{"_,__MINI-PYTHON-SYNTAX_Exprs_Expr_Exprs"}_Exprs» : SortExprs
    | «_,__MINI-PYTHON-SYNTAX_Exprs_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExprs
end

inductive SortStrings : Type where
  | «.List{"_,__MINI-PYTHON-SYNTAX_Strings_String_Strings"}_Strings» : SortStrings
  | «_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStrings

inductive SortValue : Type where
  | «vInt(_)_MINI-PYTHON_Value_Int» (x0 : SortInt) : SortValue
  | «vStr(_)_MINI-PYTHON_Value_String» (x0 : SortString) : SortValue
  | «vTuple(_)_MINI-PYTHON_Value_Strings» (x0 : SortStrings) : SortValue

inductive SortParams : Type where
  | «Params(_)_MINI-PYTHON-SYNTAX_Params_Strings» (x0 : SortStrings) : SortParams

inductive SortResult : Type where
  | «noResult_MINI-PYTHON_Result» : SortResult
  | «result(_)_MINI-PYTHON_Result_Value» (x0 : SortValue) : SortResult

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MINI-PYTHON-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «FuncDef(_,_,_)_MINI-PYTHON-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «Return(_)_MINI-PYTHON-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MINI-PYTHON-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MINI-PYTHON-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

structure SortResultCell : Type where
  val : SortResult

mutual
  structure SortEnvCell : Type where
    val : SortMap

  structure SortGeneratedTopCell : Type where
    miniPython : SortMiniPythonCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMiniPythonCell (x : SortMiniPythonCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStrings (x : SortStrings) : SortKItem
    | inj_SortValue (x : SortValue) : SortKItem
    | «#kxExport0(_)_ROMAN-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «assignTo(_)_MINI-PYTHON_KItem_String» (x0 : SortString) : SortKItem
    | «binLeft(_,_)_MINI-PYTHON_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «binRight(_,_)_MINI-PYTHON_KItem_String_Value» (x0 : SortString) (x1 : SortValue) : SortKItem
    | «eval(_)_MINI-PYTHON_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «exec(_)_MINI-PYTHON_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «returning_MINI-PYTHON_KItem» : SortKItem
    | «stmt(_)_MINI-PYTHON_KItem_Stmt» (x0 : SortStmt) : SortKItem
    | «subscriptApply(_)_MINI-PYTHON_KItem_Value» (x0 : SortValue) : SortKItem
    | «subscriptIndex(_)_MINI-PYTHON_KItem_Expr» (x0 : SortExpr) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMiniPythonCell : Type where
    k : SortKCell
    input : SortInputCell
    env : SortEnvCell
    result : SortResultCell
end