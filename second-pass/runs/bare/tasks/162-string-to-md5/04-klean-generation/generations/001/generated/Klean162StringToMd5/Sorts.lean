import Klean162StringToMd5.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» (x0 : SortExpr) (x1 : SortString) : SortExpr
    | «Call(_,)_MPY-SYNTAX_Expr_Expr» (x0 : SortExpr) : SortExpr
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «IfExp(_,_,_)_MPY-SYNTAX_Expr_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «NoneVal_MPY-SYNTAX_Expr» : SortExpr
    | «Str(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
end

structure SortInputCell : Type where
  val : SortString

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_String» (x0 : SortString) : SortParams

inductive SortPyValue : Type where
  | «pyBool(_)_SEMANTIC_PyValue_Bool» (x0 : SortBool) : SortPyValue
  | «pyBuiltin(_)_SEMANTIC_PyValue_String» (x0 : SortString) : SortPyValue
  | «pyBytes(_)_SEMANTIC_PyValue_Bytes» (x0 : SortBytes) : SortPyValue
  | «pyMethod(_,_)_SEMANTIC_PyValue_String_PyValue» (x0 : SortString) (x1 : SortPyValue) : SortPyValue
  | «pyModule(_)_SEMANTIC_PyValue_String» (x0 : SortString) : SortPyValue
  | pyNone_SEMANTIC_PyValue : SortPyValue
  | «pyString(_)_SEMANTIC_PyValue_String» (x0 : SortString) : SortPyValue

mutual
  inductive SortStmt : Type where
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «Import(_)_MPY-SYNTAX_Stmt_String» (x0 : SortString) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

inductive SortResult : Type where
  | inj_SortPyValue (x : SortPyValue) : SortResult
  | noResult_SEMANTIC_Result : SortResult

inductive SortProgram : Type where
  | «Module(_)_MPY-SYNTAX_Program_Stmts» (x0 : SortStmts) : SortProgram

structure SortResultCell : Type where
  val : SortResult

mutual
  structure SortEnvCell : Type where
    val : SortMap

  structure SortFunctionsCell : Type where
    val : SortMap

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
    | inj_SortBytes (x : SortBytes) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortProgram (x : SortProgram) : SortKItem
    | inj_SortPyCell (x : SortPyCell) : SortKItem
    | inj_SortPyValue (x : SortPyValue) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#apply0(_)_SEMANTIC_KItem_PyValue» (x0 : SortPyValue) : SortKItem
    | «#apply1(_)_SEMANTIC_KItem_PyValue» (x0 : SortPyValue) : SortKItem
    | «#attribute(_)_SEMANTIC_KItem_String» (x0 : SortString) : SortKItem
    | «#call0_SEMANTIC_KItem» : SortKItem
    | «#call1(_)_SEMANTIC_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «#compareLeft(_,_)_SEMANTIC_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «#compareRight(_,_)_SEMANTIC_KItem_String_PyValue» (x0 : SortString) (x1 : SortPyValue) : SortKItem
    | «#eval(_)_SEMANTIC_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «#functionEnd_SEMANTIC_KItem» : SortKItem
    | «#ifExp(_,_)_SEMANTIC_KItem_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortKItem
    | «#invoke(_,_)_SEMANTIC_KItem_String_PyValue» (x0 : SortString) (x1 : SortPyValue) : SortKItem
    | «#load(_)_SEMANTIC_KItem_Program» (x0 : SortProgram) : SortKItem
    | «#loadStmts(_)_SEMANTIC_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «#start_SEMANTIC_KItem» : SortKItem
    | «#systemResult» (x0 : SortInt) (x1 : SortString) (x2 : SortString) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortPyCell : Type where
    k : SortKCell
    input : SortInputCell
    functions : SortFunctionsCell
    env : SortEnvCell
    result : SortResultCell
end