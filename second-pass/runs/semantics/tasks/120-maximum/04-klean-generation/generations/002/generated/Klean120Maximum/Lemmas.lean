import Klean120Maximum.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean120Maximum.Lemmas

def targetStatement
    (sortVS : SortValSeq → SortValSeq)
    («vsLen(_)_MPY-CORE_Int_ValSeq» : SortValSeq → SortInt)
    : Prop :=
    (∀ (VS : SortValSeq), («vsLen(_)_MPY-CORE_Int_ValSeq» (sortVS VS) : SortInt) = («vsLen(_)_MPY-CORE_Int_ValSeq» VS : SortInt))

end Klean120Maximum.Lemmas
