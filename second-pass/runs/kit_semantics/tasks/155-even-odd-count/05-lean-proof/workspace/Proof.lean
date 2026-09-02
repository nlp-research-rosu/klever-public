import Klean155EvenOddCount.Lemmas
import Std.Tactic

namespace Proof

/- Decimal-digit counters used to implement the four VERIFICATION summaries.
   The zero terminator contributes no digit; `decEven` supplies the source
   program's special result for the integer zero. -/
private def evenDigitCount (n : Nat) : Int :=
  if h : n = 0 then 0
  else 1 - Int.ofNat (n % 2) + evenDigitCount (n / 10)
termination_by n
decreasing_by
  exact Nat.div_lt_self (Nat.pos_of_ne_zero h) (by omega)

private def oddDigitCount (n : Nat) : Int :=
  if n = 0 then 0
  else Int.ofNat (n % 2) + oddDigitCount (n / 10)
termination_by n
decreasing_by
  apply Nat.div_lt_self <;> omega

private theorem evenDigitCount_step (n : Nat) (h : 0 < n) :
    evenDigitCount n =
      1 - Int.ofNat (n % 2) + evenDigitCount (n / 10) := by
  rw [evenDigitCount]
  simp [Nat.ne_of_gt h]

private theorem oddDigitCount_step (n : Nat) (h : 0 < n) :
    oddDigitCount n = Int.ofNat (n % 2) + oddDigitCount (n / 10) := by
  rw [oddDigitCount]
  simp [Nat.ne_of_gt h]

private def evenMagnitude (n : Int) : Int := evenDigitCount n.natAbs
private def oddMagnitude (n : Int) : Int := oddDigitCount n.natAbs

/- On positive integers, K's normalized remainder expressions are ordinary
   decimal remainders and K's truncated quotient removes the last digit. -/
private theorem positive_normalizations (n : Int) (h : n > 0) :
    Int.tmod (Int.tmod n 2 + 2) 2 = Int.ofNat (n.natAbs % 2) ∧
    Int.tdiv (n - Int.tmod (Int.tmod n 10 + 10) 10) 10 =
      Int.ofNat (n.natAbs / 10) := by
  cases n with
  | ofNat m =>
      constructor
      · change Int.ofNat ((m % 2 + 2) % 2) = Int.ofNat (m % 2)
        simp
      · have hlast :
            Int.tmod (Int.tmod (Int.ofNat m) 10 + 10) 10 =
              Int.ofNat (m % 10) := by
          change Int.ofNat ((m % 10 + 10) % 10) = Int.ofNat (m % 10)
          simp
        rw [hlast]
        have hle : m % 10 ≤ m := Nat.mod_le m 10
        have hsub :
            Int.ofNat m - Int.ofNat (m % 10) =
              Int.ofNat (m - m % 10) := (Int.ofNat_sub hle).symm
        rw [hsub]
        change Int.ofNat ((m - m % 10) / 10) = Int.ofNat (m / 10)
        have hdecomp := Nat.mod_add_div' m 10
        have hsubnat : m - m % 10 = m / 10 * 10 := by omega
        rw [hsubnat]
        simp
  | negSucc m => omega

private theorem evenMagnitude_step (n : Int) (h : n > 0) :
    evenMagnitude n =
      1 - Int.tmod (Int.tmod n 2 + 2) 2 +
        evenMagnitude
          (Int.tdiv (n - Int.tmod (Int.tmod n 10 + 10) 10) 10) := by
  have hn : 0 < n.natAbs := Int.natAbs_pos.mpr (by omega)
  rw [evenMagnitude, evenDigitCount_step n.natAbs hn]
  obtain ⟨hparity, hquotient⟩ := positive_normalizations n h
  rw [hparity, hquotient]
  rw [evenMagnitude]
  rfl

