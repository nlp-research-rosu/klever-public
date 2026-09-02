import Klean161Solve.Lemmas

namespace Proof

/- KORE symbol: Lbl'UndsEqlsEqls'K'Unds'; frozen source obligations: rule-387d11f8474864387ce45c90f1ba7bc44da2dcb0e552a8b7845434062e527a49. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_==K_» (lhs rhs : SortK) : SortBool := by
  classical
  exact if lhs = rhs then true else false

theorem final :
    Klean161Solve.Lemmas.targetStatement «_==K_» := by
  simp [Klean161Solve.Lemmas.targetStatement, «_==K_»]

end Proof
