import Klean161Solve.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean161Solve.Lemmas

def targetStatement
    («_==K_» : SortK → SortK → SortBool)
    : Prop :=
    (∀ (C : SortInt), («_==K_» (SortK.kseq (SortKItem.inj_SortIntSeq (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)) SortK.dotk) (SortK.kseq (SortKItem.inj_SortIntSeq SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») SortK.dotk) : SortBool) = (false : SortBool))

end Klean161Solve.Lemmas
