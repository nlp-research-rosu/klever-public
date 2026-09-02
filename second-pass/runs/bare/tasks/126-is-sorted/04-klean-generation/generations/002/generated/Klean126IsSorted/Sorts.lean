import Klean126IsSorted.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortIntList : Type where
  | cons (x0 : SortInt) (x1 : SortIntList) : SortIntList
  | nil : SortIntList

mutual
  structure SortGeneratedTopCell : Type where
    k : SortKCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortIntList (x : SortIntList) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_IntList» (x0 : SortIntList) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_IntList» (x0 : SortIntList) : SortKItem
    | «#kxExport2(_)_VERIFICATION-KLEAN-EXPORT_KItem_IntList» (x0 : SortIntList) : SortKItem
end