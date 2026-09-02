import Klean152Compare.Func

inductive Rewrites : SortGeneratedTopCell → SortGeneratedTopCell → Prop where
  | tran {s1 s2 s3 : SortGeneratedTopCell} (t1 : Rewrites s1 s2) (t2 : Rewrites s2 s3) : Rewrites s1 s3
  | VERIFICATION_KLEAN_EXPORT_kxExport0 {V0 V1 _Val0 : SortValues} {_DotVar0 : SortGeneratedCounterCell} {_DotVar1 : SortK} (defn_Val0 : expected V0 V1 = some _Val0) : Rewrites { k := { val := SortK.kseq (SortKItem.«#kxExport0(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Values_Values» V0 V1) _DotVar1 }, generatedCounter := _DotVar0 } { k := { val := SortK.kseq ((@inj SortValues SortKItem) _Val0) _DotVar1 }, generatedCounter := _DotVar0 }