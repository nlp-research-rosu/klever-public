import Klean54SameChars.Prelude

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
end

structure SortS1Cell : Type where
  val : SortString

structure SortS0Cell : Type where
  val : SortString

structure SortGeneratedCounterCell : Type where
  val : SortInt

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
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortS0Cell (x : SortS0Cell) : SortKItem
    | inj_SortS1Cell (x : SortS1Cell) : SortKItem
    | inj_SortSet (x : SortSet) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortValue (x : SortValue) : SortKItem
    | «compareRight(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «compareValues(_)_MPY_KItem_Value» (x0 : SortValue) : SortKItem
    | «eval(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | finishReturn_MPY_KItem : SortKItem
    | makeSet_MPY_KItem : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    s0 : SortS0Cell
    s1 : SortS1Cell
    env : SortEnvCell
    result : SortResultCell

  inductive SortResult : Type where
    | noResult_MPY_Result : SortResult
    | «result(_)_MPY_Result_Value» (x0 : SortValue) : SortResult

  structure SortResultCell : Type where
    val : SortResult

  structure SortSet : Type where
    coll : List SortKItem

  inductive SortValue : Type where
    | «boolValue(_)_MPY_Value_Bool» (x0 : SortBool) : SortValue
    | «setValue(_)_MPY_Value_Set» (x0 : SortSet) : SortValue
    | «stringValue(_)_MPY_Value_String» (x0 : SortString) : SortValue
end