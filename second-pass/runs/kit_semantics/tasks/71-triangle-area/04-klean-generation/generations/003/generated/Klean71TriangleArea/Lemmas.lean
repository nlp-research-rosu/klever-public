import Klean71TriangleArea.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean71TriangleArea.Lemmas

def targetStatement
    (intToF : SortInt → SortFloat)
    (proofIntToF : SortInt → SortFloat)
    : Prop :=
    (∀ (I : SortInt), (intToF I : SortFloat) = (proofIntToF I : SortFloat))

end Klean71TriangleArea.Lemmas
