import Klean1SeparateParenGroups.Prelude

inductive SortChar : Type where
  | «LP_MPY-SYNTAX_Char» : SortChar
  | «RP_MPY-SYNTAX_Char» : SortChar
  | «SP_MPY-SYNTAX_Char» : SortChar

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortIds : Type where
  | «.List{"_,__MPY-SYNTAX_Ids_String_Ids"}_Ids» : SortIds
  | «_,__MPY-SYNTAX_Ids_String_Ids» (x0 : SortString) (x1 : SortIds) : SortIds

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» (x0 : SortExpr) (x1 : SortString) : SortExpr
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «ListExpr()_MPY-SYNTAX_Expr» : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Str(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
end

inductive SortChars : Type where
  | «.List{"___MPY-SYNTAX_Chars_Char_Chars"}_Chars» : SortChars
  | «___MPY-SYNTAX_Chars_Char_Chars» (x0 : SortChar) (x1 : SortChars) : SortChars

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_Ids» (x0 : SortIds) : SortParams

inductive SortOutput : Type where
  | «out(_)_MPY-SYNTAX_Output_Chars» (x0 : SortChars) : SortOutput

inductive SortInput : Type where
  | «Encoded(_)_MPY-SYNTAX_Input_Chars» (x0 : SortChars) : SortInput
  | «Raw(_)_MPY-SYNTAX_Input_String» (x0 : SortString) : SortInput

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (x0 : SortExpr) (x1 : SortString) (x2 : SortExpr) : SortStmt
    | «Expr(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt
    | «For(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortStmts) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | «ImportFrom(_,_)_MPY-SYNTAX_Stmt_String_Ids» (x0 : SortString) (x1 : SortIds) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

inductive SortOutputs : Type where
  | «.List{"___MPY-SYNTAX_Outputs_Output_Outputs"}_Outputs» : SortOutputs
  | «___MPY-SYNTAX_Outputs_Output_Outputs» (x0 : SortOutput) (x1 : SortOutputs) : SortOutputs

structure SortInputCell : Type where
  val : SortInput

inductive SortProgram : Type where
  | «Module(_)_MPY-SYNTAX_Program_Stmts» (x0 : SortStmts) : SortProgram

inductive SortValue : Type where
  | «OutList(_)_MPY-SYNTAX_Value_Outputs» (x0 : SortOutputs) : SortValue
  | «SVal(_)_MPY-SYNTAX_Value_Chars» (x0 : SortChars) : SortValue
  | «none_MPY-SYNTAX_Value» : SortValue

structure SortResultCell : Type where
  val : SortValue

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
    | inj_SortChar (x : SortChar) : SortKItem
    | inj_SortChars (x : SortChars) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortIds (x : SortIds) : SortKItem
    | inj_SortInput (x : SortInput) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortOutput (x : SortOutput) : SortKItem
    | inj_SortOutputs (x : SortOutputs) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortProgram (x : SortProgram) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortValue (x : SortValue) : SortKItem
    | «#append(_)_MPY-SYNTAX_KItem_String» (x0 : SortString) : SortKItem
    | «#assign(_)_MPY-SYNTAX_KItem_String» (x0 : SortString) : SortKItem
    | «#augAssign(_,_)_MPY-SYNTAX_KItem_String_String» (x0 : SortString) (x1 : SortString) : SortKItem
    | «#boot(_)_MPY-SYNTAX_KItem_Program» (x0 : SortProgram) : SortKItem
    | «#cmpLeft(_,_)_MPY-SYNTAX_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «#cmpRight(_,_)_MPY-SYNTAX_KItem_String_Value» (x0 : SortString) (x1 : SortValue) : SortKItem
    | «#discard_MPY-SYNTAX_KItem» : SortKItem
    | «#exec(_)_MPY-SYNTAX_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «#for(_,_)_MPY-SYNTAX_KItem_String_Stmts» (x0 : SortString) (x1 : SortStmts) : SortKItem
    | «#if(_,_)_MPY-SYNTAX_KItem_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) : SortKItem
    | «#invoke(_)_MPY-SYNTAX_KItem_String» (x0 : SortString) : SortKItem
    | «#load(_)_MPY-SYNTAX_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «#loop(_,_,_)_MPY-SYNTAX_KItem_String_Chars_Stmts» (x0 : SortString) (x1 : SortChars) (x2 : SortStmts) : SortKItem
    | «#return_MPY-SYNTAX_KItem» : SortKItem
    | «#set(_,_)_MPY-SYNTAX_KItem_String_Value» (x0 : SortString) (x1 : SortValue) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    input : SortInputCell
    env : SortEnvCell
    functions : SortFunctionsCell
    result : SortResultCell
end