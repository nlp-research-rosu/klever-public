import Klean150XOrY.Prelude

inductive SortIds : Type where
  | «.List{"_,__MPY-SYNTAX_Ids_String_Ids"}_Ids» : SortIds
  | «_,__MPY-SYNTAX_Ids_String_Ids» (x0 : SortString) (x1 : SortIds) : SortIds

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortCmpOps : Type where
    | «.List{"_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps"}_CmpOps» : SortCmpOps
    | «_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps» (x0 : SortCmpOp) (x1 : SortCmpOps) : SortCmpOps

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOps» (x0 : SortExpr) (x1 : SortCmpOps) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
end

inductive SortVal : Type where
  | «intVal(_)_MPY_Val_Int» (x0 : SortInt) : SortVal

structure SortYCell : Type where
  val : SortInt

structure SortXCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

structure SortNCell : Type where
  val : SortInt

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «FuncDef(_,Params(_),_)_MPY-SYNTAX_Stmt_String_Ids_Stmts» (x0 : SortString) (x1 : SortIds) (x2 : SortStmts) : SortStmt
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
    | inj_SortCmpOps (x : SortCmpOps) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortIds (x : SortIds) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortNCell (x : SortNCell) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortVal (x : SortVal) : SortKItem
    | inj_SortXCell (x : SortXCell) : SortKItem
    | inj_SortYCell (x : SortYCell) : SortKItem
    | «#kxExport0(_,_)_MPY-KLEAN-EXPORT_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem
    | «#kxExport1(_)_MPY-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport2(_,_,_)_MPY-KLEAN-EXPORT_KItem_Bool_Int_Int» (x0 : SortBool) (x1 : SortInt) (x2 : SortInt) : SortKItem
    | «binApply(_,_)_MPY_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «binLeft(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «branch(_,_,_)_MPY_KItem_Stmts_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) (x2 : SortStmts) : SortKItem
    | «cmpApply(_,_)_MPY_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «cmpLeft(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | doReturn_MPY_KItem : SortKItem
    | «eval(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «exec(_)_MPY_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «store(_)_MPY_KItem_String» (x0 : SortString) : SortKItem
    | «whileBranch(_,_,_)_MPY_KItem_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    env : SortEnvCell
    n : SortNCell
    x : SortXCell
    y : SortYCell
    result : SortResultCell

  structure SortResultCell : Type where
    val : SortK
end