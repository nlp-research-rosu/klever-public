import Klean106F.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean106F.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_<=Int_» : SortInt → SortInt → SortBool)
    («_==Int_» : SortInt → SortInt → SortBool)
    («_=/=Int_» : SortInt → SortInt → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_*Int_» : SortInt → SortInt → SortInt)
    («factRun(_,_,_)_VERIFICATION_Int_Int_Int_Int» : SortInt → SortInt → SortInt → SortInt)
    («pyMod(_,_)_MPY-INT_Int_Int_Int» : SortInt → SortInt → SortInt)
    («resultRun(_,_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Int_Int_Int» : SortValSeq → SortInt → SortInt → SortInt → SortInt → SortValSeq)
    («totalRun(_,_,_)_VERIFICATION_Int_Int_Int_Int» : SortInt → SortInt → SortInt → SortInt)
    («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» : SortValSeq → SortValSeq → SortValSeq)
    : Prop :=
    (∀ (I : SortInt) (F : SortInt) (N : SortInt) (h : («_<=Int_» I N) = true), («factRun(_,_,_)_VERIFICATION_Int_Int_Int_Int» («_+Int_» I 1) N («_*Int_» F I) : SortInt) = («factRun(_,_,_)_VERIFICATION_Int_Int_Int_Int» I N F : SortInt))
    ∧ (∀ (I : SortInt) (T : SortInt) (N : SortInt) (h : («_<=Int_» I N) = true), («totalRun(_,_,_)_VERIFICATION_Int_Int_Int_Int» («_+Int_» I 1) N («_+Int_» T I) : SortInt) = («totalRun(_,_,_)_VERIFICATION_Int_Int_Int_Int» I N T : SortInt))
    ∧ (∀ (I : SortInt) (T : SortInt) (F : SortInt) (N : SortInt) (VS : SortValSeq) (h : (_andBool_ («_<=Int_» I N) («_==Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» I 2) 0)) = true), («resultRun(_,_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Int_Int_Int» («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» VS (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt («_*Int_» F I)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)) («_+Int_» I 1) N («_*Int_» F I) («_+Int_» T I) : SortValSeq) = («resultRun(_,_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Int_Int_Int» VS I N F T : SortValSeq))
    ∧ (∀ (I : SortInt) (T : SortInt) (F : SortInt) (N : SortInt) (VS : SortValSeq) (h : (_andBool_ («_<=Int_» I N) («_=/=Int_» («pyMod(_,_)_MPY-INT_Int_Int_Int» I 2) 0)) = true), («resultRun(_,_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Int_Int_Int» («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» VS (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt («_+Int_» T I)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)) («_+Int_» I 1) N («_*Int_» F I) («_+Int_» T I) : SortValSeq) = («resultRun(_,_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Int_Int_Int» VS I N F T : SortValSeq))

end Klean106F.Lemmas
