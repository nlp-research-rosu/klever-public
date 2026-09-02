import Klean3BelowZero.Prelude

inductive SortResult : Type where
  | «NoResult_MPY-SYNTAX_Result» : SortResult

structure SortBalanceCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

structure SortCurrentCell : Type where
  val : SortInt

inductive SortIntList : Type where
  | «.IntList_MPY-SYNTAX_IntList» : SortIntList
  | «cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» (x0 : SortInt) (x1 : SortIntList) : SortIntList

structure SortResultCell : Type where
  val : SortResult

inductive SortStrings : Type where
  | «.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings» : SortStrings
  | «_,__MPY-SYNTAX_Strings_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStrings

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortCmpOps : Type where
    | «.List{"_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps"}_CmpOps» : SortCmpOps
    | «_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps» (x0 : SortCmpOp) (x1 : SortCmpOps) : SortCmpOps

  inductive SortExpr : Type where
    | «Bool(_)_MPY-SYNTAX_Expr_Bool» (x0 : SortBool) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOps» (x0 : SortExpr) (x1 : SortCmpOps) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
end

structure SortInputCell : Type where
  val : SortIntList

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_Strings» (x0 : SortStrings) : SortParams

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (x0 : SortExpr) (x1 : SortString) (x2 : SortExpr) : SortStmt
    | «For(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortStmts) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | «ImportFrom(_,_)_MPY-SYNTAX_Stmt_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

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
    | inj_SortBalanceCell (x : SortBalanceCell) : SortKItem
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortCmpOps (x : SortCmpOps) : SortKItem
    | inj_SortCurrentCell (x : SortCurrentCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortIntList (x : SortIntList) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStrings (x : SortStrings) : SortKItem
    | «#kxExport0(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Int_IntList» (x0 : SortInt) (x1 : SortIntList) : SortKItem
    | «branch(_,_)_SEMANTIC_KItem_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) : SortKItem
    | doReturn_SEMANTIC_KItem : SortKItem
    | «execStmts(_)_SEMANTIC_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «loop(_)_SEMANTIC_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | setBalance_SEMANTIC_KItem : SortKItem

  structure SortMpyCell : Type where
    k : SortKCell
    input : SortInputCell
    balance : SortBalanceCell
    current : SortCurrentCell
    result : SortResultCell
end