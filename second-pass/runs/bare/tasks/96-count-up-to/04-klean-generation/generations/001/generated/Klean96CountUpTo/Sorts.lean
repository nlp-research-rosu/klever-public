import Klean96CountUpTo.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

structure SortNCell : Type where
  val : SortInt

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
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortNCell (x : SortNCell) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | «prependIf(_,_)_MPY_KItem_Int_Bool» (x0 : SortInt) (x1 : SortBool) : SortKItem
    | returnValue_MPY_KItem : SortKItem
    | «scan(_,_)_MPY_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem
    | «trial(_,_,_,_)_MPY_KItem_Int_Int_Bool_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortBool) (x3 : SortInt) : SortKItem

  structure SortMpyCell : Type where
    k : SortKCell
    n : SortNCell
    result : SortResultCell

  structure SortResultCell : Type where
    val : SortK
end