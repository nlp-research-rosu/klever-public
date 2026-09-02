import Klean51RemoveVowels.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean51RemoveVowels.Lemmas

def targetStatement
    («isVowelCode(_)_VERIFICATION_Bool_Int» : SortInt → SortBool)
    («strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» : SortIntSeq → SortIntSeq → SortBool)
    : Prop :=
    (∀ (C : SortInt), («strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 97 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 101 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 105 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 111 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 117 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 65 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 69 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 73 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 79 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 85 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))))))))) : SortBool) = («isVowelCode(_)_VERIFICATION_Bool_Int» C : SortBool))

end Klean51RemoveVowels.Lemmas
