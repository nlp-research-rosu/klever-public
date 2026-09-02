import Klean35MaxElement.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean35MaxElement.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    (_orBool_ : SortBool → SortBool → SortBool)
    («_>Int_» : SortInt → SortInt → SortBool)
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    («codesOf(_)_VERIFICATION_IntSeq_Str» : SortStr → SortIntSeq)
    (isBool : SortK → SortBool)
    (isFloat : SortK → SortBool)
    (isInt : SortK → SortBool)
    («isNumericV(_)_VERIFICATION_Bool_Val» : SortVal → SortBool)
    (isStr : SortK → SortBool)
    (maxFOpaque : SortFloat → SortFloat → SortFloat)
    («maxFloat(_,_)_FLOAT_Float_Float_Float» : SortFloat → SortFloat → SortFloat)
    («numericGt(_,_)_VERIFICATION_Bool_NumericView_NumericView» : SortNumericView → SortNumericView → SortBool)
    («numericView(_)_VERIFICATION_NumericView_Val» : SortVal → SortNumericView)
    («project:Bool» : SortK → SortBool)
    («project:Float» : SortK → SortFloat)
    («project:Int» : SortK → SortInt)
    («project:Str» : SortK → SortStr)
    (projectBoolTotal : SortVal → SortBool)
    (projectFloatTotal : SortVal → SortFloat)
    (projectIntTotal : SortVal → SortInt)
    (projectStrTotal : SortVal → SortStr)
    («strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» : SortIntSeq → SortIntSeq → SortBool)
    («project:Bool?» : SortK → Option SortBool)
    («project:Float?» : SortK → Option SortFloat)
    («project:Int?» : SortK → Option SortInt)
    («project:Str?» : SortK → Option SortStr)
    : Prop :=
    (∀ (V : SortVal), ((«project:Int?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («project:Int» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortInt) = (projectIntTotal V : SortInt))
    ∧ (∀ (M : SortInt) (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" V (SortVal.inj_SortInt M) : SortBool) = («_>Int_» (projectIntTotal V) M : SortBool))
    ∧ (∀ (V : SortVal), ((«project:Float?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : (isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («project:Float» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortFloat) = (projectFloatTotal V : SortFloat))
    ∧ (∀ (F2 : SortFloat) (F1 : SortFloat), («maxFloat(_,_)_FLOAT_Float_Float_Float» F1 F2 : SortFloat) = (maxFOpaque F1 F2 : SortFloat))
    ∧ (∀ (V : SortVal), ((«project:Bool?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : (isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («project:Bool» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortBool) = (projectBoolTotal V : SortBool))
    ∧ (∀ (V : SortVal), ((«project:Str?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true) ↔ (((isStr (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortBool) = (true : SortBool)) ∧ (True)))
    ∧ (∀ (V : SortVal) (h : (isStr (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), («project:Str» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) : SortStr) = (projectStrTotal V : SortStr))
    ∧ (∀ (M : SortVal) (V : SortVal) (h : (_andBool_ («isNumericV(_)_VERIFICATION_Bool_Val» V) («isNumericV(_)_VERIFICATION_Bool_Val» M)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" V M : SortBool) = («numericGt(_,_)_VERIFICATION_Bool_NumericView_NumericView» («numericView(_)_VERIFICATION_NumericView_Val» V) («numericView(_)_VERIFICATION_NumericView_Val» M) : SortBool))
    ∧ (∀ (M : SortVal) (V : SortVal) (h : (_andBool_ (isStr (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) (isStr (SortK.kseq ((@inj SortVal SortKItem) M) SortK.dotk))) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" V M : SortBool) = («strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» («codesOf(_)_VERIFICATION_IntSeq_Str» (projectStrTotal M)) («codesOf(_)_VERIFICATION_IntSeq_Str» (projectStrTotal V)) : SortBool))
    ∧ (∀ (V : SortVal) (h : (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), (_orBool_ (isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) (isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) : SortBool) = (false : SortBool))
    ∧ (∀ (V : SortVal) (h : (isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), (_orBool_ (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) (isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) : SortBool) = (false : SortBool))
    ∧ (∀ (V : SortVal) (h : (isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) = true), (_orBool_ (isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) (isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)) : SortBool) = (false : SortBool))

end Klean35MaxElement.Lemmas
