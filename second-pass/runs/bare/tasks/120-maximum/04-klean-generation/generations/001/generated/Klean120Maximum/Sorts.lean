import Klean120Maximum.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  structure SortArgsCell : Type where
    val : SortList

  structure SortEnvCell : Type where
    val : SortMap

  structure SortGeneratedTopCell : Type where
    maximum : SortMaximumCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortArgsCell (x : SortArgsCell) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortList (x : SortList) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMaximumCell (x : SortMaximumCell) : SortKItem
    | inj_SortOutCell (x : SortOutCell) : SortKItem
    | inj_SortVal (x : SortVal) : SortKItem
    | boot_MAXIMUM_KItem : SortKItem
    | «finish(_)_MAXIMUM_KItem_Val» (x0 : SortVal) : SortKItem

  structure SortList : Type where
    coll : List SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMaximumCell : Type where
    k : SortKCell
    args : SortArgsCell
    env : SortEnvCell
    out : SortOutCell

  structure SortOutCell : Type where
    val : SortVal

  inductive SortVal : Type where
    | «intVal(_)_MAXIMUM-SYNTAX_Val_Int» (x0 : SortInt) : SortVal
    | «listVal(_)_MAXIMUM-SYNTAX_Val_List» (x0 : SortList) : SortVal
    | «noResult_MAXIMUM-SYNTAX_Val» : SortVal
end