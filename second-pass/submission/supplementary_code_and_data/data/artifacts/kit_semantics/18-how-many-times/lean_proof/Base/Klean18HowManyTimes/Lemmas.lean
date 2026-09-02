import Klean18HowManyTimes.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean18HowManyTimes.Lemmas

def targetStatement
    («_==K_» : SortK → SortK → SortBool)
    («buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» : SortIntSeq → SortInt → SortInt → SortInt → SortIntSeq)
    («clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» : SortInt → SortInt → SortInt → SortInt)
    («isLen(_)_MPY-CORE_Int_IntSeq» : SortIntSeq → SortInt)
    (notBool_ : SortBool → SortBool)
    («tailIS(_)_VERIFICATION_IntSeq_IntSeq» : SortIntSeq → SortIntSeq)
    : Prop :=
    (∀ (S : SortIntSeq) (h : (notBool_ («_==K_» (SortK.kseq (SortKItem.inj_SortIntSeq S) SortK.dotk) (SortK.kseq (SortKItem.inj_SortIntSeq SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») SortK.dotk))) = true), («buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» S («clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» 1 («isLen(_)_MPY-CORE_Int_IntSeq» S) 1) («isLen(_)_MPY-CORE_Int_IntSeq» S) 1 : SortIntSeq) = («tailIS(_)_VERIFICATION_IntSeq_IntSeq» S : SortIntSeq))

end Klean18HowManyTimes.Lemmas
