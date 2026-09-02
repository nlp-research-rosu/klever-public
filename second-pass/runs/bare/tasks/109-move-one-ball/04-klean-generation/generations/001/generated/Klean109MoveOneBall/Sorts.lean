import Klean109MoveOneBall.Prelude

inductive SortIList : Type where
  | «.IList_HUMAN-EVAL-SYNTAX_IList» : SortIList
  | «_::__HUMAN-EVAL-SYNTAX_IList_Int_IList» (x0 : SortInt) (x1 : SortIList) : SortIList

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
    | inj_SortIList (x : SortIList) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | «#kxExport0(_)_HUMAN-EVAL-KLEAN-EXPORT_KItem_IList» (x0 : SortIList) : SortKItem
    | «#kxExport1(_)_HUMAN-EVAL-KLEAN-EXPORT_KItem_IList» (x0 : SortIList) : SortKItem
    | «#kxExport2(_,_)_HUMAN-EVAL-KLEAN-EXPORT_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem
    | «#kxExport3(_,_)_HUMAN-EVAL-KLEAN-EXPORT_KItem_Int_IList» (x0 : SortInt) (x1 : SortIList) : SortKItem
    | «#kxExport4(_)_HUMAN-EVAL-KLEAN-EXPORT_KItem_IList» (x0 : SortIList) : SortKItem
    | «#kxExport5(_)_HUMAN-EVAL-KLEAN-EXPORT_KItem_IList» (x0 : SortIList) : SortKItem
end