import Klean40TriplesSumToZero.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean40TriplesSumToZero.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_<Int_» : SortInt → SortInt → SortBool)
    («_<=Int_» : SortInt → SortInt → SortBool)
    («intAt(_,_)_VERIFICATION_Int_IntSeq_Int» : SortIntSeq → SortInt → SortInt)
    («intVals(_)_VERIFICATION_ValSeq_IntSeq» : SortIntSeq → SortValSeq)
    («isLen(_)_MPY-CORE_Int_IntSeq» : SortIntSeq → SortInt)
    («valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» : SortValSeq → SortInt → SortVal)
    («vsLen(_)_MPY-CORE_Int_ValSeq» : SortValSeq → SortInt)
    : Prop :=
    (∀ (IS : SortIntSeq), («vsLen(_)_MPY-CORE_Int_ValSeq» («intVals(_)_VERIFICATION_ValSeq_IntSeq» IS) : SortInt) = («isLen(_)_MPY-CORE_Int_IntSeq» IS : SortInt))
    ∧ (∀ (I : SortInt) (IS : SortIntSeq) (h : (_andBool_ («_<=Int_» 0 I) («_<Int_» I («isLen(_)_MPY-CORE_Int_IntSeq» IS))) = true), («valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» («intVals(_)_VERIFICATION_ValSeq_IntSeq» IS) I : SortVal) = (SortVal.inj_SortInt («intAt(_,_)_VERIFICATION_Int_IntSeq_Int» IS I) : SortVal))

end Klean40TriplesSumToZero.Lemmas
