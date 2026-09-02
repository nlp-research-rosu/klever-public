import Klean15StringSequence.Prelude

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
    | «Str(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
end

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_String» (x0 : SortString) : SortParams

inductive SortVal : Type where
  | «BVal(_)_MPY_Val_Bool» (x0 : SortBool) : SortVal
  | «IVal(_)_MPY_Val_Int» (x0 : SortInt) : SortVal
  | «SVal(_)_MPY_Val_String» (x0 : SortString) : SortVal

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

inductive SortFunction : Type where
  | «function(_,_)_MPY_Function_String_Stmts» (x0 : SortString) (x1 : SortStmts) : SortFunction

inductive SortModule : Type where
  | «Module(_)_MPY-SYNTAX_Module_Stmts» (x0 : SortStmts) : SortModule

mutual
  structure SortEnvCell : Type where
    val : SortMap

  structure SortFunctionsCell : Type where
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
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortFunction (x : SortFunction) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortList (x : SortList) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortModule (x : SortModule) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortStackCell (x : SortStackCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortVal (x : SortVal) : SortKItem
    | «#kxExport0(_,_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Int_Int_String» (x0 : SortInt) (x1 : SortInt) (x2 : SortString) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport2(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem
    | «#kxExport3_VERIFICATION-KLEAN-EXPORT_KItem» : SortKItem
    | «#kxExport4_VERIFICATION-KLEAN-EXPORT_KItem» : SortKItem
    | «#kxExport5_VERIFICATION-KLEAN-EXPORT_KItem» : SortKItem
    | «#kxExport6_VERIFICATION-KLEAN-EXPORT_KItem» : SortKItem
    | «#kxExport7_VERIFICATION-KLEAN-EXPORT_KItem» : SortKItem
    | «binLeft(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «binRight(_,_)_MPY_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem
    | «call(_)_MPY_KItem_String» (x0 : SortString) : SortKItem
    | «cmpLeft(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «cmpRight(_,_)_MPY_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem
    | «eval(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «exec(_)_MPY_KItem_Stmt» (x0 : SortStmt) : SortKItem
    | «functionEnd()_MPY_KItem» : SortKItem
    | «ifGuard(_,_)_MPY_KItem_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) : SortKItem
    | «init(_,_)_MPY_KItem_Module_Int» (x0 : SortModule) (x1 : SortInt) : SortKItem
    | «returning()_MPY_KItem» : SortKItem
    | «run(_)_MPY_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «store(_)_MPY_KItem_String» (x0 : SortString) : SortKItem
    | «toStr()_MPY_KItem» : SortKItem
    | «whileGuard(_,_)_MPY_KItem_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortKItem

  structure SortList : Type where
    coll : List SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    env : SortEnvCell
    functions : SortFunctionsCell
    stack : SortStackCell

  structure SortStackCell : Type where
    val : SortList
end