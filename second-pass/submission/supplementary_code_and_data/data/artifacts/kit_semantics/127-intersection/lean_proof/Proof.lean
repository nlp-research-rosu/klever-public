import Klean127Intersection.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-7dcc581fc2eb7b71715119443ca2ecc1192932d0a0273a3e90bd21562ae85ff4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (left right : SortBool) : SortBool := left && right
/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-7dcc581fc2eb7b71715119443ca2ecc1192932d0a0273a3e90bd21562ae85ff4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>=Int_» (left right : SortInt) : SortBool := decide (left ≥ right)
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-7dcc581fc2eb7b71715119443ca2ecc1192932d0a0273a3e90bd21562ae85ff4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (left right : SortInt) : SortBool := decide (left < right)
/- KORE symbol: Lbl'UndsEqlsSlshEqls'Int'Unds'; frozen source obligations: rule-7dcc581fc2eb7b71715119443ca2ecc1192932d0a0273a3e90bd21562ae85ff4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_=/=Int_» (left right : SortInt) : SortBool := decide (left ≠ right)
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-7dcc581fc2eb7b71715119443ca2ecc1192932d0a0273a3e90bd21562ae85ff4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (left right : SortInt) : SortInt := left + right
/- KORE symbol: LblpyMod'LParUndsCommUndsRParUnds'MPY-INT'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-7dcc581fc2eb7b71715119443ca2ecc1192932d0a0273a3e90bd21562ae85ff4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «pyMod(_,_)_MPY-INT_Int_Int_Int» (dividend divisor : SortInt) : SortInt :=
  Int.tmod (Int.tmod dividend divisor + divisor) divisor
/- KORE symbol: LblscanHasDivisor'LParUndsCommUndsCommUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'Bool'Unds'Int'Unds'Int; frozen source obligations: rule-7dcc581fc2eb7b71715119443ca2ecc1192932d0a0273a3e90bd21562ae85ff4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def scanFrom (number divisor : SortInt) : Nat → SortBool
  | 0 => false
  | fuel + 1 =>
      if «pyMod(_,_)_MPY-INT_Int_Int_Int» number divisor = 0 then
        true
      else
        scanFrom number (divisor + 1) fuel

def «scanHasDivisor(_,_,_)_VERIFICATION-SYNTAX_Bool_Bool_Int_Int»
    (seen : SortBool) (number divisor : SortInt) : SortBool :=
  if seen then
    true
  else
    let start := if divisor < 2 then 2 else divisor
    scanFrom number start (number - start).toNat

theorem final :
    Klean127Intersection.Lemmas.targetStatement _andBool_ «_>=Int_» «_<Int_» «_=/=Int_» «_+Int_» «pyMod(_,_)_MPY-INT_Int_Int_Int» «scanHasDivisor(_,_,_)_VERIFICATION-SYNTAX_Bool_Bool_Int_Int» := by
  unfold Klean127Intersection.Lemmas.targetStatement
  intro D N h
  change
    ((decide (D ≥ 2) && decide (D < N)) &&
      decide («pyMod(_,_)_MPY-INT_Int_Int_Int» N D ≠ 0)) = true at h
  have outer := Bool.and_eq_true_iff.mp h
  have inner := Bool.and_eq_true_iff.mp outer.1
  have hD : D ≥ 2 := of_decide_eq_true inner.1
  have hDN : D < N := of_decide_eq_true inner.2
  have hmod : «pyMod(_,_)_MPY-INT_Int_Int_Int» N D ≠ 0 :=
    of_decide_eq_true outer.2
  have hDstart : ¬D < 2 := Int.not_lt_of_ge hD
  have hDnextStart : ¬D + 1 < 2 :=
    Int.not_lt_of_ge (Int.le_add_one hD)
  have hnextNonnegative : 0 ≤ N - (D + 1) :=
    Int.sub_nonneg_of_le (Int.add_one_le_of_lt hDN)
  have hfuel : (N - D).toNat = (N - (D + 1)).toNat + 1 := by
    rw [show N - D = (N - (D + 1)) + 1 by
      simp [Int.sub_eq_add_neg, Int.neg_add, Int.add_assoc]]
    exact Int.toNat_add_nat hnextNonnegative 1
  simp only [«scanHasDivisor(_,_,_)_VERIFICATION-SYNTAX_Bool_Bool_Int_Int»,
    «_+Int_», Bool.false_eq_true, ↓reduceIte, hDstart, hDnextStart]
  rw [hfuel]
  simp [scanFrom, hmod]

end Proof
