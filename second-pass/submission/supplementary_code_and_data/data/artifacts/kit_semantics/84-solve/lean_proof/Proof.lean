import Klean84Solve.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» (x y : SortInt) : SortInt := x - y
/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-6c41bb59ad1d9e21227b52ea306abb7b34b84c951d9e8989d939daab63c61f3a, rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (x y : SortBool) : SortBool := x && y
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-6c41bb59ad1d9e21227b52ea306abb7b34b84c951d9e8989d939daab63c61f3a, rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (x y : SortInt) : SortBool := decide (x < y)
/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-6c41bb59ad1d9e21227b52ea306abb7b34b84c951d9e8989d939daab63c61f3a, rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (x y : SortInt) : SortBool := decide (x ≤ y)
/- KORE symbol: Lbl'UndsPerc'Int'Unds'; frozen source obligations: rule-6c41bb59ad1d9e21227b52ea306abb7b34b84c951d9e8989d939daab63c61f3a. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_%Int_» (x y : SortInt) : SortInt := Int.tmod x y
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-6c41bb59ad1d9e21227b52ea306abb7b34b84c951d9e8989d939daab63c61f3a, rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x y : SortInt) : SortInt := x + y
/- KORE symbol: Lbl'UndsSlsh'Int'Unds'; frozen source obligations: rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_/Int_» (x y : SortInt) : SortInt := Int.tdiv x y
/- KORE symbol: Lbl'UndsStar'Int'Unds'; frozen source obligations: rule-6c41bb59ad1d9e21227b52ea306abb7b34b84c951d9e8989d939daab63c61f3a, rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_*Int_» (x y : SortInt) : SortInt := x * y

theorem final :
    Klean84Solve.Lemmas.targetStatement «_-Int_» _andBool_ «_<Int_» «_<=Int_» «_%Int_» «_+Int_» «_/Int_» «_*Int_» := by
  unfold Klean84Solve.Lemmas.targetStatement
  constructor
  · intro Q D h
    simp [_andBool_, «_<=Int_», «_<Int_»] at h
    have hmod : D % 10 = D := Int.emod_eq_of_lt h.1 h.2
    have hD10 : 0 ≤ D + 10 :=
      Int.add_nonneg h.1 (by decide)
    by_cases hc : 0 ≤ D + 10 * Q ∨ (10 : Int) ∣ D
    · simp [«_%Int_», «_+Int_», «_*Int_», Int.tmod_eq_emod,
        hmod, hD10, hc]
    · simp [«_%Int_», «_+Int_», «_*Int_», Int.tmod_eq_emod,
        hmod, h.1, hc]
  · intro D Q h
    simp [_andBool_, «_<=Int_», «_<Int_»] at h
    change Int.tdiv (D + 10 * Q - D) 10 = Q
    rw [Int.add_comm D (10 * Q), Int.add_sub_cancel]
    exact Int.mul_tdiv_cancel_left Q (by decide)

end Proof