private theorem oddMagnitude_step (n : Int) (h : n > 0) :
    oddMagnitude n =
      Int.tmod (Int.tmod n 2 + 2) 2 +
        oddMagnitude
          (Int.tdiv (n - Int.tmod (Int.tmod n 10 + 10) 10) 10) := by
  have hn : 0 < n.natAbs := Int.natAbs_pos.mpr (by omega)
  rw [oddMagnitude, oddDigitCount_step n.natAbs hn]
  obtain ⟨hparity, hquotient⟩ := positive_normalizations n h
  rw [hparity, hquotient]
  rw [oddMagnitude]
  rfl

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-5a0a2cc7a4d444f988e3cebb6dc26aebd6f8dde901db6bda39bde915d219c1cb, rule-72eaeaa9cbb5d008fe6415d81db969a48965568d1278c34ae925816b5e85b44f, rule-316f5e2aa29d4aa0e25b0c2870a62f8dbc956a33e3070de5c80aafba74e0893d, rule-e0dab4a9b20997030cfca78b7b30e2b46b8e7ec4b5649685518b6d53684edc98. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» : SortInt → SortInt → SortInt := Int.sub
/- KORE symbol: Lbl'Unds-GT-'Int'Unds'; frozen source obligations: rule-2f7142f79fcc9e619c4580decceb38a73bb3716819a71c7503d94cb1dc77b79c, rule-2a60622c3bbfa43590a66aa9e80b161f0edcd18ff09827cc120a8dec01c2e0b6, rule-61db74cde356f6655a9b1b0684b4d8bce65291a3f9cd8deb327f942ea6a7d071, rule-0f9ee7597728fa7f27d3d9ad4a8f4339e78c38563b31dbb6199eea9aa11d82ec, rule-5a0a2cc7a4d444f988e3cebb6dc26aebd6f8dde901db6bda39bde915d219c1cb, rule-72eaeaa9cbb5d008fe6415d81db969a48965568d1278c34ae925816b5e85b44f, rule-316f5e2aa29d4aa0e25b0c2870a62f8dbc956a33e3070de5c80aafba74e0893d, rule-e0dab4a9b20997030cfca78b7b30e2b46b8e7ec4b5649685518b6d53684edc98. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>Int_» (a b : SortInt) : SortBool := decide (a > b)
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-bf2f17042baead9b767eb8154375d9748d18a100e17da03642a77cfe406ce383, rule-b844cb11342eaa449e577cd7e74b99d3283bacf3b169e29c94235f1c7edc1748. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (a b : SortInt) : SortBool := a == b
/- KORE symbol: Lbl'UndsPerc'Int'Unds'; frozen source obligations: rule-5a0a2cc7a4d444f988e3cebb6dc26aebd6f8dde901db6bda39bde915d219c1cb, rule-72eaeaa9cbb5d008fe6415d81db969a48965568d1278c34ae925816b5e85b44f, rule-316f5e2aa29d4aa0e25b0c2870a62f8dbc956a33e3070de5c80aafba74e0893d, rule-e0dab4a9b20997030cfca78b7b30e2b46b8e7ec4b5649685518b6d53684edc98. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_%Int_» : SortInt → SortInt → SortInt := Int.tmod
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-5a0a2cc7a4d444f988e3cebb6dc26aebd6f8dde901db6bda39bde915d219c1cb, rule-72eaeaa9cbb5d008fe6415d81db969a48965568d1278c34ae925816b5e85b44f, rule-316f5e2aa29d4aa0e25b0c2870a62f8dbc956a33e3070de5c80aafba74e0893d, rule-e0dab4a9b20997030cfca78b7b30e2b46b8e7ec4b5649685518b6d53684edc98. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» : SortInt → SortInt → SortInt := Int.add
/- KORE symbol: Lbl'UndsSlsh'Int'Unds'; frozen source obligations: rule-5a0a2cc7a4d444f988e3cebb6dc26aebd6f8dde901db6bda39bde915d219c1cb, rule-72eaeaa9cbb5d008fe6415d81db969a48965568d1278c34ae925816b5e85b44f, rule-316f5e2aa29d4aa0e25b0c2870a62f8dbc956a33e3070de5c80aafba74e0893d, rule-e0dab4a9b20997030cfca78b7b30e2b46b8e7ec4b5649685518b6d53684edc98. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_/Int_» : SortInt → SortInt → SortInt := Int.tdiv
/- KORE symbol: LblabsInt'LParUndsRParUnds'INT-COMMON'Unds'Int'Unds'Int; frozen source obligations: rule-bf2f17042baead9b767eb8154375d9748d18a100e17da03642a77cfe406ce383, rule-b844cb11342eaa449e577cd7e74b99d3283bacf3b169e29c94235f1c7edc1748, rule-2f7142f79fcc9e619c4580decceb38a73bb3716819a71c7503d94cb1dc77b79c, rule-2a60622c3bbfa43590a66aa9e80b161f0edcd18ff09827cc120a8dec01c2e0b6, rule-61db74cde356f6655a9b1b0684b4d8bce65291a3f9cd8deb327f942ea6a7d071, rule-0f9ee7597728fa7f27d3d9ad4a8f4339e78c38563b31dbb6199eea9aa11d82ec. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «absInt(_)_INT-COMMON_Int_Int» (n : SortInt) : SortInt :=
  Int.ofNat n.natAbs
