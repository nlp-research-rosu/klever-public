import Klean131Digits.Lemmas

namespace Proof

/- K's `%Int` and `/Int` hooks are truncating remainder and quotient.  The
   frozen pyMod equation applies truncating remainder twice to obtain Python's
   nonnegative remainder for the positive moduli used by the program. -/
def pyModCore (a b : Int) : Int := (a.tmod b + b).tmod b

theorem tmod_of_nonneg (a b : Int) (ha : 0 ≤ a) :
    a.tmod b = a % b := by
  simp [Int.tmod_eq_emod, ha]

theorem quotient_ofNat (n : Nat) :
    (((Int.ofNat n - pyModCore (Int.ofNat n) 10).tdiv 10).toNat) =
      n / 10 := by
  rw [show pyModCore (Int.ofNat n) 10 = Int.ofNat (n % 10) by
    unfold pyModCore
    rw [show (Int.ofNat n).tmod 10 = (Int.ofNat n) % 10 by
      exact tmod_of_nonneg _ _ (Int.ofNat_zero_le n)]
    rw [tmod_of_nonneg _ _ (by
      have := Int.emod_nonneg (Int.ofNat n) (by omega : (10 : Int) ≠ 0)
      omega)]
    rw [Int.add_emod]
    simp]
  have hdecomp := Int.ediv_add_emod (Int.ofNat n) 10
  have hmod : (Int.ofNat n) % 10 = Int.ofNat (n % 10) := by simp
  have hdiv : (Int.ofNat n) / 10 = Int.ofNat (n / 10) := by simp
  have hnum :
      Int.ofNat n - Int.ofNat (n % 10) =
        10 * Int.ofNat (n / 10) := by
    omega
  rw [hnum, Int.tdiv_eq_ediv]
  simp
  exact Int.toNat_natCast (n / 10)

