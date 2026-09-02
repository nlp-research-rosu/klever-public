import Klean110Exchange.Prelude

inductive SortPyList : Type where
  | Cons (x0 : SortInt) (x1 : SortPyList) : SortPyList
  | Nil : SortPyList

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
    | inj_SortPyList (x : SortPyList) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_PyList» (x0 : SortPyList) : SortKItem
    | «#kxExport2(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_PyList_Int» (x0 : SortPyList) (x1 : SortInt) : SortKItem
end