/- KORE symbol: LbldecEven'LParUndsRParUnds'VERIFICATION'Unds'Int'Unds'Int; frozen source obligations: rule-bf2f17042baead9b767eb8154375d9748d18a100e17da03642a77cfe406ce383, rule-2f7142f79fcc9e619c4580decceb38a73bb3716819a71c7503d94cb1dc77b79c, rule-2a60622c3bbfa43590a66aa9e80b161f0edcd18ff09827cc120a8dec01c2e0b6. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «decEven(_)_VERIFICATION_Int_Int» (n : SortInt) : SortInt :=
  if n = 0 then 1 else evenMagnitude n
/- KORE symbol: LbldecOdd'LParUndsRParUnds'VERIFICATION'Unds'Int'Unds'Int; frozen source obligations: rule-b844cb11342eaa449e577cd7e74b99d3283bacf3b169e29c94235f1c7edc1748, rule-61db74cde356f6655a9b1b0684b4d8bce65291a3f9cd8deb327f942ea6a7d071, rule-0f9ee7597728fa7f27d3d9ad4a8f4339e78c38563b31dbb6199eea9aa11d82ec. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «decOdd(_)_VERIFICATION_Int_Int» (n : SortInt) : SortInt :=
  if n = 0 then 0 else oddMagnitude n
/- KORE symbol: LblevenPos'LParUndsRParUnds'VERIFICATION'Unds'Int'Unds'Int; frozen source obligations: rule-2f7142f79fcc9e619c4580decceb38a73bb3716819a71c7503d94cb1dc77b79c, rule-2a60622c3bbfa43590a66aa9e80b161f0edcd18ff09827cc120a8dec01c2e0b6, rule-5a0a2cc7a4d444f988e3cebb6dc26aebd6f8dde901db6bda39bde915d219c1cb, rule-72eaeaa9cbb5d008fe6415d81db969a48965568d1278c34ae925816b5e85b44f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «evenPos(_)_VERIFICATION_Int_Int» (n : SortInt) : SortInt :=
  evenMagnitude n
/- KORE symbol: LbloddPos'LParUndsRParUnds'VERIFICATION'Unds'Int'Unds'Int; frozen source obligations: rule-61db74cde356f6655a9b1b0684b4d8bce65291a3f9cd8deb327f942ea6a7d071, rule-0f9ee7597728fa7f27d3d9ad4a8f4339e78c38563b31dbb6199eea9aa11d82ec, rule-316f5e2aa29d4aa0e25b0c2870a62f8dbc956a33e3070de5c80aafba74e0893d, rule-e0dab4a9b20997030cfca78b7b30e2b46b8e7ec4b5649685518b6d53684edc98. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «oddPos(_)_VERIFICATION_Int_Int» (n : SortInt) : SortInt :=
  oddMagnitude n

