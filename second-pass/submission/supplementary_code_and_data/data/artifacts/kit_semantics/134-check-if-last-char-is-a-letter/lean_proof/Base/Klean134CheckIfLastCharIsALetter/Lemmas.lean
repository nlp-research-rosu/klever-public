import Klean134CheckIfLastCharIsALetter.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean134CheckIfLastCharIsALetter.Lemmas

def targetStatement
    («_==Int_» : SortInt → SortInt → SortBool)
    («_==K_» : SortK → SortK → SortBool)
    : Prop :=
    (∀ (_REST : SortIntSeq) (_C : SortInt), («_==K_» (SortK.kseq (SortKItem.inj_SortIntSeq (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _C _REST)) SortK.dotk) (SortK.kseq (SortKItem.inj_SortIntSeq SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») SortK.dotk) : SortBool) = (false : SortBool))
    ∧ (∀ (D : SortInt) (C : SortInt), («_==K_» (SortK.kseq (SortKItem.inj_SortIntSeq (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)) SortK.dotk) (SortK.kseq (SortKItem.inj_SortIntSeq (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» D SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)) SortK.dotk) : SortBool) = («_==Int_» C D : SortBool))

end Klean134CheckIfLastCharIsALetter.Lemmas
