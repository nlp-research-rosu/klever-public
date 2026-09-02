import Klean63Fibfib.Func

inductive Rewrites : SortGeneratedTopCell → SortGeneratedTopCell → Prop where
  | tran {s1 s2 s3 : SortGeneratedTopCell} (t1 : Rewrites s1 s2) (t2 : Rewrites s2 s3) : Rewrites s1 s3
  | FIBFIB_KLEAN_EXPORT_kxExport0 {V0 _Val0 : SortInt} {_DotVar0 : SortGeneratedCounterCell} {_DotVar1 : SortK} (defn_Val0 : «fibfibMath(_)_FIBFIB-VERIFICATION_Int_Int» V0 = some _Val0) : Rewrites { k := { val := SortK.kseq (SortKItem.«#kxExport0(_)_FIBFIB-KLEAN-EXPORT_KItem_Int» V0) _DotVar1 }, generatedCounter := _DotVar0 } { k := { val := SortK.kseq ((@inj SortInt SortKItem) _Val0) _DotVar1 }, generatedCounter := _DotVar0 }