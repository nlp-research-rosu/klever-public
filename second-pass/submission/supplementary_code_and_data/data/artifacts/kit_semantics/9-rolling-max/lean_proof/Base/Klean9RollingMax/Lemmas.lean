import Klean9RollingMax.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean9RollingMax.Lemmas

def targetStatement
    (isInt : SortK → SortBool)
    : Prop :=
    (∀ (V : SortVal), ((true : SortBool) = (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortBool)) ↔ (∃ (I : SortInt), (V : SortVal) = (SortVal.inj_SortInt I : SortVal)))

end Klean9RollingMax.Lemmas
