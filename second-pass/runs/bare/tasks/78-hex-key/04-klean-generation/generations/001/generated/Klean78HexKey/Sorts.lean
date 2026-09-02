import Klean78HexKey.Prelude

inductive SortResult : Type where
  | noResult_MPY_Result : SortResult

structure SortResultCell : Type where
  val : SortResult

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  structure SortEnvCell : Type where
    val : SortMap

  structure SortGeneratedTopCell : Type where
    hexKey : SortHexKeyCell
    generatedCounter : SortGeneratedCounterCell

  structure SortHexKeyCell : Type where
    k : SortKCell
    env : SortEnvCell
    result : SortResultCell

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
    | inj_SortHexKeyCell (x : SortHexKeyCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortResult (x : SortResult) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#invoke(_,_)_MPY_KItem_String_String» (x0 : SortString) (x1 : SortString) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_String» (x0 : SortString) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)
end