import Klean72WillItFly.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean72WillItFly.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («floatV(_)_VERIFICATION-SYNTAX_Bool_Val» : SortVal → SortBool)
    (intLikeTotal : SortVal → SortInt)
    («intOf(_)_MPY-BUILTINS_Int_Val» : SortVal → SortInt)
    («integralV(_)_VERIFICATION-SYNTAX_Bool_Val» : SortVal → SortBool)
    (isBool : SortK → SortBool)
    (isFloat : SortK → SortBool)
    (isInt : SortK → SortBool)
    (notBool_ : SortBool → SortBool)
    («project:Bool» : SortK → SortBool)
    («project:Float» : SortK → SortFloat)
    («project:Int» : SortK → SortInt)
    (projectBoolTotal : SortVal → SortBool)
    (projectFloatTotal : SortVal → SortFloat)
    (projectIntTotal : SortVal → SortInt)
    : Prop :=
    (∀ (V : SortVal) (h : (_andBool_ (_andBool_ (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) (notBool_ (isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)))) (notBool_ (isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)))) = true), («project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortInt) = (projectIntTotal V : SortInt))
    ∧ (∀ (V : SortVal), (True) ↔ (((isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : (_andBool_ (_andBool_ (isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) (notBool_ (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)))) (notBool_ (isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)))) = true), («project:Bool» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortBool) = (projectBoolTotal V : SortBool))
    ∧ (∀ (V : SortVal), (True) ↔ (((isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : («floatV(_)_VERIFICATION-SYNTAX_Bool_Val» V) = true), («project:Float» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortFloat) = (projectFloatTotal V : SortFloat))
    ∧ (∀ (V : SortVal), (True) ↔ (((isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : («integralV(_)_VERIFICATION-SYNTAX_Bool_Val» V) = true), («intOf(_)_MPY-BUILTINS_Int_Val» V : SortInt) = (intLikeTotal V : SortInt))

end Klean72WillItFly.Lemmas
