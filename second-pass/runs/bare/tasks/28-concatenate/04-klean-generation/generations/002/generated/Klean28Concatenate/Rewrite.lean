import Klean28Concatenate.Func

inductive Rewrites : SortGeneratedTopCell → SortGeneratedTopCell → Prop where
  | tran {s1 s2 s3 : SortGeneratedTopCell} (t1 : Rewrites s1 s2) (t2 : Rewrites s2 s3) : Rewrites s1 s3
  | VERIFICATION_KLEAN_EXPORT_kxExport0 {V0 _Val0 : SortString} {V1 : SortStrList} {_DotVar0 : SortGeneratedCounterCell} {_DotVar1 : SortK} (defn_Val0 : «concatAcc(_,_)_VERIFICATION_String_String_StrList» V0 V1 = some _Val0) : Rewrites { k := { val := SortK.kseq (SortKItem.«#kxExport0(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_String_StrList» V0 V1) _DotVar1 }, generatedCounter := _DotVar0 } { k := { val := SortK.kseq ((@inj SortString SortKItem) _Val0) _DotVar1 }, generatedCounter := _DotVar0 }