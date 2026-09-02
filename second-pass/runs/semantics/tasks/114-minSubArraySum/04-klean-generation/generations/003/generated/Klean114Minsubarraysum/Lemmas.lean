import Klean114Minsubarraysum.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean114Minsubarraysum.Lemmas

def targetStatement
    («valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» : SortValSeq → SortInt → SortVal)
    : Prop :=
    (∀ (_R : SortIntSeq) (I : SortInt), («valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» (SortValSeq.«intVals(_)_VERIFICATION-BASE_ValSeq_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _R)) 0 : SortVal) = (SortVal.inj_SortInt I : SortVal))

end Klean114Minsubarraysum.Lemmas
