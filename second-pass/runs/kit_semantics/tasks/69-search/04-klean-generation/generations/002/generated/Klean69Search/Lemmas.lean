import Klean69Search.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean69Search.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>Int_» : SortInt → SortInt → SortBool)
    («_>=Int_» : SortInt → SortInt → SortBool)
    («_==Int_» : SortInt → SortInt → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal)
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («definedProjectInt(_)_VERIFICATION_Bool_Val» : SortVal → SortBool)
    («isIntVal(_)_VERIFICATION_Bool_Val» : SortVal → SortBool)
    («project:Int» : SortK → SortInt)
    (projectIntTotal : SortVal → SortInt)
    : Prop :=
    (∀ (V : SortVal), (True) ↔ (((«definedProjectInt(_)_VERIFICATION_Bool_Val» V : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (W : SortVal) (V : SortVal) (h : (_andBool_ («isIntVal(_)_VERIFICATION_Bool_Val» V) («isIntVal(_)_VERIFICATION_Bool_Val» W)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "==" V W : SortBool) = («_==Int_» (projectIntTotal V) (projectIntTotal W) : SortBool))
    ∧ (∀ (W : SortVal) (V : SortVal) (h : (_andBool_ («isIntVal(_)_VERIFICATION_Bool_Val» V) («isIntVal(_)_VERIFICATION_Bool_Val» W)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">=" V W : SortBool) = («_>=Int_» (projectIntTotal V) (projectIntTotal W) : SortBool))
    ∧ (∀ (W : SortVal) (V : SortVal) (h : (_andBool_ («isIntVal(_)_VERIFICATION_Bool_Val» V) («isIntVal(_)_VERIFICATION_Bool_Val» W)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" V W : SortBool) = («_>Int_» (projectIntTotal V) (projectIntTotal W) : SortBool))
    ∧ (∀ (W : SortVal) (V : SortVal) (h : (_andBool_ («isIntVal(_)_VERIFICATION_Bool_Val» V) («isIntVal(_)_VERIFICATION_Bool_Val» W)) = true), («applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" V W : SortVal) = (SortVal.inj_SortInt («_+Int_» (projectIntTotal V) (projectIntTotal W)) : SortVal))

end Klean69Search.Lemmas
