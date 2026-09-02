import Klean76IsSimplePower.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-8464b0da61f140807ea0bf9d284978c8e9beca854f787960b68d619fb825f1ee, rule-03216b3b471d3a9d3f64484ebc0ff5a8d18bceade6710b43811706d8d0373c9b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (a b : SortBool) : SortBool := a && b
/- KORE symbol: Lbl'Unds'orBool'Unds'; frozen source obligations: rule-8464b0da61f140807ea0bf9d284978c8e9beca854f787960b68d619fb825f1ee, rule-03216b3b471d3a9d3f64484ebc0ff5a8d18bceade6710b43811706d8d0373c9b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _orBool_ (a b : SortBool) : SortBool := a || b
/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-8464b0da61f140807ea0bf9d284978c8e9beca854f787960b68d619fb825f1ee, rule-03216b3b471d3a9d3f64484ebc0ff5a8d18bceade6710b43811706d8d0373c9b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>=Int_» (a b : SortInt) : SortBool := decide (a ≥ b)
/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-8464b0da61f140807ea0bf9d284978c8e9beca854f787960b68d619fb825f1ee, rule-03216b3b471d3a9d3f64484ebc0ff5a8d18bceade6710b43811706d8d0373c9b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (a b : SortInt) : SortBool := decide (a ≤ b)
/- KORE symbol: Lbl'UndsEqlsEqls'Bool'Unds'; frozen source obligations: rule-8464b0da61f140807ea0bf9d284978c8e9beca854f787960b68d619fb825f1ee. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Bool_» (a b : SortBool) : SortBool := a == b
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-8464b0da61f140807ea0bf9d284978c8e9beca854f787960b68d619fb825f1ee, rule-03216b3b471d3a9d3f64484ebc0ff5a8d18bceade6710b43811706d8d0373c9b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (a b : SortInt) : SortBool := a == b
/- KORE symbol: Lbl'UndsEqlsSlshEqls'Int'Unds'; frozen source obligations: rule-8464b0da61f140807ea0bf9d284978c8e9beca854f787960b68d619fb825f1ee, rule-03216b3b471d3a9d3f64484ebc0ff5a8d18bceade6710b43811706d8d0373c9b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_=/=Int_» (a b : SortInt) : SortBool := a != b
/- KORE symbol: Lbl'UndsSlsh'Int'Unds'; frozen source obligations: rule-03216b3b471d3a9d3f64484ebc0ff5a8d18bceade6710b43811706d8d0373c9b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_/Int_» (a b : SortInt) : SortInt := Int.tdiv a b
/- KORE symbol: LblpyMod'LParUndsCommUndsRParUnds'MPY-INT'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-8464b0da61f140807ea0bf9d284978c8e9beca854f787960b68d619fb825f1ee, rule-03216b3b471d3a9d3f64484ebc0ff5a8d18bceade6710b43811706d8d0373c9b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «pyMod(_,_)_MPY-INT_Int_Int_Int» (a b : SortInt) : SortInt :=
  Int.tmod (Int.tmod a b + b) b
/- KORE symbol: LblsimplePower'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Int'Unds'Int; frozen source obligations: rule-8464b0da61f140807ea0bf9d284978c8e9beca854f787960b68d619fb825f1ee, rule-03216b3b471d3a9d3f64484ebc0ff5a8d18bceade6710b43811706d8d0373c9b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «simplePower(_,_)_VERIFICATION_Bool_Int_Int» (x n : Int) : Bool :=
  if x == 1 then true
  else if n == 0 then x == 0
  else if n == 1 then false
  else if n == -1 then x == -1
  else if x == 0 then false
  else if «pyMod(_,_)_MPY-INT_Int_Int_Int» x n == 0 then
    «simplePower(_,_)_VERIFICATION_Bool_Int_Int» (Int.tdiv x n) n
  else false
termination_by x.natAbs
decreasing_by
  simp at *
  apply Nat.div_lt_self
  · exact Int.natAbs_pos.mpr (by assumption)
  · have hnabs_ne_one : n.natAbs ≠ 1 := by
      intro hnabs
      have hn := Int.natAbs_eq_iff.mp hnabs
      rcases hn with hn | hn <;> omega
    omega

private theorem pyMod_one_ne_zero {n : Int} (hn : n ≤ -2 ∨ 2 ≤ n) :
    «pyMod(_,_)_MPY-INT_Int_Int_Int» 1 n ≠ 0 := by
  intro hmod
  have hfirst : Int.tmod 1 n = 1 := by
    rcases hn with hn | hn
    · rw [show n = -(-n) by omega, Int.tmod_neg]
      exact Int.tmod_eq_of_lt (by omega) (by omega)
    · exact Int.tmod_eq_of_lt (by omega) (by omega)
  unfold «pyMod(_,_)_MPY-INT_Int_Int_Int» at hmod
  rw [hfirst] at hmod
  have hdivSum : n ∣ 1 + n := Int.dvd_of_tmod_eq_zero hmod
  have hdivOne : n ∣ 1 :=
    (Int.dvd_add_left (Int.dvd_refl n)).mp hdivSum
  have hnabs : n.natAbs = 1 :=
    Nat.eq_one_of_dvd_one (Int.natAbs_dvd_natAbs.mpr hdivOne)
  rcases hn with hn | hn <;> omega

private theorem absBase_excludes {n : Int} (hn : n ≤ -2 ∨ 2 ≤ n) :
    n ≠ 0 ∧ n ≠ 1 ∧ n ≠ -1 := by
  rcases hn with hn | hn <;> omega

theorem final :
    Klean76IsSimplePower.Lemmas.targetStatement _andBool_ _orBool_ «_>=Int_» «_<=Int_» «_==Bool_» «_==Int_» «_=/=Int_» «_/Int_» «pyMod(_,_)_MPY-INT_Int_Int_Int» «simplePower(_,_)_VERIFICATION_Bool_Int_Int» := by
  unfold Klean76IsSimplePower.Lemmas.targetStatement
  constructor
  · intro n x h
    simp only [_andBool_, _orBool_, «_>=Int_», «_<=Int_», «_=/=Int_»,
      Bool.and_eq_true, Bool.or_eq_true, decide_eq_true_eq, bne_iff_ne] at h
    rcases h with ⟨hn, hmod⟩
    obtain ⟨hn0, hn1, hnm1⟩ := absBase_excludes hn
    rw [«simplePower(_,_)_VERIFICATION_Bool_Int_Int».eq_def]
    by_cases hx1 : x = 1
    · simp [«_==Bool_», «_==Int_», hx1]
    · by_cases hx0 : x = 0
      · simp [«_==Bool_», «_==Int_», hx0, hn0, hn1, hnm1]
      · simp [«_==Bool_», «_==Int_», hx1, hx0, hn0, hn1, hnm1, hmod]
  · intro n x h
    simp only [_andBool_, _orBool_, «_>=Int_», «_<=Int_», «_==Int_», «_=/=Int_»,
      Bool.and_eq_true, Bool.or_eq_true, decide_eq_true_eq, bne_iff_ne, beq_iff_eq] at h
    rcases h with ⟨⟨hx0, hn⟩, hmod⟩
    obtain ⟨hn0, hn1, hnm1⟩ := absBase_excludes hn
    have hx1 : x ≠ 1 := by
      intro hx1
      subst x
      exact pyMod_one_ne_zero hn hmod
    rw [«simplePower(_,_)_VERIFICATION_Bool_Int_Int».eq_def]
    simp [hx1, hx0, hn0, hn1, hnm1, hmod, «_/Int_»]

end Proof
