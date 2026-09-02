import Klean101WordsString.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

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
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortList (x : SortList) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_String» (x0 : SortString) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_String» (x0 : SortString) : SortKItem

  structure SortList : Type where
    coll : List SortKItem
end