import Klean151DoubleTheDifference.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean151DoubleTheDifference.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>Int_» : SortInt → SortInt → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_*Int_» : SortInt → SortInt → SortInt)
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» : SortVal → SortBool)
    («dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» : SortValSeq → SortInt)
    (isFloat : SortK → SortBool)
    (isInt : SortK → SortBool)
    («isIntV(_)_MPY-BUILTINS_Bool_Val» : SortVal → SortBool)
    («oddIntSquare(_)_VERIFICATION-SYNTAX_Int_Int» : SortInt → SortInt)
    («project:Int» : SortK → SortInt)
    (projectIntTotal : SortVal → SortInt)
    («pyMod(_,_)_MPY-INT_Int_Int_Int» : SortInt → SortInt → SortInt)
    : Prop :=
    (∀ (VS : SortValSeq) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS) : SortInt) = («_+Int_» («oddIntSquare(_)_VERIFICATION-SYNTAX_Int_Int» (projectIntTotal V)) («dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» VS) : SortInt))
    ∧ (∀ (VS : SortValSeq) (V : SortVal) (h : (isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VS) : SortInt) = («dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» VS : SortInt))
    ∧ (∀ (V : SortVal), (True) ↔ (((«definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal), (projectIntTotal (SortVal.inj_SortInt (projectIntTotal V)) : SortInt) = (projectIntTotal V : SortInt))
    ∧ (∀ (V : SortVal), («isIntV(_)_MPY-BUILTINS_Bool_Val» V : SortBool) = (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortBool))
    ∧ (∀ (I : SortInt) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" V (SortVal.inj_SortInt I) : SortBool) = («_>Int_» (projectIntTotal V) I : SortBool))
    ∧ (∀ (I : SortInt) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "%" V (SortVal.inj_SortInt I) : SortVal) = (SortVal.inj_SortInt («pyMod(_,_)_MPY-INT_Int_Int_Int» (projectIntTotal V) I) : SortVal))
    ∧ (∀ (V2 : SortVal) (V1 : SortVal) (h : (_andBool_ (isInt (SortK.kseq ((@inj SortVal SortKItem) V1) SortK.dotk)) (isInt (SortK.kseq ((@inj SortVal SortKItem) V2) SortK.dotk))) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "*" V1 V2 : SortVal) = (SortVal.inj_SortInt («_*Int_» (projectIntTotal V1) (projectIntTotal V2)) : SortVal))

end Klean151DoubleTheDifference.Lemmas
