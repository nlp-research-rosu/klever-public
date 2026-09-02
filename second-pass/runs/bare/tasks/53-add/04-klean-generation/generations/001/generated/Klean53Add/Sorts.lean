import Klean53Add.Prelude

inductive SortPyVal : Type where
  | «pyInt(_)_SEMANTIC_PyVal_Int» (x0 : SortInt) : SortPyVal

structure SortResultCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortExpr : Type where
  | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
  | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
  | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr

inductive SortParams : Type where
  | «Params(_,_)_MPY-SYNTAX_Params_String_String» (x0 : SortString) (x1 : SortString) : SortParams

inductive SortStmt : Type where
  | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmt» (x0 : SortString) (x1 : SortParams) (x2 : SortStmt) : SortStmt
  | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

inductive SortPgm : Type where
  | «Module(_)_MPY-SYNTAX_Pgm_Stmt» (x0 : SortStmt) : SortPgm

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
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPgm (x : SortPgm) : SortKItem
    | inj_SortPyVal (x : SortPyVal) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «bind(_,_)_SEMANTIC_KItem_String_PyVal» (x0 : SortString) (x1 : SortPyVal) : SortKItem
    | «eval(_)_SEMANTIC_KItem_Expr» (x0 : SortExpr) : SortKItem
    | finishReturn_SEMANTIC_KItem : SortKItem
    | «invoke(_,_,_)_SEMANTIC_KItem_String_PyVal_PyVal» (x0 : SortString) (x1 : SortPyVal) (x2 : SortPyVal) : SortKItem
    | «load(_)_SEMANTIC_KItem_Pgm» (x0 : SortPgm) : SortKItem
    | «plusLeft(_)_SEMANTIC_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «plusRight(_)_SEMANTIC_KItem_PyVal» (x0 : SortPyVal) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    env : SortEnvCell
    functions : SortFunctionsCell
    result : SortResultCell
end