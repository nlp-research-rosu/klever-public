import Klean155EvenOddCount.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean155EvenOddCount.Lemmas

def targetStatement
    («_-Int_» : SortInt → SortInt → SortInt)
    («_>Int_» : SortInt → SortInt → SortBool)
    («_==Int_» : SortInt → SortInt → SortBool)
    («_%Int_» : SortInt → SortInt → SortInt)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_/Int_» : SortInt → SortInt → SortInt)
    («absInt(_)_INT-COMMON_Int_Int» : SortInt → SortInt)
    («decEven(_)_VERIFICATION_Int_Int» : SortInt → SortInt)
    («decOdd(_)_VERIFICATION_Int_Int» : SortInt → SortInt)
    («evenPos(_)_VERIFICATION_Int_Int» : SortInt → SortInt)
    («oddPos(_)_VERIFICATION_Int_Int» : SortInt → SortInt)
    : Prop :=
    (∀ (N : SortInt) (h : («_==Int_» («absInt(_)_INT-COMMON_Int_Int» N) 0) = true), (1 : SortInt) = («decEven(_)_VERIFICATION_Int_Int» N : SortInt))
    ∧ (∀ (N : SortInt) (h : («_==Int_» («absInt(_)_INT-COMMON_Int_Int» N) 0) = true), (0 : SortInt) = («decOdd(_)_VERIFICATION_Int_Int» N : SortInt))
    ∧ (∀ (N : SortInt) (h : («_>Int_» («absInt(_)_INT-COMMON_Int_Int» N) 0) = true), («evenPos(_)_VERIFICATION_Int_Int» («absInt(_)_INT-COMMON_Int_Int» N) : SortInt) = («decEven(_)_VERIFICATION_Int_Int» N : SortInt))
    ∧ (∀ (N : SortInt) (h : («_>Int_» («absInt(_)_INT-COMMON_Int_Int» N) 0) = true), («decEven(_)_VERIFICATION_Int_Int» N : SortInt) = («evenPos(_)_VERIFICATION_Int_Int» («absInt(_)_INT-COMMON_Int_Int» N) : SortInt))
    ∧ (∀ (N : SortInt) (h : («_>Int_» («absInt(_)_INT-COMMON_Int_Int» N) 0) = true), («oddPos(_)_VERIFICATION_Int_Int» («absInt(_)_INT-COMMON_Int_Int» N) : SortInt) = («decOdd(_)_VERIFICATION_Int_Int» N : SortInt))
    ∧ (∀ (N : SortInt) (h : («_>Int_» («absInt(_)_INT-COMMON_Int_Int» N) 0) = true), («decOdd(_)_VERIFICATION_Int_Int» N : SortInt) = («oddPos(_)_VERIFICATION_Int_Int» («absInt(_)_INT-COMMON_Int_Int» N) : SortInt))
    ∧ (∀ (N : SortInt) (E : SortInt) (h : («_>Int_» N 0) = true), («_+Int_» E («evenPos(_)_VERIFICATION_Int_Int» N) : SortInt) = («_+Int_» («_-Int_» («_+Int_» E 1) («_%Int_» («_+Int_» («_%Int_» N 2) 2) 2)) («evenPos(_)_VERIFICATION_Int_Int» («_/Int_» («_-Int_» N («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10)) 10)) : SortInt))
    ∧ (∀ (N : SortInt) (E : SortInt) (h : («_>Int_» N 0) = true), («_+Int_» («_-Int_» («_+Int_» E 1) («_%Int_» («_+Int_» («_%Int_» N 2) 2) 2)) («evenPos(_)_VERIFICATION_Int_Int» («_/Int_» («_-Int_» N («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10)) 10)) : SortInt) = («_+Int_» E («evenPos(_)_VERIFICATION_Int_Int» N) : SortInt))
    ∧ (∀ (N : SortInt) (O : SortInt) (h : («_>Int_» N 0) = true), («_+Int_» O («oddPos(_)_VERIFICATION_Int_Int» N) : SortInt) = («_+Int_» («_+Int_» O («_%Int_» («_+Int_» («_%Int_» N 2) 2) 2)) («oddPos(_)_VERIFICATION_Int_Int» («_/Int_» («_-Int_» N («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10)) 10)) : SortInt))
    ∧ (∀ (N : SortInt) (O : SortInt) (h : («_>Int_» N 0) = true), («_+Int_» («_+Int_» O («_%Int_» («_+Int_» («_%Int_» N 2) 2) 2)) («oddPos(_)_VERIFICATION_Int_Int» («_/Int_» («_-Int_» N («_%Int_» («_+Int_» («_%Int_» N 10) 10) 10)) 10)) : SortInt) = («_+Int_» O («oddPos(_)_VERIFICATION_Int_Int» N) : SortInt))

end Klean155EvenOddCount.Lemmas
