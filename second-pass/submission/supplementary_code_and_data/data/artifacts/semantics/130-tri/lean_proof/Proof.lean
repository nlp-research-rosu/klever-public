import Klean130Tri.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-b0d5d32b6d6da30b8df12d8dc4bcd5eed64ca172053bb4d19b8e4ea5a823e019. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» (a b : SortInt) : SortInt := a - b
/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-daae64b4e1df08d2cccd808f4de05f8ca03d8e60a44b291a388a62df7606e8ac, rule-b0d5d32b6d6da30b8df12d8dc4bcd5eed64ca172053bb4d19b8e4ea5a823e019. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (a b : SortBool) : SortBool := a && b
/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-daae64b4e1df08d2cccd808f4de05f8ca03d8e60a44b291a388a62df7606e8ac, rule-b0d5d32b6d6da30b8df12d8dc4bcd5eed64ca172053bb4d19b8e4ea5a823e019. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>=Int_» (a b : SortInt) : SortBool := decide (a ≥ b)
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-daae64b4e1df08d2cccd808f4de05f8ca03d8e60a44b291a388a62df7606e8ac, rule-b0d5d32b6d6da30b8df12d8dc4bcd5eed64ca172053bb4d19b8e4ea5a823e019. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (a b : SortInt) : SortBool := decide (a = b)
/- KORE symbol: Lbl'UndsPerc'Int'Unds'; frozen source obligations: rule-b0d5d32b6d6da30b8df12d8dc4bcd5eed64ca172053bb4d19b8e4ea5a823e019. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_%Int_» (a b : SortInt) : SortInt := Int.tmod a b
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-daae64b4e1df08d2cccd808f4de05f8ca03d8e60a44b291a388a62df7606e8ac, rule-b0d5d32b6d6da30b8df12d8dc4bcd5eed64ca172053bb4d19b8e4ea5a823e019. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (a b : SortInt) : SortInt := a + b
/- KORE symbol: Lbl'UndsSlsh'Int'Unds'; frozen source obligations: rule-daae64b4e1df08d2cccd808f4de05f8ca03d8e60a44b291a388a62df7606e8ac, rule-b0d5d32b6d6da30b8df12d8dc4bcd5eed64ca172053bb4d19b8e4ea5a823e019. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_/Int_» (a b : SortInt) : SortInt := Int.tdiv a b
/- KORE symbol: LblpyMod'LParUndsCommUndsRParUnds'MPY-INT'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-daae64b4e1df08d2cccd808f4de05f8ca03d8e60a44b291a388a62df7606e8ac. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «pyMod(_,_)_MPY-INT_Int_Int_Int» (a b : SortInt) : SortInt :=
  Int.tmod (Int.tmod a b + b) b
/- KORE symbol: LbltriAt; frozen source obligations: rule-daae64b4e1df08d2cccd808f4de05f8ca03d8e60a44b291a388a62df7606e8ac, rule-b0d5d32b6d6da30b8df12d8dc4bcd5eed64ca172053bb4d19b8e4ea5a823e019. Replace this stub with its honest total meaning from the frozen K semantics. -/
/- The frozen sequence is `i /Int 2 +Int 1` at even indices.  At an
   odd index `i = 2*k-1`, its two-step recurrence has the closed value
   `k*(k+2)`.  The same frozen pyMod expression selects the branch. -/
def triAt (i : SortInt) : SortInt :=
  if Int.tmod (Int.tmod i 2 + 2) 2 = 0 then
    Int.tdiv i 2 + 1
  else
    let k := Int.tdiv (i + 1) 2
    k * (k + 2)

theorem final :
    Klean130Tri.Lemmas.targetStatement «_-Int_» _andBool_ «_>=Int_» «_==Int_» «_%Int_» «_+Int_» «_/Int_» «pyMod(_,_)_MPY-INT_Int_Int_Int» triAt := by
  unfold Klean130Tri.Lemmas.targetStatement
  constructor
  · intro I h
    simp [_andBool_, «_>=Int_», «_==Int_», «_+Int_»,
      «_/Int_», «pyMod(_,_)_MPY-INT_Int_Int_Int»] at h ⊢
    rw [triAt, if_pos h.2]
  · intro I h
    simp [«_-Int_», _andBool_, «_>=Int_», «_==Int_», «_%Int_», «_+Int_»,
      «_/Int_»] at h ⊢
    rcases h with ⟨hge, hParity⟩
    let J : Int := I
    have hgeJ : (3 : Int) ≤ J := by exact hge
    have hParityJ : Int.tmod (Int.tmod J 2 + 2) 2 = 1 := by exact hParity
    have pyMod_two_eq_emod (x : Int) (hx : 0 ≤ x) :
        Int.tmod (Int.tmod x 2 + 2) 2 = x % 2 := by
      rw [Int.tmod_eq_emod_of_nonneg hx]
      rw [Int.tmod_eq_emod_of_nonneg]
      · omega
      · exact Int.add_nonneg (Int.emod_nonneg x (by decide)) (by decide)
    have hJ : (0 : Int) ≤ J := by omega
    have hJm1 : (0 : Int) ≤ J + -1 := by omega
    have hJm2 : (0 : Int) ≤ J + -2 := by omega
    have hJp1 : (0 : Int) ≤ J + 1 := by omega
    have hmodJ : J % (2 : Int) = 1 := by
      rw [← pyMod_two_eq_emod J hJ]
      exact hParityJ
    have hEvenPrev :
        Int.tmod (Int.tmod (J + -1) 2 + 2) 2 = 0 := by
      rw [pyMod_two_eq_emod (J + -1) hJm1]
      omega
    have hOddPrev :
        Int.tmod (Int.tmod (J + -2) 2 + 2) 2 ≠ 0 := by
      rw [pyMod_two_eq_emod (J + -2) hJm2]
      omega
    have hOdd :
        Int.tmod (Int.tmod J 2 + 2) 2 ≠ 0 := by
      rw [pyMod_two_eq_emod J hJ]
      omega
    have hEvenNext :
        Int.tmod (Int.tmod (J + 1) 2 + 2) 2 = 0 := by
      rw [pyMod_two_eq_emod (J + 1) hJp1]
      omega
    have hArg : J + -2 + 1 = J + -1 := by omega
    have hDiv :
        Int.tdiv (J + 1) 2 = Int.tdiv (J + -1) 2 + 1 := by
      rw [Int.tdiv_eq_ediv_of_nonneg hJp1,
        Int.tdiv_eq_ediv_of_nonneg hJm1]
      omega
    change
      ((triAt (J + -1) + triAt (J + -2)) + 1) +
          Int.tdiv ((J + 1) - Int.tmod (Int.tmod (J + 1) 2 + 2) 2) 2 =
        triAt J
    simp [triAt, hEvenPrev, hOddPrev, hOdd, hEvenNext]
    rw [hArg, hDiv]
    grind

end Proof
