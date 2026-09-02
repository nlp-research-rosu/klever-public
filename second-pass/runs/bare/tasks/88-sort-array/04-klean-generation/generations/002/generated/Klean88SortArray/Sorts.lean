import Klean88SortArray.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortIntList : Type where
  | «cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» (x0 : SortInt) (x1 : SortIntList) : SortIntList
  | «nil_MPY-SYNTAX_IntList» : SortIntList

inductive SortExpr : Type where
  | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
  | «BoolOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
  | «Call(_,_,_)_MPY-SYNTAX_Expr_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
  | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
  | «CmpOp(_,_)_MPY-SYNTAX_Expr_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortExpr
  | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
  | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
  | «KwArg(_,_)_MPY-SYNTAX_Expr_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortExpr
  | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
  | «Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
  | «UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortExpr

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_String» (x0 : SortString) : SortParams

inductive SortVal : Type where
  | «BoolVal(_)_MPY-SYNTAX_Val_Bool» (x0 : SortBool) : SortVal
  | «IntVal(_)_MPY-SYNTAX_Val_Int» (x0 : SortInt) : SortVal
  | «ListVal(_)_MPY-SYNTAX_Val_IntList» (x0 : SortIntList) : SortVal
  | «NoneVal_MPY-SYNTAX_Val» : SortVal

inductive SortStmt : Type where
  | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmt» (x0 : SortString) (x1 : SortParams) (x2 : SortStmt) : SortStmt
  | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt

structure SortResultCell : Type where
  val : SortVal

structure SortInputCell : Type where
  val : SortVal

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
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortIntList (x : SortIntList) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPyCell (x : SortPyCell) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortVal (x : SortVal) : SortKItem
    | «#kxExport0(_)_MPY-KLEAN-EXPORT_KItem_IntList» (x0 : SortIntList) : SortKItem
    | «#kxExport1(_)_MPY-KLEAN-EXPORT_KItem_IntList» (x0 : SortIntList) : SortKItem
    | «#kxExport2(_)_MPY-KLEAN-EXPORT_KItem_IntList» (x0 : SortIntList) : SortKItem
    | «#kxExport3(_)_MPY-KLEAN-EXPORT_KItem_IntList» (x0 : SortIntList) : SortKItem
    | «#kxExport4(_)_MPY-KLEAN-EXPORT_KItem_IntList» (x0 : SortIntList) : SortKItem
    | «execute(_,_)_MPY_KItem_Stmt_Map» (x0 : SortStmt) (x1 : SortMap) : SortKItem
    | «finish(_)_MPY_KItem_Val» (x0 : SortVal) : SortKItem
    | «invoke(_,_)_MPY_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortPyCell : Type where
    k : SortKCell
    input : SortInputCell
    result : SortResultCell
end