/- This is the total operational reading of oddDigitProduct.  Positive inputs
   take exactly the frozen K recurrence; zero (and negative inputs, which are
   outside that recurrence's guard) return the accumulator.  Recursion
   terminates because the positive decimal quotient is strictly smaller. -/
def oddDigitProductCore (n : Nat) (A : Int) : Int :=
  if _hn : n = 0 then
    A
  else
    let N : Int := Int.ofNat n
    let D := pyModCore N 10
    let Q : Nat := ((N - D).tdiv 10).toNat
    if pyModCore N 2 = 1 then
      if A = 0 then
        oddDigitProductCore Q D
      else
        oddDigitProductCore Q (A * D)
    else
      oddDigitProductCore Q A
termination_by n
decreasing_by
  all_goals
    rw [quotient_ofNat]
    exact Nat.div_lt_self (Nat.pos_of_ne_zero _hn) (by decide)

theorem oddDigitProductCore_even
    (n : Nat) (A : Int) (hn : n ≠ 0)
    (heven : pyModCore (Int.ofNat n) 2 ≠ 1) :
    oddDigitProductCore n A =
      oddDigitProductCore
        (((Int.ofNat n - pyModCore (Int.ofNat n) 10).tdiv 10).toNat) A := by
  rw [oddDigitProductCore.eq_def n A]
  simp only [dif_neg hn, if_neg heven]

theorem oddDigitProductCore_first
    (n : Nat) (hn : n ≠ 0)
    (hodd : pyModCore (Int.ofNat n) 2 = 1) :
    oddDigitProductCore n 0 =
      oddDigitProductCore
        (((Int.ofNat n - pyModCore (Int.ofNat n) 10).tdiv 10).toNat)
        (pyModCore (Int.ofNat n) 10) := by
  rw [oddDigitProductCore.eq_def n 0]
  simp only [dif_neg hn, if_pos hodd, if_pos]

theorem oddDigitProductCore_later
    (n : Nat) (A : Int) (hn : n ≠ 0)
    (hodd : pyModCore (Int.ofNat n) 2 = 1) (hA : A ≠ 0) :
    oddDigitProductCore n A =
      oddDigitProductCore
        (((Int.ofNat n - pyModCore (Int.ofNat n) 10).tdiv 10).toNat)
        (A * pyModCore (Int.ofNat n) 10) := by
  rw [oddDigitProductCore.eq_def n A]
  simp only [dif_neg hn, if_pos hodd, if_neg hA]

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-4d51675c3f64dd8d5acd7f855e28f517fc1edc539220ae3724773ad4a26eded2, rule-3978fc0ec976783d9a30feccc0ac292802be0d3aecc09914bc975f6c302270b2, rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» : SortInt → SortInt → SortInt := Int.sub
/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-4d51675c3f64dd8d5acd7f855e28f517fc1edc539220ae3724773ad4a26eded2, rule-3978fc0ec976783d9a30feccc0ac292802be0d3aecc09914bc975f6c302270b2, rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ : SortBool → SortBool → SortBool := Bool.and
/- KORE symbol: Lbl'Unds-GT-'Int'Unds'; frozen source obligations: rule-4d51675c3f64dd8d5acd7f855e28f517fc1edc539220ae3724773ad4a26eded2, rule-3978fc0ec976783d9a30feccc0ac292802be0d3aecc09914bc975f6c302270b2, rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>Int_» (a b : SortInt) : SortBool := decide (a > b)
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-3978fc0ec976783d9a30feccc0ac292802be0d3aecc09914bc975f6c302270b2, rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (a b : SortInt) : SortBool := decide (a = b)
/- KORE symbol: Lbl'UndsEqlsSlshEqls'Int'Unds'; frozen source obligations: rule-4d51675c3f64dd8d5acd7f855e28f517fc1edc539220ae3724773ad4a26eded2, rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_=/=Int_» (a b : SortInt) : SortBool := decide (a ≠ b)
/- KORE symbol: Lbl'UndsPerc'Int'Unds'; frozen source obligations: rule-4d51675c3f64dd8d5acd7f855e28f517fc1edc539220ae3724773ad4a26eded2, rule-3978fc0ec976783d9a30feccc0ac292802be0d3aecc09914bc975f6c302270b2, rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_%Int_» : SortInt → SortInt → SortInt := Int.tmod
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-4d51675c3f64dd8d5acd7f855e28f517fc1edc539220ae3724773ad4a26eded2, rule-3978fc0ec976783d9a30feccc0ac292802be0d3aecc09914bc975f6c302270b2, rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» : SortInt → SortInt → SortInt := Int.add
/- KORE symbol: Lbl'UndsSlsh'Int'Unds'; frozen source obligations: rule-4d51675c3f64dd8d5acd7f855e28f517fc1edc539220ae3724773ad4a26eded2, rule-3978fc0ec976783d9a30feccc0ac292802be0d3aecc09914bc975f6c302270b2, rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_/Int_» : SortInt → SortInt → SortInt := Int.tdiv
/- KORE symbol: Lbl'UndsStar'Int'Unds'; frozen source obligations: rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_*Int_» : SortInt → SortInt → SortInt := Int.mul
/- KORE symbol: LbloddDigitProduct'LParUndsCommUndsRParUnds'DIGITS-VERIFICATION'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-4d51675c3f64dd8d5acd7f855e28f517fc1edc539220ae3724773ad4a26eded2, rule-3978fc0ec976783d9a30feccc0ac292802be0d3aecc09914bc975f6c302270b2, rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «oddDigitProduct(_,_)_DIGITS-VERIFICATION_Int_Int_Int»
    (N A : SortInt) : SortInt :=
  oddDigitProductCore N.toNat A
/- KORE symbol: LblpyMod'LParUndsCommUndsRParUnds'MPY-INT'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-4d51675c3f64dd8d5acd7f855e28f517fc1edc539220ae3724773ad4a26eded2, rule-3978fc0ec976783d9a30feccc0ac292802be0d3aecc09914bc975f6c302270b2, rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «pyMod(_,_)_MPY-INT_Int_Int_Int» : SortInt → SortInt → SortInt :=
  pyModCore

theorem final :
    Klean131Digits.Lemmas.targetStatement «_-Int_» _andBool_ «_>Int_» «_==Int_» «_=/=Int_» «_%Int_» «_+Int_» «_/Int_» «_*Int_» «oddDigitProduct(_,_)_DIGITS-VERIFICATION_Int_Int_Int» «pyMod(_,_)_MPY-INT_Int_Int_Int» := by
  unfold Klean131Digits.Lemmas.targetStatement
  constructor
  · intro A N h
    have hcond : N > 0 ∧ pyModCore N 2 ≠ 1 := by
      simpa [_andBool_, «_>Int_», «_=/=Int_»,
        «pyMod(_,_)_MPY-INT_Int_Int_Int»] using h
    obtain ⟨hN, hparity⟩ := hcond
    have hcast : Int.ofNat N.toNat = N :=
      Int.toNat_of_nonneg (Int.le_of_lt hN)
    have hn : N.toNat ≠ 0 := by
      intro hz
      rw [hz] at hcast
      simp at hcast
      exact (Int.ne_of_gt hN) hcast.symm
    rw [← hcast] at hparity ⊢
    change
      oddDigitProductCore
          (((Int.ofNat N.toNat -
              pyModCore (Int.ofNat N.toNat) 10).tdiv 10).toNat)
          A =
        oddDigitProductCore N.toNat A
    exact
      (oddDigitProductCore_even N.toNat A hn hparity).symm
  constructor
  · intro N h
    have hcond : N > 0 ∧ pyModCore N 2 = 1 := by
      simpa [_andBool_, «_>Int_», «_==Int_»,
        «pyMod(_,_)_MPY-INT_Int_Int_Int»] using h
    obtain ⟨hN, hparity⟩ := hcond
    have hcast : Int.ofNat N.toNat = N :=
      Int.toNat_of_nonneg (Int.le_of_lt hN)
    have hn : N.toNat ≠ 0 := by
      intro hz
      rw [hz] at hcast
      simp at hcast
      exact (Int.ne_of_gt hN) hcast.symm
    rw [← hcast] at hparity ⊢
    change
      oddDigitProductCore
          (((Int.ofNat N.toNat -
              pyModCore (Int.ofNat N.toNat) 10).tdiv 10).toNat)
          (pyModCore (Int.ofNat N.toNat) 10) =
        oddDigitProductCore N.toNat 0
    exact
      (oddDigitProductCore_first N.toNat hn hparity).symm
  · intro A N h
    have hcond :
        (N > 0 ∧ A ≠ 0) ∧ pyModCore N 2 = 1 := by
      simpa [_andBool_, «_>Int_», «_=/=Int_», «_==Int_»,
        «pyMod(_,_)_MPY-INT_Int_Int_Int»] using h
    obtain ⟨⟨hN, hA⟩, hparity⟩ := hcond
    have hcast : Int.ofNat N.toNat = N :=
      Int.toNat_of_nonneg (Int.le_of_lt hN)
    have hn : N.toNat ≠ 0 := by
      intro hz
      rw [hz] at hcast
      simp at hcast
      exact (Int.ne_of_gt hN) hcast.symm
    rw [← hcast] at hparity ⊢
    change
      oddDigitProductCore
          (((Int.ofNat N.toNat -
              pyModCore (Int.ofNat N.toNat) 10).tdiv 10).toNat)
          (A * pyModCore (Int.ofNat N.toNat) 10) =
        oddDigitProductCore N.toNat A
    exact
      (oddDigitProductCore_later N.toNat A hn hparity hA).symm

end Proof
