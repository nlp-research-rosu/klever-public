import Klean107EvenOddPalindrome.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «TupleExpr(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
end

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_String» (x0 : SortString) : SortParams

inductive SortValue : Type where
  | «VBool(_)_MPY_Value_Bool» (x0 : SortBool) : SortValue
  | «VInt(_)_MPY_Value_Int» (x0 : SortInt) : SortValue
  | «VTuple(_,_)_MPY_Value_Value_Value» (x0 : SortValue) (x1 : SortValue) : SortValue

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

inductive SortReturnState : Type where
  | noReturn_MPY_ReturnState : SortReturnState
  | «returned(_)_MPY_ReturnState_Value» (x0 : SortValue) : SortReturnState

inductive SortPgm : Type where
  | «Module(_)_MPY-SYNTAX_Pgm_Stmts» (x0 : SortStmts) : SortPgm

structure SortReturnCell : Type where
  val : SortReturnState

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
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPgm (x : SortPgm) : SortKItem
    | inj_SortReturnCell (x : SortReturnCell) : SortKItem
    | inj_SortReturnState (x : SortReturnState) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortValue (x : SortValue) : SortKItem
    | «exec(_)_MPY_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «expect(_,_)_VERIFICATION_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem
    | finish_MPY_KItem : SortKItem
    | «run(_,_)_MPY_KItem_Pgm_Int» (x0 : SortPgm) (x1 : SortInt) : SortKItem
    | verified_VERIFICATION_KItem : SortKItem
    | «verifyRange(_,_,_,_,_)_VERIFICATION_KItem_Pgm_Int_Int_Int_Int» (x0 : SortPgm) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    env : SortEnvCell
    «return» : SortReturnCell
end