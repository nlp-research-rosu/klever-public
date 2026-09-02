import Klean50DecodeShift.Prelude

inductive SortChars : Type where
  | «cons(_,_)_VERIFICATION_Chars_Int_Chars» (x0 : SortInt) (x1 : SortChars) : SortChars
  | nil_VERIFICATION_Chars : SortChars

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
    | inj_SortChars (x : SortChars) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_Chars» (x0 : SortChars) : SortKItem
    | «#kxExport2(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport3(_)_VERIFICATION-KLEAN-EXPORT_KItem_Chars» (x0 : SortChars) : SortKItem
    | «#kxExport4(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport5(_)_VERIFICATION-KLEAN-EXPORT_KItem_Chars» (x0 : SortChars) : SortKItem
end