import Klean52BelowThreshold.Prelude

structure SortThresholdCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortIntSeq : Type where
  | «cons(_,_)_MPY-SYNTAX_IntSeq_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : SortIntSeq
  | «nil_MPY-SYNTAX_IntSeq» : SortIntSeq

inductive SortParamItems : Type where
  | «.List{"_,__MPY-SYNTAX_ParamItems_String_ParamItems"}_ParamItems» : SortParamItems
  | «_,__MPY-SYNTAX_ParamItems_String_ParamItems» (x0 : SortString) (x1 : SortParamItems) : SortParamItems

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «Bool(_)_MPY-SYNTAX_Expr_Bool» (x0 : SortBool) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
end

inductive SortResult : Type where
  | noResult_MPY_Result : SortResult
  | «result(_)_MPY_Result_Bool» (x0 : SortBool) : SortResult

structure SortInputCell : Type where
  val : SortIntSeq

inductive SortValue : Type where
  | «VBool(_)_MPY_Value_Bool» (x0 : SortBool) : SortValue
  | «VInt(_)_MPY_Value_Int» (x0 : SortInt) : SortValue
  | «VList(_)_MPY_Value_IntSeq» (x0 : SortIntSeq) : SortValue

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_ParamItems» (x0 : SortParamItems) : SortParams

structure SortResultCell : Type where
  val : SortResult

inductive SortSlot : Type where
  | «slot(_)_MPY_Slot_Value» (x0 : SortValue) : SortSlot
  | unbound_MPY_Slot : SortSlot

mutual
  inductive SortStmt : Type where
    | «For(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortStmts) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

structure SortLCell : Type where
  val : SortSlot

structure SortXCell : Type where
  val : SortSlot

structure SortTCell : Type where
  val : SortSlot

inductive SortPgm : Type where
  | «Module(_)_MPY-SYNTAX_Pgm_Stmts» (x0 : SortStmts) : SortPgm

structure SortProgramCell : Type where
  val : SortPgm

mutual
  structure SortBtCell : Type where
    k : SortKCell
    program : SortProgramCell
    input : SortInputCell
    threshold : SortThresholdCell
    l : SortLCell
    t : SortTCell
    x : SortXCell
    result : SortResultCell

  structure SortGeneratedTopCell : Type where
    bt : SortBtCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortBtCell (x : SortBtCell) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortIntSeq (x : SortIntSeq) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortLCell (x : SortLCell) : SortKItem
    | inj_SortParamItems (x : SortParamItems) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPgm (x : SortPgm) : SortKItem
    | inj_SortProgramCell (x : SortProgramCell) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortSlot (x : SortSlot) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortTCell (x : SortTCell) : SortKItem
    | inj_SortThresholdCell (x : SortThresholdCell) : SortKItem
    | inj_SortValue (x : SortValue) : SortKItem
    | inj_SortXCell (x : SortXCell) : SortKItem
    | «#kxExport0(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : SortKItem
    | boot_MPY_KItem : SortKItem
    | «cmpRight(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «cmpValues(_,_)_MPY_KItem_Value_String» (x0 : SortValue) (x1 : SortString) : SortKItem
    | «eval(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «exec(_)_MPY_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «forK(_,_)_MPY_KItem_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortKItem
    | «ifK(_,_)_MPY_KItem_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) : SortKItem
    | «loop(_,_,_)_MPY_KItem_Expr_IntSeq_Stmts» (x0 : SortExpr) (x1 : SortIntSeq) (x2 : SortStmts) : SortKItem
    | returnK_MPY_KItem : SortKItem
end