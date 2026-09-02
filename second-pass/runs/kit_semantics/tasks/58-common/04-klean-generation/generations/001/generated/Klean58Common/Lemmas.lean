import Klean58Common.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean58Common.Lemmas

def targetStatement
    (_orBool_ : SortBool → SortBool → SortBool)
    («_==K_» : SortK → SortK → SortBool)
    (notBool_ : SortBool → SortBool)
    : Prop :=
    (∀ (B : SortBool) (V : SortVal) (E : SortVal) (h : (notBool_ («_==K_» (SortK.kseq ((@inj SortVal SortKItem) E) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk))) = true), (_orBool_ («_==K_» (SortK.kseq ((@inj SortVal SortKItem) E) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) B : SortBool) = (B : SortBool))

end Klean58Common.Lemmas
