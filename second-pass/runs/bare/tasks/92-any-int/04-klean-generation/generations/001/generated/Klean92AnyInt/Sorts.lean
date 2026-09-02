import Klean92AnyInt.Prelude

inductive SortStmts : Type

inductive SortProgram : Type where
  | «Module(_)_MPY-SYNTAX_Program_Stmts» (x0 : SortStmts) : SortProgram

inductive SortVal : Type where
  | «typeVal(_)_MPY-SYNTAX_Val_String» (x0 : SortString) : SortVal

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Bool(_)_MPY-SYNTAX_Expr_Bool» (x0 : SortBool) : SortExpr
    | «BoolOp(_,_,_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) (x3 : SortExpr) (x4 : SortExpr) : SortExpr
    | «BoolOp(_,_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) (x3 : SortExpr) : SortExpr
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
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
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortProgram (x : SortProgram) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortVal (x : SortVal) : SortKItem
    | «Invoke(_,_,_,_)_MPY-SYNTAX_KItem_Program_Val_Val_Val» (x0 : SortProgram) (x1 : SortVal) (x2 : SortVal) (x3 : SortVal) : SortKItem
    | «andThen(_)_MPY-SEMANTICS_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «binLeft(_,_)_MPY-SEMANTICS_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «binRight(_,_)_MPY-SEMANTICS_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem
    | «compareLeft(_,_)_MPY-SEMANTICS_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «compareRight(_,_)_MPY-SEMANTICS_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem
    | «eval(_)_MPY-SEMANTICS_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «exec(_)_MPY-SEMANTICS_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «finishCall_MPY-SEMANTICS_KItem» : SortKItem
    | «orThen(_)_MPY-SEMANTICS_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «typeOf_MPY-SEMANTICS_KItem» : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    env : SortEnvCell
end