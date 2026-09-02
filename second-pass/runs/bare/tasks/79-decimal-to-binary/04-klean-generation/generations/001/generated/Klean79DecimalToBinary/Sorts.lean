import Klean79DecimalToBinary.Prelude

structure SortArgCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  structure SortGeneratedTopCell : Type where
    python : SortPythonCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortArgCell (x : SortArgCell) : SortKItem
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortPythonCell (x : SortPythonCell) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem

  structure SortPythonCell : Type where
    k : SortKCell
    arg : SortArgCell
    result : SortResultCell

  structure SortResultCell : Type where
    val : SortK
end