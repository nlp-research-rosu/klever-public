import Klean65CircularShift.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean65CircularShift.Lemmas

def targetStatement
    («Int2String(_)_STRING-COMMON_String_Int» : SortInt → SortString)
    («strToCodes(_)_MPY-STR_IntSeq_String?» : SortString → Option SortIntSeq)
    : Prop :=
    (∀ (X : SortInt), ((«strToCodes(_)_MPY-STR_IntSeq_String?» («Int2String(_)_STRING-COMMON_String_Int» X)).isSome = true) ↔ (True))

end Klean65CircularShift.Lemmas
