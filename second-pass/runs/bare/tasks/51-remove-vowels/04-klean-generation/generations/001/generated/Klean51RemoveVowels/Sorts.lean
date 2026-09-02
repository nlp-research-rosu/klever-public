import Klean51RemoveVowels.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortResult : Type where
  | noResult_MPY_Result : SortResult
  | «result(_)_MPY_Result_String» (x0 : SortString) : SortResult

structure SortInputCell : Type where
  val : SortString

structure SortResultCell : Type where
  val : SortResult

mutual
  structure SortGeneratedTopCell : Type where
    mpy : SortMpyCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_String» (x0 : SortString) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_String» (x0 : SortString) : SortKItem
    | «#kxExport2(_)_VERIFICATION-KLEAN-EXPORT_KItem_String» (x0 : SortString) : SortKItem
    | done_MPY_KItem : SortKItem

  structure SortMpyCell : Type where
    k : SortKCell
    input : SortInputCell
    result : SortResultCell
end