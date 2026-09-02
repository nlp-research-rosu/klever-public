import Klean63Fibfib.Lemmas
import Lean.Elab.Tactic.Omega

namespace Proof.FibfibModel

/-- The frozen `fibfibSpec` recurrence on natural-number indices. -/
def fibfibNat : Nat → Int
  | 0 => 0
  | 1 => 0
  | 2 => 1
  | n + 3 => fibfibNat n + fibfibNat (n + 1) + fibfibNat (n + 2)
termination_by n => n
decreasing_by all_goals omega

theorem fibfibNat_add_three (n : Nat) :
    fibfibNat (n + 3) =
      fibfibNat n + fibfibNat (n + 1) + fibfibNat (n + 2) := by
  rw [fibfibNat]

/--
The total frozen K summary on integers. Negative integers map through
`Int.toNat` to zero, so they have the frozen totalization value `0`.
-/
def fibfibInt (n : Int) : Int :=
  fibfibNat n.toNat

theorem fibfibInt_add_three (i : Int) (h : 0 ≤ i) :
    fibfibInt i + fibfibInt (i + 1) + fibfibInt (i + 2) =
      fibfibInt (i + 3) := by
  have h1 : (i + 1).toNat = i.toNat + 1 := by omega
  have h2 : (i + 2).toNat = i.toNat + 2 := by omega
  have h3 : (i + 3).toNat = i.toNat + 3 := by omega
  simp only [fibfibInt, h1, h2, h3]
  exact (fibfibNat_add_three i.toNat).symm

end Proof.FibfibModel
