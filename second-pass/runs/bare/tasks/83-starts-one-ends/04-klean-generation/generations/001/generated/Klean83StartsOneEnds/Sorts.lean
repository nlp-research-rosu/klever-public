import Klean83StartsOneEnds.Prelude

inductive SortControl : Type where
  | normal_MPY_Control : SortControl
  | returned_MPY_Control : SortControl

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortResult : Type where
  | noResult_MPY_Result : SortResult
  | «result(_)_MPY_Result_Int» (x0 : SortInt) : SortResult

structure SortControlCell : Type where
  val : SortControl

mutual
  inductive SortCmpOp : Type where
    | CmpOp (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | BinOp (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | Compare (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | IntExpr (x0 : SortInt) : SortExpr
    | NameExpr (x0 : SortString) : SortExpr
    | StrExpr (x0 : SortString) : SortExpr
end

inductive SortParams : Type where
  | Params (x0 : SortString) : SortParams

structure SortResultCell : Type where
  val : SortResult

mutual
  inductive SortStmt : Type where
    | ExprStmt (x0 : SortExpr) : SortStmt
    | FuncDef (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | If (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | Return (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

inductive SortFunctionValue : Type where
  | «function(_,_,_)_MPY_FunctionValue_String_String_Stmts» (x0 : SortString) (x1 : SortString) (x2 : SortStmts) : SortFunctionValue
  | noFunction_MPY_FunctionValue : SortFunctionValue

structure SortFunctionCell : Type where
  val : SortFunctionValue

mutual
  structure SortEnvCell : Type where
    val : SortMap

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
    | inj_SortControl (x : SortControl) : SortKItem
    | inj_SortControlCell (x : SortControlCell) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortFunctionCell (x : SortFunctionCell) : SortKItem
    | inj_SortFunctionValue (x : SortFunctionValue) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport2(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport3(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport4(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | endCall_MPY_KItem : SortKItem
    | «entry(_,_)_MPY_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «exec(_)_MPY_KItem_Stmts» (x0 : SortStmts) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    function : SortFunctionCell
    env : SortEnvCell
    control : SortControlCell
    result : SortResultCell
end