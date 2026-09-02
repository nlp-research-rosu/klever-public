import Klean86AntiShuffle.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean86AntiShuffle.Lemmas

def targetStatement
    («_<Int_» : SortInt → SortInt → SortBool)
    («strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» : SortIntSeq → SortIntSeq → SortBool)
    : Prop :=
    (∀ (D : SortInt) (C : SortInt), («strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» D SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») : SortBool) = («_<Int_» C D : SortBool))

end Klean86AntiShuffle.Lemmas
