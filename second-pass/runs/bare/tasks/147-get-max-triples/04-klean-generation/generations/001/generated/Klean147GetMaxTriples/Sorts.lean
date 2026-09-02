import Klean147GetMaxTriples.Prelude

inductive SortResult : Type where
  | noResult_MPY_Result : SortResult
  | «result(_)_MPY_Result_Int» (x0 : SortInt) : SortResult

structure SortInputCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

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
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | «#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr1_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr2_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerReturn(_)_MPY-SYNTAX_Stmt_Expr0_» : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    input : SortInputCell
    env : SortEnvCell
    result : SortResultCell
end