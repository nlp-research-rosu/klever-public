import Klean148Bf.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Str(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «TupleExpr(_)_MPY-SYNTAX_Expr_Exprs» (x0 : SortExprs) : SortExpr

  inductive SortExprs : Type where
    | «.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs» : SortExprs
    | «_,__MPY-SYNTAX_Exprs_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExprs
end

structure SortPlanet1Cell : Type where
  val : SortString

inductive SortNames : Type where
  | «.List{"_,__MPY-SYNTAX_Names_String_Names"}_Names» : SortNames
  | «_,__MPY-SYNTAX_Names_String_Names» (x0 : SortString) (x1 : SortNames) : SortNames

structure SortPlanet2Cell : Type where
  val : SortString

inductive SortStringValues : Type where
  | «.List{"_,__MPY_StringValues_String_StringValues"}_StringValues» : SortStringValues
  | «_,__MPY_StringValues_String_StringValues» (x0 : SortString) (x1 : SortStringValues) : SortStringValues

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_Names» (x0 : SortNames) : SortParams

inductive SortResult : Type where
  | noResult_MPY_Result : SortResult
  | «tupleValue(_)_MPY_Result_StringValues» (x0 : SortStringValues) : SortResult

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

mutual
  structure SortBfCell : Type where
    k : SortKCell
    planet1 : SortPlanet1Cell
    planet2 : SortPlanet2Cell
    result : SortResultCell

  structure SortGeneratedTopCell : Type where
    bf : SortBfCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortBfCell (x : SortBfCell) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortNames (x : SortNames) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPlanet1Cell (x : SortPlanet1Cell) : SortKItem
    | inj_SortPlanet2Cell (x : SortPlanet2Cell) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStringValues (x : SortStringValues) : SortKItem
    | «#systemResult» (x0 : SortInt) (x1 : SortString) (x2 : SortString) : SortKItem
    | «execStmt(_)_MPY_KItem_Stmt» (x0 : SortStmt) : SortKItem
    | «invokeBF(_,_)_MPY_KItem_String_String» (x0 : SortString) (x1 : SortString) : SortKItem
    | «verifyBF(_,_)_VERIFICATION_KItem_String_String» (x0 : SortString) (x1 : SortString) : SortKItem
end