import Klean95CheckDictCase.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean95CheckDictCase.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («applyMethod(_,_,_)_MPY-METHODS_Val_Val_String_Vals» : SortVal → SortString → SortVals → SortVal)
    («isRefV(_)_MPY-CORE_Bool_Val» : SortVal → SortBool)
    («isStringKey(_)_PROOF-THEORY_Bool_Val» : SortVal → SortBool)
    («lowerKeyCodes(_)_PROOF-THEORY_Bool_IntSeq» : SortIntSeq → SortBool)
    (notBool_ : SortBool → SortBool)
    (stringCodes : SortVal → SortIntSeq)
    («upperKeyCodes(_)_PROOF-THEORY_Bool_IntSeq» : SortIntSeq → SortBool)
    : Prop :=
    (∀ (V : SortVal) (h : (_andBool_ («isStringKey(_)_PROOF-THEORY_Bool_Val» V) (notBool_ («isRefV(_)_MPY-CORE_Bool_Val» V))) = true), («applyMethod(_,_,_)_MPY-METHODS_Val_Val_String_Vals» V "islower" SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» : SortVal) = (SortVal.inj_SortBool («lowerKeyCodes(_)_PROOF-THEORY_Bool_IntSeq» (stringCodes V)) : SortVal))
    ∧ (∀ (V : SortVal) (h : (_andBool_ («isStringKey(_)_PROOF-THEORY_Bool_Val» V) (notBool_ («isRefV(_)_MPY-CORE_Bool_Val» V))) = true), («applyMethod(_,_,_)_MPY-METHODS_Val_Val_String_Vals» V "isupper" SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» : SortVal) = (SortVal.inj_SortBool («upperKeyCodes(_)_PROOF-THEORY_Bool_IntSeq» (stringCodes V)) : SortVal))

end Klean95CheckDictCase.Lemmas
