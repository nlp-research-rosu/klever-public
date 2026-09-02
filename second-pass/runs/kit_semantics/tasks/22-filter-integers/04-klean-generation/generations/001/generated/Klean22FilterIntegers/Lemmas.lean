import Klean22FilterIntegers.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean22FilterIntegers.Lemmas

def targetStatement
    (_orBool_ : SortBool → SortBool → SortBool)
    (isBool : SortK → SortBool)
    (isInt : SortK → SortBool)
    («isIntV(_)_MPY-BUILTINS_Bool_Val» : SortVal → SortBool)
    : Prop :=
    (∀ (V : SortVal), («isIntV(_)_MPY-BUILTINS_Bool_Val» V : SortBool) = (_orBool_ (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) (isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) : SortBool))

end Klean22FilterIntegers.Lemmas
