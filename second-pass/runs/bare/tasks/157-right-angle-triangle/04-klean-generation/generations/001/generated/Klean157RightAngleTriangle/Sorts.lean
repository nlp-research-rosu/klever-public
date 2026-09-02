import Klean157RightAngleTriangle.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortInts : Type where
  | «.List{"_,__MPY-SYNTAX_Ints_Int_Ints"}_Ints» : SortInts
  | «_,__MPY-SYNTAX_Ints_Int_Ints» (x0 : SortInt) (x1 : SortInts) : SortInts

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «BoolOp(_,_)_MPY-SYNTAX_Expr_String_Exprs» (x0 : SortString) (x1 : SortExprs) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr

  inductive SortExprs : Type where
    | «.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs» : SortExprs
    | «_,__MPY-SYNTAX_Exprs_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExprs
end

inductive SortStrings : Type where
  | «.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings» : SortStrings
  | «_,__MPY-SYNTAX_Strings_String_Strings» (x0 : SortString) (x1 : SortStrings) : SortStrings

inductive SortResult : Type where
  | noResult_MPY_Result : SortResult
  | «result(_)_MPY_Result_Bool» (x0 : SortBool) : SortResult

structure SortResultCell : Type where
  val : SortResult

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
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortInts (x : SortInts) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStrings (x : SortStrings) : SortKItem
    | «#systemResult» (x0 : SortInt) (x1 : SortString) (x2 : SortString) : SortKItem
    | «binApply(_,_)_MPY_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «binRight(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «bind(_,_)_MPY_KItem_Strings_Ints» (x0 : SortStrings) (x1 : SortInts) : SortKItem
    | «boolMerge(_,_,_)_MPY_KItem_String_Bool_Exprs» (x0 : SortString) (x1 : SortBool) (x2 : SortExprs) : SortKItem
    | «boolTail(_,_)_MPY_KItem_String_Exprs» (x0 : SortString) (x1 : SortExprs) : SortKItem
    | «cmpApply(_,_)_MPY_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «cmpRight(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «eval(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | publish_MPY_KItem : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    env : SortEnvCell
    result : SortResultCell
end