import Klean151DoubleTheDifference.Prelude

inductive SortFunctionSlot : Type where
  | «noFunction_MPY-SYNTAX_FunctionSlot» : SortFunctionSlot

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortStrings : Type where
  | «.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings» : SortStrings
  | «_,__MPY-SYNTAX_Strings_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStrings

structure SortFunctionCell : Type where
  val : SortFunctionSlot

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortCmpOps : Type where
    | «.List{"_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps"}_CmpOps» : SortCmpOps
    | «_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps» (x0 : SortCmpOp) (x1 : SortCmpOps) : SortCmpOps

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Bool(_)_MPY-SYNTAX_Expr_Bool» (x0 : SortBool) : SortExpr
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOps» (x0 : SortExpr) (x1 : SortCmpOps) : SortExpr
    | «Float(_)_MPY-SYNTAX_Expr_Float» (x0 : SortFloat) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr

  inductive SortExprs : Type where
    | «.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs» : SortExprs
    | «_,__MPY-SYNTAX_Exprs_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExprs
end

inductive SortVals : Type where
  | «boolCons(_,_)_MPY-SYNTAX_Vals_Bool_Vals» (x0 : SortBool) (x1 : SortVals) : SortVals
  | «floatCons(_,_)_MPY-SYNTAX_Vals_Float_Vals» (x0 : SortFloat) (x1 : SortVals) : SortVals
  | «intCons(_,_)_MPY-SYNTAX_Vals_Int_Vals» (x0 : SortInt) (x1 : SortVals) : SortVals
  | «listCons(_,_)_MPY-SYNTAX_Vals_Vals_Vals» (x0 : SortVals) (x1 : SortVals) : SortVals
  | «nil_MPY-SYNTAX_Vals» : SortVals

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_Strings» (x0 : SortStrings) : SortParams

inductive SortVal : Type where
  | «pyBool(_)_MPY-SYNTAX_Val_Bool» (x0 : SortBool) : SortVal
  | «pyFloat(_)_MPY-SYNTAX_Val_Float» (x0 : SortFloat) : SortVal
  | «pyInt(_)_MPY-SYNTAX_Val_Int» (x0 : SortInt) : SortVal
  | «pyList(_)_MPY-SYNTAX_Val_Vals» (x0 : SortVals) : SortVal

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «For(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortStmts) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

structure SortValueCell : Type where
  val : SortVal

structure SortTotalCell : Type where
  val : SortVal

structure SortInputCell : Type where
  val : SortVal

inductive SortResult : Type where
  | inj_SortVal (x : SortVal) : SortResult
  | «noResult_MPY-SYNTAX_Result» : SortResult

inductive SortValSlot : Type where
  | inj_SortVal (x : SortVal) : SortValSlot
  | «noValue_MPY-SYNTAX_ValSlot» : SortValSlot

structure SortResultCell : Type where
  val : SortResult

structure SortLstCell : Type where
  val : SortValSlot

mutual
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
    | inj_SortCmpOps (x : SortCmpOps) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortFloat (x : SortFloat) : SortKItem
    | inj_SortFunctionCell (x : SortFunctionCell) : SortKItem
    | inj_SortFunctionSlot (x : SortFunctionSlot) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortLstCell (x : SortLstCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPyCell (x : SortPyCell) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStrings (x : SortStrings) : SortKItem
    | inj_SortTotalCell (x : SortTotalCell) : SortKItem
    | inj_SortVal (x : SortVal) : SortKItem
    | inj_SortValSlot (x : SortValSlot) : SortKItem
    | inj_SortVals (x : SortVals) : SortKItem
    | inj_SortValueCell (x : SortValueCell) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport1(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Vals_Int» (x0 : SortVals) (x1 : SortInt) : SortKItem
    | «bind(_,_)_MPY_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem
    | «branch(_,_,_)_MPY_KItem_Bool_Stmts_Stmts» (x0 : SortBool) (x1 : SortStmts) (x2 : SortStmts) : SortKItem
    | «loop(_,_,_)_MPY_KItem_String_Val_Stmts» (x0 : SortString) (x1 : SortVal) (x2 : SortStmts) : SortKItem
    | «returnValue(_)_MPY_KItem_Val» (x0 : SortVal) : SortKItem
    | start_MPY_KItem : SortKItem

  structure SortPyCell : Type where
    k : SortKCell
    input : SortInputCell
    lst : SortLstCell
    total : SortTotalCell
    value : SortValueCell
    function : SortFunctionCell
    result : SortResultCell
end