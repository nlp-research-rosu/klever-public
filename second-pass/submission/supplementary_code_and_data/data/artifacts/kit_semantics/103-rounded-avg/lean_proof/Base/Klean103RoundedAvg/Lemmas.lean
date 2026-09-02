import Klean103RoundedAvg.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean103RoundedAvg.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>Int_» : SortInt → SortInt → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_*Int_» : SortInt → SortInt → SortInt)
    («allBits(_)_VERIFICATION-BASE_Bool_IntSeq» : SortIntSeq → SortBool)
    («bitValue(_)_VERIFICATION-BASE_Int_IntSeq» : SortIntSeq → SortInt)
    («bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» : SortIntSeq → SortInt)
    (loopDigits : SortInt → SortIntSeq → SortIntSeq)
    : Prop :=
    (∀ (A : SortIntSeq) (V : SortInt) (h : (_andBool_ («_>Int_» V 0) («allBits(_)_VERIFICATION-BASE_Bool_IntSeq» A)) = true), («_+Int_» («bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» (loopDigits V A)) («bitValue(_)_VERIFICATION-BASE_Int_IntSeq» (loopDigits V A)) : SortInt) = («_+Int_» («_*Int_» V («bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» A)) («bitValue(_)_VERIFICATION-BASE_Int_IntSeq» A) : SortInt))
    ∧ (∀ (A : SortIntSeq) (V : SortInt) (h : (_andBool_ («_>Int_» V 0) («allBits(_)_VERIFICATION-BASE_Bool_IntSeq» A)) = true), («_+Int_» («_*Int_» 1 («bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» (loopDigits V A))) («bitValue(_)_VERIFICATION-BASE_Int_IntSeq» (loopDigits V A)) : SortInt) = («_+Int_» («_*Int_» V («bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» A)) («bitValue(_)_VERIFICATION-BASE_Int_IntSeq» A) : SortInt))
    ∧ (∀ (A : SortIntSeq) (V : SortInt) (h : (_andBool_ («_>Int_» V 0) («allBits(_)_VERIFICATION-BASE_Bool_IntSeq» A)) = true), («allBits(_)_VERIFICATION-BASE_Bool_IntSeq» (loopDigits V A) : SortBool) = (true : SortBool))

end Klean103RoundedAvg.Lemmas
