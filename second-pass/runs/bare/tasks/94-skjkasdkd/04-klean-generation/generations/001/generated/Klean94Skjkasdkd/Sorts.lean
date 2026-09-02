import Klean94Skjkasdkd.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortStrings : Type where
  | «.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings» : SortStrings
  | «_,__MPY-SYNTAX_Strings_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStrings

mutual
  inductive SortBound : Type where
    | inj_SortExpr (x : SortExpr) : SortBound
    | «NoBound_MPY-SYNTAX_Bound» : SortBound

  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortCmpOps : Type where
    | «.List{"_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps"}_CmpOps» : SortCmpOps
    | «_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps» (x0 : SortCmpOp) (x1 : SortCmpOps) : SortCmpOps

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Bool(_)_MPY-SYNTAX_Expr_Bool» (x0 : SortBool) : SortExpr
    | «BoolOp(_,_)_MPY-SYNTAX_Expr_String_Exprs» (x0 : SortString) (x1 : SortExprs) : SortExpr
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOps» (x0 : SortExpr) (x1 : SortCmpOps) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (x0 : SortExpr) (x1 : SortIndex) : SortExpr

  inductive SortExprs : Type where
    | «.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs» : SortExprs
    | «_,__MPY-SYNTAX_Exprs_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExprs

  inductive SortIndex : Type where
    | inj_SortExpr (x : SortExpr) : SortIndex
    | «Slice(_,_,_)_MPY-SYNTAX_Index_Bound_Bound_Bound» (x0 : SortBound) (x1 : SortBound) (x2 : SortBound) : SortIndex
end

mutual
  inductive SortVal : Type where
    | «boolVal(_)_SEMANTIC_Val_Bool» (x0 : SortBool) : SortVal
    | «intVal(_)_SEMANTIC_Val_Int» (x0 : SortInt) : SortVal
    | «listVal(_)_SEMANTIC_Val_Vals» (x0 : SortVals) : SortVal

  inductive SortVals : Type where
    | «.List{"_,__SEMANTIC_Vals_Val_Vals"}_Vals» : SortVals
    | «_,__SEMANTIC_Vals_Val_Vals» (x0 : SortVal) (x1 : SortVals) : SortVals
end

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_Strings» (x0 : SortStrings) : SortParams

inductive SortResult : Type where
  | noResult_SEMANTIC_Result : SortResult
  | «result(_)_SEMANTIC_Result_Val» (x0 : SortVal) : SortResult

mutual
  inductive SortStmt : Type where
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

structure SortResultCell : Type where
  val : SortResult

inductive SortDef : Type where
  | «def(_,_)_SEMANTIC_Def_Params_Stmts» (x0 : SortParams) (x1 : SortStmts) : SortDef

inductive SortPgm : Type where
  | «Module(_)_MPY-SYNTAX_Pgm_Stmts» (x0 : SortStmts) : SortPgm

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
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortBound (x : SortBound) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortCmpOps (x : SortCmpOps) : SortKItem
    | inj_SortDef (x : SortDef) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortIndex (x : SortIndex) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPgm (x : SortPgm) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStrings (x : SortStrings) : SortKItem
    | inj_SortVal (x : SortVal) : SortKItem
    | inj_SortVals (x : SortVals) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Pgm» (x0 : SortPgm) : SortKItem
    | «#kxExport1(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem
    | «#kxExport2(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport3(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem
    | «#kxExport4(_)_VERIFICATION-KLEAN-EXPORT_KItem_Vals» (x0 : SortVals) : SortKItem
    | «#kxExport5(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport6(_)_VERIFICATION-KLEAN-EXPORT_KItem_Vals» (x0 : SortVals) : SortKItem
    | «andLeft(_,_,_)_SEMANTIC_KItem_Expr_Map_Map» (x0 : SortExpr) (x1 : SortMap) (x2 : SortMap) : SortKItem
    | «andRight(_)_SEMANTIC_KItem_Bool» (x0 : SortBool) : SortKItem
    | «argsDone(_)_SEMANTIC_KItem_Vals» (x0 : SortVals) : SortKItem
    | «argsRest(_,_,_)_SEMANTIC_KItem_Exprs_Map_Map» (x0 : SortExprs) (x1 : SortMap) (x2 : SortMap) : SortKItem
    | «binLeft(_,_,_,_)_SEMANTIC_KItem_String_Expr_Map_Map» (x0 : SortString) (x1 : SortExpr) (x2 : SortMap) (x3 : SortMap) : SortKItem
    | «binRight(_,_)_SEMANTIC_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem
    | «callWith(_,_)_SEMANTIC_KItem_String_Map» (x0 : SortString) (x1 : SortMap) : SortKItem
    | «compareLeft(_,_,_,_)_SEMANTIC_KItem_String_Expr_Map_Map» (x0 : SortString) (x1 : SortExpr) (x2 : SortMap) (x3 : SortMap) : SortKItem
    | «compareRight(_,_)_SEMANTIC_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem
    | «eval(_,_,_)_SEMANTIC_KItem_Expr_Map_Map» (x0 : SortExpr) (x1 : SortMap) (x2 : SortMap) : SortKItem
    | «evalArgs(_,_,_)_SEMANTIC_KItem_Exprs_Map_Map» (x0 : SortExprs) (x1 : SortMap) (x2 : SortMap) : SortKItem
    | «execStmts(_,_,_)_SEMANTIC_KItem_Stmts_Map_Map» (x0 : SortStmts) (x1 : SortMap) (x2 : SortMap) : SortKItem
    | finish_SEMANTIC_KItem : SortKItem
    | «init(_,_)_SEMANTIC_KItem_Pgm_Val» (x0 : SortPgm) (x1 : SortVal) : SortKItem
    | «invoke(_,_,_)_SEMANTIC_KItem_String_Vals_Map» (x0 : SortString) (x1 : SortVals) (x2 : SortMap) : SortKItem
    | «invokeDef(_,_,_)_SEMANTIC_KItem_Def_Vals_Map» (x0 : SortDef) (x1 : SortVals) (x2 : SortMap) : SortKItem
    | «invokeProgram(_,_)_SEMANTIC_KItem_Pgm_Val» (x0 : SortPgm) (x1 : SortVal) : SortKItem
    | «prependArg(_)_SEMANTIC_KItem_Val» (x0 : SortVal) : SortKItem
    | «returnIf(_,_,_,_,_)_SEMANTIC_KItem_Stmts_Stmts_Stmts_Map_Map» (x0 : SortStmts) (x1 : SortStmts) (x2 : SortStmts) (x3 : SortMap) (x4 : SortMap) : SortKItem
    | «subscriptWith(_)_SEMANTIC_KItem_Index» (x0 : SortIndex) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    result : SortResultCell
end