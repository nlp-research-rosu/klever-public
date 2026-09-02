import Klean9RollingMax.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean9RollingMax.Lemmas

def targetStatement
    («firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» : SortIntSeq → SortBool → SortBool)
    : Prop :=
    (∀ (_IS : SortIntSeq) (_Gen0 : SortBool), «firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» _IS false = _Gen0)

end Klean9RollingMax.Lemmas
