import Klean84Solve.Prelude

structure SortInputCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Str(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
    | «TupleExpr(_)_MPY-SYNTAX_Expr_NeExprs» (x0 : SortNeExprs) : SortExpr

  inductive SortNeExprs : Type where
    | inj_SortExpr (x : SortExpr) : SortNeExprs
    | «_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (x0 : SortExpr) (x1 : SortNeExprs) : SortNeExprs
end

mutual
  inductive SortVList : Type where
    | «VCons(_,_)_MPY-SEMANTIC_VList_Value_VList» (x0 : SortValue) (x1 : SortVList) : SortVList
    | «VNil_MPY-SEMANTIC_VList» : SortVList

  inductive SortValue : Type where
    | «VInt(_)_MPY-SEMANTIC_Value_Int» (x0 : SortInt) : SortValue
    | «VStr(_)_MPY-SEMANTIC_Value_String» (x0 : SortString) : SortValue
    | «VTuple(_)_MPY-SEMANTIC_Value_VList» (x0 : SortVList) : SortValue
end

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_String» (x0 : SortString) : SortParams

inductive SortStmt : Type where
  | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

inductive SortFuncDef : Type where
  | «FuncDef(_,_,_)_MPY-SYNTAX_FuncDef_String_Params_Stmt» (x0 : SortString) (x1 : SortParams) (x2 : SortStmt) : SortFuncDef

inductive SortPgm : Type where
  | «Module(_)_MPY-SYNTAX_Pgm_FuncDef» (x0 : SortFuncDef) : SortPgm

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
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortFuncDef (x : SortFuncDef) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortNeExprs (x : SortNeExprs) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPgm (x : SortPgm) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortVList (x : SortVList) : SortKItem
    | inj_SortValue (x : SortValue) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport2(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport3(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Value_Int» (x0 : SortValue) (x1 : SortInt) : SortKItem
    | «#kxExport4(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Value_Value» (x0 : SortValue) (x1 : SortValue) : SortKItem
    | «#kxExport5(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport6(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem

  structure SortMpyCell : Type where
    k : SortKCell
    input : SortInputCell
    result : SortResultCell

  structure SortResultCell : Type where
    val : SortK
end