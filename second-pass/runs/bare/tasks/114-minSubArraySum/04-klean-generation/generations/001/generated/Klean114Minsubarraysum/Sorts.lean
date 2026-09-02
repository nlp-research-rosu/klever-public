import Klean114Minsubarraysum.Prelude

inductive SortDepth : Type where
  | «s(_)_MPY-SYNTAX_Depth_Depth» (x0 : SortDepth) : SortDepth
  | «z_MPY-SYNTAX_Depth» : SortDepth

structure SortCallDepthCell : Type where
  val : SortDepth

structure SortEntryCell : Type where
  val : SortString

inductive SortStrings : Type where
  | «.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings» : SortStrings
  | «_,__MPY-SYNTAX_Strings_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStrings

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortCmpOps : Type where
    | «.List{"___MPY-SYNTAX_CmpOps_CmpOp_CmpOps"}_CmpOps» : SortCmpOps
    | «___MPY-SYNTAX_CmpOps_CmpOp_CmpOps» (x0 : SortCmpOp) (x1 : SortCmpOps) : SortCmpOps

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOps» (x0 : SortExpr) (x1 : SortCmpOps) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (x0 : SortExpr) (x1 : SortIndex) : SortExpr

  inductive SortExprs : Type where
    | «.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs» : SortExprs
    | «_,__MPY-SYNTAX_Exprs_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExprs

  inductive SortIndex : Type where
    | inj_SortExpr (x : SortExpr) : SortIndex
end

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortIntList : Type where
  | «cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» (x0 : SortInt) (x1 : SortIntList) : SortIntList
  | «nil_MPY-SYNTAX_IntList» : SortIntList

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_Strings» (x0 : SortStrings) : SortParams

inductive SortValue : Type where
  | «builtin(_)_MPY-SYNTAX_Value_String» (x0 : SortString) : SortValue
  | «funref(_)_MPY-SYNTAX_Value_String» (x0 : SortString) : SortValue
  | «pyBool(_)_MPY-SYNTAX_Value_Bool» (x0 : SortBool) : SortValue
  | «pyInt(_)_MPY-SYNTAX_Value_Int» (x0 : SortInt) : SortValue
  | «pyList(_)_MPY-SYNTAX_Value_IntList» (x0 : SortIntList) : SortValue

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

inductive SortValues : Type where
  | «.List{"_,__MPY-SYNTAX_Values_Value_Values"}_Values» : SortValues
  | «_,__MPY-SYNTAX_Values_Value_Values» (x0 : SortValue) (x1 : SortValues) : SortValues

structure SortArgsCell : Type where
  val : SortValues

mutual
  structure SortCallStackCell : Type where
    val : SortList

  structure SortEnvCell : Type where
    val : SortMap

  structure SortFunctionsCell : Type where
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
    | inj_SortArgsCell (x : SortArgsCell) : SortKItem
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortCallDepthCell (x : SortCallDepthCell) : SortKItem
    | inj_SortCallStackCell (x : SortCallStackCell) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortCmpOps (x : SortCmpOps) : SortKItem
    | inj_SortDepth (x : SortDepth) : SortKItem
    | inj_SortEntryCell (x : SortEntryCell) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortIndex (x : SortIndex) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortIntList (x : SortIntList) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortList (x : SortList) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPyCell (x : SortPyCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStrings (x : SortStrings) : SortKItem
    | inj_SortValue (x : SortValue) : SortKItem
    | inj_SortValues (x : SortValues) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_IntList» (x0 : SortIntList) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_IntList» (x0 : SortIntList) : SortKItem
    | «apply(_,_,_)_MPY_KItem_Value_Value_Value» (x0 : SortValue) (x1 : SortValue) (x2 : SortValue) : SortKItem
    | «apply(_,_)_MPY_KItem_Value_Value» (x0 : SortValue) (x1 : SortValue) : SortKItem
    | «applyOne(_)_MPY_KItem_Value» (x0 : SortValue) : SortKItem
    | «applyTwo(_,_)_MPY_KItem_Value_Value» (x0 : SortValue) (x1 : SortValue) : SortKItem
    | «binLeft(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «binRight(_,_)_MPY_KItem_String_Value» (x0 : SortString) (x1 : SortValue) : SortKItem
    | «callOne(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «callTwo(_,_)_MPY_KItem_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortKItem
    | «callTwoSecond(_,_)_MPY_KItem_Value_Expr» (x0 : SortValue) (x1 : SortExpr) : SortKItem
    | «choose(_,_)_MPY_KItem_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) : SortKItem
    | «compareLeft(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «compareRight(_,_)_MPY_KItem_String_Value» (x0 : SortString) (x1 : SortValue) : SortKItem
    | «exec(_)_MPY_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «invoke(_,_)_MPY_KItem_String_Values» (x0 : SortString) (x1 : SortValues) : SortKItem
    | listHead_MPY_KItem : SortKItem
    | «returned(_,_)_MPY_KItem_Depth_Value» (x0 : SortDepth) (x1 : SortValue) : SortKItem
    | returning_MPY_KItem : SortKItem
    | singletonTest_MPY_KItem : SortKItem
    | sliceTail_MPY_KItem : SortKItem
    | «storeName(_)_MPY_KItem_String» (x0 : SortString) : SortKItem

  structure SortList : Type where
    coll : List SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortPyCell : Type where
    k : SortKCell
    entry : SortEntryCell
    args : SortArgsCell
    functions : SortFunctionsCell
    env : SortEnvCell
    callStack : SortCallStackCell
    callDepth : SortCallDepthCell
end