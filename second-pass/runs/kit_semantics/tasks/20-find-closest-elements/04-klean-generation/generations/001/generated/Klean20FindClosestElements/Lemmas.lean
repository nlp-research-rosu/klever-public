import Klean20FindClosestElements.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean20FindClosestElements.Lemmas

def targetStatement
    («allFloatItems(_)_VERIFICATION-BASE_Bool_ValSeq» : SortValSeq → SortBool)
    («allFloatVS(_)_VERIFICATION-BASE_Bool_ValSeq» : SortValSeq → SortBool)
    («applyIndex(_,_)_MPY-SUBSCRIPT_Val_Val_Int» : SortVal → SortInt → SortVal)
    («enumVS(_,_)_MPY-BUILTINS_ValSeq_ValSeq_Int» : SortValSeq → SortInt → SortValSeq)
    («itemFloat(_)_VERIFICATION-BASE_Float_Val» : SortVal → SortFloat)
    («itemIndex(_)_VERIFICATION-BASE_Int_Val» : SortVal → SortInt)
    : Prop :=
    (∀ (V : SortVal) (h : (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) = (SortK.kseq ((@inj SortIterable SortKItem) (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt («itemIndex(_)_VERIFICATION-BASE_Int_Val» V)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortFloat («itemFloat(_)_VERIFICATION-BASE_Float_Val» V)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)))) SortK.dotk)), («applyIndex(_,_)_MPY-SUBSCRIPT_Val_Val_Int» V 0 : SortVal) = (SortVal.inj_SortInt («itemIndex(_)_VERIFICATION-BASE_Int_Val» V) : SortVal))
    ∧ (∀ (V : SortVal) (h : (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) = (SortK.kseq ((@inj SortIterable SortKItem) (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt («itemIndex(_)_VERIFICATION-BASE_Int_Val» V)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortFloat («itemFloat(_)_VERIFICATION-BASE_Float_Val» V)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)))) SortK.dotk)), («applyIndex(_,_)_MPY-SUBSCRIPT_Val_Val_Int» V 1 : SortVal) = (SortVal.inj_SortFloat («itemFloat(_)_VERIFICATION-BASE_Float_Val» V) : SortVal))
    ∧ (∀ (_Gen0 : SortInt) (VS : SortValSeq) (h : («allFloatVS(_)_VERIFICATION-BASE_Bool_ValSeq» VS) = true), («allFloatItems(_)_VERIFICATION-BASE_Bool_ValSeq» («enumVS(_,_)_MPY-BUILTINS_ValSeq_ValSeq_Int» VS _Gen0) : SortBool) = (true : SortBool))

end Klean20FindClosestElements.Lemmas
