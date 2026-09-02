import Klean77Iscube.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027, rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» (x y : SortInt) : SortInt := x - y
/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027, rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (x y : SortBool) : SortBool := x && y
/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>=Int_» (x y : SortInt) : SortBool := decide (x >= y)
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027, rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (x y : SortInt) : SortBool := decide (x < y)
/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027, rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (x y : SortInt) : SortBool := decide (x <= y)
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (x y : SortInt) : SortBool := decide (x = y)
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027, rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x y : SortInt) : SortInt := x + y
/- KORE symbol: Lbl'UndsStar'Int'Unds'; frozen source obligations: rule-71fab8be3031badfbb8efe37c8587b786b455d6670cf74a013dbf65634d49027, rule-5cd618327b17d41867b4a5cadea7277532d58e8066be05ee8bd76b5c99b6690f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_*Int_» (x y : SortInt) : SortInt := x * y

theorem final :
    Klean77Iscube.Lemmas.targetStatement «_-Int_» _andBool_ «_>=Int_» «_<Int_» «_<=Int_» «_==Int_» «_+Int_» «_*Int_» := by
  constructor
  · intro N I D h
    simp only [
      _andBool_, «_<=Int_», «_<Int_», «_+Int_», «_-Int_», «_*Int_»,
      Bool.and_eq_true, decide_eq_true_eq
    ] at h ⊢
    rcases h with ⟨⟨⟨⟨⟨hI0, hIupper⟩, hN0⟩, hD0⟩, hDgap⟩, hguard⟩
    by_cases hlt : I < N + 1
    · exact hlt
    · have heq : I = N + 1 :=
        Int.le_antisymm hIupper (Int.le_of_not_gt hlt)
      subst I
      have hsum :
          N * N * N + D < (N + 1) * (N + 1) * (N + 1) :=
        Int.add_lt_of_lt_sub_left hDgap
      exact False.elim (Int.lt_asymm hguard hsum)
  · intro N I D h
    simp only [
      _andBool_, «_<=Int_», «_<Int_», «_>=Int_», «_==Int_», «_+Int_»,
      «_-Int_», «_*Int_», Bool.and_eq_true, decide_eq_true_eq
    ] at h ⊢
    rcases h with ⟨⟨⟨⟨⟨hI0, hIupper⟩, hN0⟩, hD0⟩, hDgap⟩, hguard⟩
    by_cases heq : I = N + 1
    · exact heq
    · have hlt : I < N + 1 :=
        Int.lt_iff_le_and_ne.mpr ⟨hIupper, heq⟩
      have hIN : I ≤ N := Int.le_of_lt_add_one hlt
      have hNN0 : 0 ≤ N * N := Int.mul_nonneg hN0 hN0
      have hsq : I * I ≤ N * N := Int.mul_le_mul hIN hIN hI0 hN0
      have hcube : (I * I) * I ≤ (N * N) * N :=
        Int.mul_le_mul hsq hIN hI0 hNN0
      have hbase : N * N * N < N * N * N + D :=
        Int.lt_add_of_pos_right _ hD0
      have hbaseToI : N * N * N < I * I * I :=
        Int.lt_of_lt_of_le hbase hguard
      exact False.elim (Int.not_lt_of_ge hcube hbaseToI)

end Proof
