import Klean136LargestSmallestIntegers.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortIntSeq : Type where
  | «icon(_,_)_MPY-SYNTAX_IntSeq_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : SortIntSeq
  | «nil_MPY-SYNTAX_IntSeq» : SortIntSeq

structure SortStepsCell : Type where
  val : SortInt

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_String» (x0 : SortString) : SortParams

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  structure SortEnvCell : Type where
    val : SortMap

  inductive SortExpr : Type where
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «ListExpr(_)_MPY-SYNTAX_Expr_Exprs» (x0 : SortExprs) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «NoneVal_MPY-SYNTAX_Expr» : SortExpr
    | «TupleExpr(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
    | «Value(_)_MPY-SYNTAX_Expr_PyVal» (x0 : SortPyVal) : SortExpr

  inductive SortExprs : Type where
    | «.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs» : SortExprs
    | «_,__MPY-SYNTAX_Exprs_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExprs

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
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortIntSeq (x : SortIntSeq) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortList (x : SortList) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortProgram (x : SortProgram) : SortKItem
    | inj_SortPyVal (x : SortPyVal) : SortKItem
    | inj_SortStepsCell (x : SortStepsCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «bind(_,_)_MPY_KItem_String_PyVal» (x0 : SortString) (x1 : SortPyVal) : SortKItem
    | «bindIteration(_,_)_MPY_KItem_String_PyVal» (x0 : SortString) (x1 : SortPyVal) : SortKItem
    | «branch(_,_)_MPY_KItem_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) : SortKItem
    | «compareLeft(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «compareRight(_,_)_MPY_KItem_String_PyVal» (x0 : SortString) (x1 : SortPyVal) : SortKItem
    | «exec(_)_MPY_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «iterate(_,_,_)_MPY_KItem_String_List_Stmts» (x0 : SortString) (x1 : SortList) (x2 : SortStmts) : SortKItem
    | «iterateIntSeq(_,_,_)_MPY_KItem_String_IntSeq_Stmts» (x0 : SortString) (x1 : SortIntSeq) (x2 : SortStmts) : SortKItem
    | iterationDone_MPY_KItem : SortKItem
    | «listValue(_,_)_MPY_KItem_Exprs_List» (x0 : SortExprs) (x1 : SortList) : SortKItem
    | «loop(_,_)_MPY_KItem_String_Stmts» (x0 : SortString) (x1 : SortStmts) : SortKItem
    | «makeList(_,_)_MPY_KItem_Exprs_List» (x0 : SortExprs) (x1 : SortList) : SortKItem
    | «run(_,_)_MPY_KItem_Program_Expr» (x0 : SortProgram) (x1 : SortExpr) : SortKItem
    | «start(_)_MPY_KItem_Program» (x0 : SortProgram) : SortKItem
    | «store(_)_MPY_KItem_String» (x0 : SortString) : SortKItem
    | «tupleLeft(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «tupleRight(_)_MPY_KItem_PyVal» (x0 : SortPyVal) : SortKItem

  structure SortList : Type where
    coll : List SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    env : SortEnvCell
    steps : SortStepsCell

  inductive SortProgram : Type where
    | «Module(_)_MPY-SYNTAX_Program_Stmts» (x0 : SortStmts) : SortProgram

  inductive SortPyVal : Type where
    | «pyBool(_)_MPY-SYNTAX_PyVal_Bool» (x0 : SortBool) : SortPyVal
    | «pyIntList(_)_MPY-SYNTAX_PyVal_IntSeq» (x0 : SortIntSeq) : SortPyVal
    | «pyList(_)_MPY-SYNTAX_PyVal_List» (x0 : SortList) : SortPyVal
    | «pyTuple(_,_)_MPY-SYNTAX_PyVal_PyVal_PyVal» (x0 : SortPyVal) (x1 : SortPyVal) : SortPyVal

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