import Proof

namespace BridgeDefinitionProof

def F (n : SortInt) : SortInt :=
  Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» n

example : F 0 = 0 := by
  simp [
    F,
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»,
    Proof.FibfibModel.fibfibInt,
    Proof.FibfibModel.fibfibNat
  ]

example : F 1 = 0 := by
  simp [
    F,
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»,
    Proof.FibfibModel.fibfibInt,
    Proof.FibfibModel.fibfibNat
  ]

example : F 2 = 1 := by
  simp [
    F,
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»,
    Proof.FibfibModel.fibfibInt,
    Proof.FibfibModel.fibfibNat
  ]

example (n : SortInt) (h : n < 0) : F n = 0 := by
  have hn : n.toNat = 0 :=
    Int.toNat_of_nonpos (Int.le_of_lt h)
  simp [
    F,
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»,
    Proof.FibfibModel.fibfibInt,
    Proof.FibfibModel.fibfibNat,
    hn
  ]

example (n : SortInt) (h : n ≥ 3) :
    F n = F (n - 1) + F (n - 2) + F (n - 3) := by
  have hi : 0 ≤ n - 3 := Int.sub_nonneg_of_le h
  have recurrence :=
    Proof.FibfibModel.fibfibInt_add_three (n - 3) hi
  have h1 : n - 3 + 1 = n - 2 := by
    simp [Int.sub_eq_add_neg, Int.add_assoc]
  have h2 : n - 3 + 2 = n - 1 := by
    simp [Int.sub_eq_add_neg, Int.add_assoc]
  have h3 : n - 3 + 3 = n := by
    simp
  rw [h1, h2, h3] at recurrence
  simp only [
    F,
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»
  ]
  calc
    Proof.FibfibModel.fibfibInt n =
        Proof.FibfibModel.fibfibInt (n - 3) +
        Proof.FibfibModel.fibfibInt (n - 2) +
        Proof.FibfibModel.fibfibInt (n - 1) := recurrence.symm
    _ =
        Proof.FibfibModel.fibfibInt (n - 1) +
        Proof.FibfibModel.fibfibInt (n - 2) +
        Proof.FibfibModel.fibfibInt (n - 3) := by ac_rfl

example (x y : SortInt) :
    Proof.«_+Int_» x y = x + y := by rfl

example (x y : SortInt) :
    Proof.«_>=Int_» x y = decide (x ≥ y) := by rfl

end BridgeDefinitionProof
