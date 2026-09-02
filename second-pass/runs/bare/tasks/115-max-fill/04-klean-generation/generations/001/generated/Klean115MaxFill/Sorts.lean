import Klean115MaxFill.Prelude

inductive SortParamList : Type where
  | «.List{"_,__MPY-SYNTAX_ParamList_String_ParamList"}_ParamList» : SortParamList
  | «_,__MPY-SYNTAX_ParamList_String_ParamList» (x0 : SortString) (x1 : SortParamList) : SortParamList

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortCmpOps : Type where
    | «.List{"_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps"}_CmpOps» : SortCmpOps
    | «_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps» (x0 : SortCmpOp) (x1 : SortCmpOps) : SortCmpOps

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_ExprList» (x0 : SortExpr) (x1 : SortExprList) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOps» (x0 : SortExpr) (x1 : SortCmpOps) : SortExpr
    | «IfExp(_,_,_)_MPY-SYNTAX_Expr_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «ListExpr(_)_MPY-SYNTAX_Expr_ExprList» (x0 : SortExprList) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (x0 : SortExpr) (x1 : SortIndex) : SortExpr

  inductive SortExprList : Type where
    | «.List{"_,__MPY-SYNTAX_ExprList_Expr_ExprList"}_ExprList» : SortExprList
    | «_,__MPY-SYNTAX_ExprList_Expr_ExprList» (x0 : SortExpr) (x1 : SortExprList) : SortExprList

  inductive SortIndex : Type where
    | inj_SortExpr (x : SortExpr) : SortIndex
end

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortInts : Type where
  | «.List{"_,__MPY_Ints_Int_Ints"}_Ints» : SortInts
  | «_,__MPY_Ints_Int_Ints» (x0 : SortInt) (x1 : SortInts) : SortInts

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_ParamList» (x0 : SortParamList) : SortParams

inductive SortExprs : Type where
  | «exprs(_)_MPY_Exprs_ExprList» (x0 : SortExprList) : SortExprs

inductive SortRow : Type where
  | «rowVal(_)_MPY_Row_Ints» (x0 : SortInts) : SortRow

mutual
  inductive SortStmt : Type where
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

inductive SortRows : Type where
  | «.List{"_,__MPY_Rows_Row_Rows"}_Rows» : SortRows
  | «_,__MPY_Rows_Row_Rows» (x0 : SortRow) (x1 : SortRows) : SortRows

inductive SortFunction : Type where
  | «function(_,_)_MPY_Function_Params_Stmts» (x0 : SortParams) (x1 : SortStmts) : SortFunction

inductive SortModule : Type where
  | «Module(_)_MPY-SYNTAX_Module_Stmts» (x0 : SortStmts) : SortModule

mutual
  inductive SortVal : Type where
    | inj_SortRow (x : SortRow) : SortVal
    | «boolVal(_)_MPY_Val_Bool» (x0 : SortBool) : SortVal
    | «gridVal(_)_MPY_Val_Rows» (x0 : SortRows) : SortVal
    | «intVal(_)_MPY_Val_Int» (x0 : SortInt) : SortVal
    | «listVal(_)_MPY_Val_Vals» (x0 : SortVals) : SortVal
    | noneVal_MPY_Val : SortVal

  inductive SortVals : Type where
    | «.List{"_,__MPY_Vals_Val_Vals"}_Vals» : SortVals
    | «_,__MPY_Vals_Val_Vals» (x0 : SortVal) (x1 : SortVals) : SortVals
end

structure SortArgsCell : Type where
  val : SortVals

inductive SortArgVals : Type where
  | «arg(_,_)_MPY_ArgVals_Val_ArgVals» (x0 : SortVal) (x1 : SortArgVals) : SortArgVals
  | noArgs_MPY_ArgVals : SortArgVals

structure SortResultCell : Type where
  val : SortVal

mutual
  structure SortEnvCell : Type where
    val : SortMap

  structure SortFunctionsCell : Type where
    val : SortMap

  structure SortGeneratedTopCell : Type where
    maxFill : SortMaxFillCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortArgVals (x : SortArgVals) : SortKItem
    | inj_SortArgsCell (x : SortArgsCell) : SortKItem
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortCmpOps (x : SortCmpOps) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortExprList (x : SortExprList) : SortKItem
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortFunction (x : SortFunction) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortIndex (x : SortIndex) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortInts (x : SortInts) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMaxFillCell (x : SortMaxFillCell) : SortKItem
    | inj_SortModule (x : SortModule) : SortKItem
    | inj_SortParamList (x : SortParamList) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortRow (x : SortRow) : SortKItem
    | inj_SortRows (x : SortRows) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortVal (x : SortVal) : SortKItem
    | inj_SortVals (x : SortVals) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Module» (x0 : SortModule) : SortKItem
    | «binApply(_,_)_MPY_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem
    | «binRight(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «chooseBranch(_,_)_MPY_KItem_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortKItem
    | «collectCallArg(_,_,_)_MPY_KItem_String_Exprs_ArgVals» (x0 : SortString) (x1 : SortExprs) (x2 : SortArgVals) : SortKItem
    | «collectListItem(_,_)_MPY_KItem_Exprs_ArgVals» (x0 : SortExprs) (x1 : SortArgVals) : SortKItem
    | compareEmpty_MPY_KItem : SortKItem
    | «evalCallArgs(_,_,_)_MPY_KItem_String_Exprs_ArgVals» (x0 : SortString) (x1 : SortExprs) (x2 : SortArgVals) : SortKItem
    | «evalListItems(_,_)_MPY_KItem_Exprs_ArgVals» (x0 : SortExprs) (x1 : SortArgVals) : SortKItem
    | «invoke(_,_)_MPY_KItem_String_ArgVals» (x0 : SortString) (x1 : SortArgVals) : SortKItem
    | «restoreEnv(_)_MPY_KItem_Map» (x0 : SortMap) : SortKItem
    | «sliceFrom(_)_MPY_KItem_Int» (x0 : SortInt) : SortKItem
    | «subscriptApply(_)_MPY_KItem_Val» (x0 : SortVal) : SortKItem
    | «subscriptIndex(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMaxFillCell : Type where
    k : SortKCell
    args : SortArgsCell
    functions : SortFunctionsCell
    env : SortEnvCell
    result : SortResultCell
end