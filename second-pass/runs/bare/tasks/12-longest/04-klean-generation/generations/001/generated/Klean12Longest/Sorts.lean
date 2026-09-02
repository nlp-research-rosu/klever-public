import Klean12Longest.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortCmpOps : Type where
    | «.List{"_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps"}_CmpOps» : SortCmpOps
    | «_,__MPY-SYNTAX_CmpOps_CmpOp_CmpOps» (x0 : SortCmpOp) (x1 : SortCmpOps) : SortCmpOps

  inductive SortExpr : Type where
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOps» (x0 : SortExpr) (x1 : SortCmpOps) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «ListExpr(_)_MPY-SYNTAX_Expr_Exprs» (x0 : SortExprs) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «NoneVal_MPY-SYNTAX_Expr» : SortExpr
    | «Str(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr

  inductive SortExprs : Type where
    | «.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs» : SortExprs
    | «_,__MPY-SYNTAX_Exprs_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExprs
end

inductive SortStrings : Type where
  | «.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings» : SortStrings
  | «_,__MPY-SYNTAX_Strings_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStrings

mutual
  inductive SortValue : Type where
    | «boolVal(_)_MPY-SEMANTICS_Value_Bool» (x0 : SortBool) : SortValue
    | «intVal(_)_MPY-SEMANTICS_Value_Int» (x0 : SortInt) : SortValue
    | «listVal(_)_MPY-SEMANTICS_Value_Values» (x0 : SortValues) : SortValue
    | «noneVal_MPY-SEMANTICS_Value» : SortValue
    | «seqVal(_,_,_)_VERIFICATION_Value_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : SortValue
    | «strVal(_)_MPY-SEMANTICS_Value_String» (x0 : SortString) : SortValue

  inductive SortValues : Type where
    | «.List{"_,__MPY-SEMANTICS_Values_Value_Values"}_Values» : SortValues
    | «_,__MPY-SEMANTICS_Values_Value_Values» (x0 : SortValue) (x1 : SortValues) : SortValues
end

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_Strings» (x0 : SortStrings) : SortParams

structure SortArgsCell : Type where
  val : SortValue

inductive SortOutput : Type where
  | inj_SortValue (x : SortValue) : SortOutput
  | «noOutput_MPY-SEMANTICS_Output» : SortOutput

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «For(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortStmts) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | «ImportFrom(_,_)_MPY-SYNTAX_Stmt_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStmt
    | «Module(_)_MPY-SYNTAX_Stmt_Stmts» (x0 : SortStmts) : SortStmt
    | «Return()_MPY-SYNTAX_Stmt» : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

structure SortOutCell : Type where
  val : SortOutput

inductive SortFunction : Type where
  | «function(_,_)_MPY-SEMANTICS_Function_Params_Stmts» (x0 : SortParams) (x1 : SortStmts) : SortFunction
  | «noFunction_MPY-SEMANTICS_Function» : SortFunction

structure SortFunctionCell : Type where
  val : SortFunction

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
    | inj_SortArgsCell (x : SortArgsCell) : SortKItem
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortCmpOps (x : SortCmpOps) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortFunction (x : SortFunction) : SortKItem
    | inj_SortFunctionCell (x : SortFunctionCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortOutCell (x : SortOutCell) : SortKItem
    | inj_SortOutput (x : SortOutput) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStrings (x : SortStrings) : SortKItem
    | inj_SortValue (x : SortValue) : SortKItem
    | inj_SortValues (x : SortValues) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Strings» (x0 : SortStrings) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_Strings» (x0 : SortStrings) : SortKItem
    | «#kxExport2(_)_VERIFICATION-KLEAN-EXPORT_KItem_Strings» (x0 : SortStrings) : SortKItem
    | «#kxExport3(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortKItem
    | «#kxExport4(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «#kxExport5(_,_,_,_)_VERIFICATION-KLEAN-EXPORT_KItem_String_String_Int_Int» (x0 : SortString) (x1 : SortString) (x2 : SortInt) (x3 : SortInt) : SortKItem
    | «branch(_,_,_)_MPY-SEMANTICS_KItem_Value_Stmts_Stmts» (x0 : SortValue) (x1 : SortStmts) (x2 : SortStmts) : SortKItem
    | «exec(_)_MPY-SEMANTICS_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «execStmt(_)_MPY-SEMANTICS_KItem_Stmt» (x0 : SortStmt) : SortKItem
    | «forValues(_,_,_)_MPY-SEMANTICS_KItem_String_Value_Stmts» (x0 : SortString) (x1 : SortValue) (x2 : SortStmts) : SortKItem
    | «functionEnd_MPY-SEMANTICS_KItem» : SortKItem
    | «invokeEntry_MPY-SEMANTICS_KItem» : SortKItem
    | «returning(_)_MPY-SEMANTICS_KItem_Value» (x0 : SortValue) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    args : SortArgsCell
    env : SortEnvCell
    function : SortFunctionCell
    out : SortOutCell
end