theorem final :
    Klean155EvenOddCount.Lemmas.targetStatement «_-Int_» «_>Int_» «_==Int_» «_%Int_» «_+Int_» «_/Int_» «absInt(_)_INT-COMMON_Int_Int» «decEven(_)_VERIFICATION_Int_Int» «decOdd(_)_VERIFICATION_Int_Int» «evenPos(_)_VERIFICATION_Int_Int» «oddPos(_)_VERIFICATION_Int_Int» := by
  unfold Klean155EvenOddCount.Lemmas.targetStatement
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro n h
    have hn : n = 0 := by
      simpa [«_==Int_», «absInt(_)_INT-COMMON_Int_Int»] using h
    simp [hn, «decEven(_)_VERIFICATION_Int_Int»]
  · intro n h
    have hn : n = 0 := by
      simpa [«_==Int_», «absInt(_)_INT-COMMON_Int_Int»] using h
    simp [hn, «decOdd(_)_VERIFICATION_Int_Int»]
  · intro n h
    have hpos : Int.ofNat n.natAbs > 0 := by
      simpa [«_>Int_», «absInt(_)_INT-COMMON_Int_Int»] using h
    have hn : n ≠ 0 := by
      intro hn
      simp [hn] at hpos
    unfold «evenPos(_)_VERIFICATION_Int_Int»
      «decEven(_)_VERIFICATION_Int_Int»
    rw [if_neg hn]
    unfold evenMagnitude «absInt(_)_INT-COMMON_Int_Int»
    rfl
  · intro n h
    have hpos : Int.ofNat n.natAbs > 0 := by
      simpa [«_>Int_», «absInt(_)_INT-COMMON_Int_Int»] using h
    have hn : n ≠ 0 := by
      intro hn
      simp [hn] at hpos
    unfold «evenPos(_)_VERIFICATION_Int_Int»
      «decEven(_)_VERIFICATION_Int_Int»
    rw [if_neg hn]
    unfold evenMagnitude «absInt(_)_INT-COMMON_Int_Int»
    rfl
  · intro n h
    have hpos : Int.ofNat n.natAbs > 0 := by
      simpa [«_>Int_», «absInt(_)_INT-COMMON_Int_Int»] using h
    have hn : n ≠ 0 := by
      intro hn
      simp [hn] at hpos
    unfold «oddPos(_)_VERIFICATION_Int_Int»
      «decOdd(_)_VERIFICATION_Int_Int»
    rw [if_neg hn]
    unfold oddMagnitude «absInt(_)_INT-COMMON_Int_Int»
    rfl
  · intro n h
    have hpos : Int.ofNat n.natAbs > 0 := by
      simpa [«_>Int_», «absInt(_)_INT-COMMON_Int_Int»] using h
    have hn : n ≠ 0 := by
      intro hn
      simp [hn] at hpos
    unfold «oddPos(_)_VERIFICATION_Int_Int»
      «decOdd(_)_VERIFICATION_Int_Int»
    rw [if_neg hn]
    unfold oddMagnitude «absInt(_)_INT-COMMON_Int_Int»
    rfl
  · intro n e h
    have hn : n > 0 := by simpa [«_>Int_»] using h
    simp only [«_+Int_», «_-Int_», «_%Int_», «_/Int_»,
      «evenPos(_)_VERIFICATION_Int_Int»]
    rw [evenMagnitude_step n hn]
    change e +
        (1 - Int.tmod (Int.tmod n 2 + 2) 2 +
          evenMagnitude
            (Int.tdiv (n - Int.tmod (Int.tmod n 10 + 10) 10) 10)) =
      (e + 1 - Int.tmod (Int.tmod n 2 + 2) 2) +
        evenMagnitude
          (Int.tdiv (n - Int.tmod (Int.tmod n 10 + 10) 10) 10)
    simp [Int.sub_eq_add_neg, Int.add_assoc]
  · intro n e h
    have hn : n > 0 := by simpa [«_>Int_»] using h
    simp only [«_+Int_», «_-Int_», «_%Int_», «_/Int_»,
      «evenPos(_)_VERIFICATION_Int_Int»]
    rw [evenMagnitude_step n hn]
    change (e + 1 - Int.tmod (Int.tmod n 2 + 2) 2) +
        evenMagnitude
          (Int.tdiv (n - Int.tmod (Int.tmod n 10 + 10) 10) 10) =
      e +
        (1 - Int.tmod (Int.tmod n 2 + 2) 2 +
          evenMagnitude
            (Int.tdiv (n - Int.tmod (Int.tmod n 10 + 10) 10) 10))
    simp [Int.sub_eq_add_neg, Int.add_assoc]
  · intro n o h
    have hn : n > 0 := by simpa [«_>Int_»] using h
    simp only [«_+Int_», «_-Int_», «_%Int_», «_/Int_»,
      «oddPos(_)_VERIFICATION_Int_Int»]
    rw [oddMagnitude_step n hn]
    change o +
        (Int.tmod (Int.tmod n 2 + 2) 2 +
          oddMagnitude
            (Int.tdiv (n - Int.tmod (Int.tmod n 10 + 10) 10) 10)) =
      (o + Int.tmod (Int.tmod n 2 + 2) 2) +
        oddMagnitude
          (Int.tdiv (n - Int.tmod (Int.tmod n 10 + 10) 10) 10)
    simp [Int.add_assoc]
  · intro n o h
    have hn : n > 0 := by simpa [«_>Int_»] using h
    simp only [«_+Int_», «_-Int_», «_%Int_», «_/Int_»,
      «oddPos(_)_VERIFICATION_Int_Int»]
    rw [oddMagnitude_step n hn]
    change (o + Int.tmod (Int.tmod n 2 + 2) 2) +
        oddMagnitude
          (Int.tdiv (n - Int.tmod (Int.tmod n 10 + 10) 10) 10) =
      o +
        (Int.tmod (Int.tmod n 2 + 2) 2 +
          oddMagnitude
            (Int.tdiv (n - Int.tmod (Int.tmod n 10 + 10) 10) 10))
    simp [Int.add_assoc]

end Proof
