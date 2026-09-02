import Klean29FilterByPrefix.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortStrings : Type where
  | «.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings» : SortStrings
  | «_,__MPY-SYNTAX_Strings_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStrings

structure SortPrefixCell : Type where
  val : SortString

inductive SortStrList : Type where
  | «cons(_,_)_MPY-SYNTAX_StrList_String_StrList» (x0 : SortString) (x1 : SortStrList) : SortStrList
  | «nil_MPY-SYNTAX_StrList» : SortStrList

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_Strings» (x0 : SortStrings) : SortParams

inductive SortVal : Type where
  | «boolVal(_)_MPY-SYNTAX_Val_Bool» (x0 : SortBool) : SortVal
  | «boundRef(_,_)_MPY-SYNTAX_Val_String_String» (x0 : SortString) (x1 : SortString) : SortVal
  | «boundString(_,_)_MPY-SYNTAX_Val_String_String» (x0 : SortString) (x1 : SortString) : SortVal
  | «listVal(_)_MPY-SYNTAX_Val_StrList» (x0 : SortStrList) : SortVal
  | «noneVal_MPY-SYNTAX_Val» : SortVal
  | «strVal(_)_MPY-SYNTAX_Val_String» (x0 : SortString) : SortVal

structure SortInputCell : Type where
  val : SortStrList

inductive SortExpr : Type where
  | inj_SortVal (x : SortVal) : SortExpr
  | «Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» (x0 : SortExpr) (x1 : SortString) : SortExpr
  | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
  | «ListExpr()_MPY-SYNTAX_Expr» : SortExpr
  | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr

inductive SortOutput : Type where
  | inj_SortVal (x : SortVal) : SortOutput
  | «noOutput_MPY-SYNTAX_Output» : SortOutput

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «Expr(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt
    | «For(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortStmts) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | «ImportFrom(_,_)_MPY-SYNTAX_Stmt_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

structure SortOutputCell : Type where
  val : SortOutput

inductive SortModule : Type where
  | «Module(_)_MPY-SYNTAX_Module_Stmts» (x0 : SortStmts) : SortModule

mutual
  structure SortEnvCell : Type where
    val : SortMap

  structure SortFunctionsCell : Type where
    val : SortMap

  structure SortGeneratedTopCell : Type where
    t : SortTCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortModule (x : SortModule) : SortKItem
    | inj_SortOutput (x : SortOutput) : SortKItem
    | inj_SortOutputCell (x : SortOutputCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPrefixCell (x : SortPrefixCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortStrList (x : SortStrList) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStrings (x : SortStrings) : SortKItem
    | inj_SortTCell (x : SortTCell) : SortKItem
    | inj_SortVal (x : SortVal) : SortKItem
    | «#kxExport0(_,_,_)_VERIFICATION-KLEAN-EXPORT_KItem_StrList_String_StrList» (x0 : SortStrList) (x1 : SortString) (x2 : SortStrList) : SortKItem
    | «#kxExport1(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_StrList_String» (x0 : SortStrList) (x1 : SortString) : SortKItem
    | «#kxExport2_VERIFICATION-KLEAN-EXPORT_KItem» : SortKItem
    | «#kxExport3_VERIFICATION-KLEAN-EXPORT_KItem» : SortKItem
    | «apply(_)_MPY_KItem_Val» (x0 : SortVal) : SortKItem
    | «assignTo(_)_MPY_KItem_String» (x0 : SortString) : SortKItem
    | bindStartsWith_MPY_KItem : SortKItem
    | «callArg(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «choose(_,_)_MPY_KItem_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) : SortKItem
    | discard_MPY_KItem : SortKItem
    | doReturn_MPY_KItem : SortKItem
    | functionEnd_MPY_KItem : SortKItem
    | launch_MPY_KItem : SortKItem
    | «loop(_,_,_)_MPY_KItem_String_Stmts_StrList» (x0 : SortString) (x1 : SortStmts) (x2 : SortStrList) : SortKItem
    | «startFor(_,_)_MPY_KItem_String_Stmts» (x0 : SortString) (x1 : SortStmts) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortTCell : Type where
    k : SortKCell
    env : SortEnvCell
    functions : SortFunctionsCell
    input : SortInputCell
    «prefix» : SortPrefixCell
    output : SortOutputCell
end