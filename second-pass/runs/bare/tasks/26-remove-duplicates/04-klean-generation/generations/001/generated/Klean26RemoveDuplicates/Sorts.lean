import Klean26RemoveDuplicates.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortInts : Type where
  | «.List{"_,__MPY_Ints_Int_Ints"}_Ints» : SortInts
  | «_,__MPY_Ints_Int_Ints» (x0 : SortInt) (x1 : SortInts) : SortInts

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortCmpOps : Type where
    | «.List{"_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps"}_CmpOps» : SortCmpOps
    | «_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps» (x0 : SortCmpOp) (x1 : SortCmpOps) : SortCmpOps

  inductive SortCompFor : Type where
    | «CompFor(_,_,_)_MPY-SYNTAX_CompFor_Expr_Expr_Exprs» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortExprs) : SortCompFor

  inductive SortCompFors : Type where
    | «.List{"___MPY-SYNTAX_CompFors_CompFor_CompFors"}_CompFors» : SortCompFors
    | «___MPY-SYNTAX_CompFors_CompFor_CompFors» (x0 : SortCompFor) (x1 : SortCompFors) : SortCompFors

  inductive SortExpr : Type where
    | «Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» (x0 : SortExpr) (x1 : SortString) : SortExpr
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOps» (x0 : SortExpr) (x1 : SortCmpOps) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «ListComp(_,_)_MPY-SYNTAX_Expr_Expr_CompFors» (x0 : SortExpr) (x1 : SortCompFors) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr

  inductive SortExprs : Type where
    | «.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs» : SortExprs
    | «_,__MPY-SYNTAX_Exprs_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExprs
end

inductive SortStrings : Type where
  | «.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings» : SortStrings
  | «_,__MPY-SYNTAX_Strings_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStrings

inductive SortPyVal : Type where
  | «boolValue(_)_MPY_PyVal_Bool» (x0 : SortBool) : SortPyVal
  | «intValue(_)_MPY_PyVal_Int» (x0 : SortInt) : SortPyVal
  | «listValue(_)_MPY_PyVal_Ints» (x0 : SortInts) : SortPyVal

inductive SortFreeVars : Type where
  | «FreeVars(_)_MPY-SYNTAX_FreeVars_Strings» (x0 : SortStrings) : SortFreeVars

inductive SortCellVars : Type where
  | «CellVars(_)_MPY-SYNTAX_CellVars_Strings» (x0 : SortStrings) : SortCellVars

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_Strings» (x0 : SortStrings) : SortParams

inductive SortEnv : Type where
  | «bind(_,_,_)_MPY_Env_String_PyVal_Env» (x0 : SortString) (x1 : SortPyVal) (x2 : SortEnv) : SortEnv
  | emptyEnv_MPY_Env : SortEnv

structure SortInputCell : Type where
  val : SortPyVal

structure SortOutputCell : Type where
  val : SortPyVal

mutual
  inductive SortStmt : Type where
    | «FuncDef(_,_,_,_,_)_MPY-SYNTAX_Stmt_String_Params_CellVars_FreeVars_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortCellVars) (x3 : SortFreeVars) (x4 : SortStmts) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «ImportFrom(_,_)_MPY-SYNTAX_Stmt_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

structure SortEnvCell : Type where
  val : SortEnv

inductive SortFunction : Type where
  | «closure(_,_)_MPY_Function_String_Stmts» (x0 : SortString) (x1 : SortStmts) : SortFunction
  | noFunction_MPY_Function : SortFunction

structure SortFunctionCell : Type where
  val : SortFunction

mutual
  structure SortGeneratedTopCell : Type where
    py : SortPyCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortCellVars (x : SortCellVars) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortCmpOps (x : SortCmpOps) : SortKItem
    | inj_SortCompFor (x : SortCompFor) : SortKItem
    | inj_SortCompFors (x : SortCompFors) : SortKItem
    | inj_SortEnv (x : SortEnv) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortFreeVars (x : SortFreeVars) : SortKItem
    | inj_SortFunction (x : SortFunction) : SortKItem
    | inj_SortFunctionCell (x : SortFunctionCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortInts (x : SortInts) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortOutputCell (x : SortOutputCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPyCell (x : SortPyCell) : SortKItem
    | inj_SortPyVal (x : SortPyVal) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStrings (x : SortStrings) : SortKItem
    | «emitComputed(_,_)_MPY_KItem_Bool_Int» (x0 : SortBool) (x1 : SortInt) : SortKItem
    | «execFunction(_)_MPY_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «execModule(_)_MPY_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | startEntry_MPY_KItem : SortKItem
    | «walkComp(_,_,_,_,_)_MPY_KItem_Ints_String_Expr_Expr_Env» (x0 : SortInts) (x1 : SortString) (x2 : SortExpr) (x3 : SortExpr) (x4 : SortEnv) : SortKItem

  structure SortPyCell : Type where
    k : SortKCell
    input : SortInputCell
    function : SortFunctionCell
    env : SortEnvCell
    output : SortOutputCell
end