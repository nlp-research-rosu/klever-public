import Proof

namespace BridgeAudit

open Klean63Fibfib

#eval [
  Proof.«_>=Int_» (-1) 0,
  Proof.«_>=Int_» 0 0,
  Proof.«_>=Int_» 7 0,
  Proof.«_>=Int_» 2 3
]

#eval [
  Proof.«_+Int_» (-4) 7,
  Proof.«_+Int_» 0 0,
  Proof.«_+Int_» 12 (-5)
]

#eval [
  Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» (-5),
  Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» (-1),
  Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» 0,
  Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» 1,
  Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» 2,
  Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» 3,
  Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» 4,
  Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» 5,
  Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» 8,
  Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» 12
]

example : Proof.«_>=Int_» (-1) 0 = false := by decide
example : Proof.«_>=Int_» 0 0 = true := by decide
example : Proof.«_+Int_» (-4) 7 = 3 := by decide
example :
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» (-5) = 0 := by
  simp [
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»,
    Proof.FibfibModel.fibfibInt,
    Proof.FibfibModel.fibfibNat
  ]
example :
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» 2 = 1 := by
  simp [
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»,
    Proof.FibfibModel.fibfibInt,
    Proof.FibfibModel.fibfibNat
  ]
example :
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» 8 = 24 := by
  simp [
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»,
    Proof.FibfibModel.fibfibInt,
    Proof.FibfibModel.fibfibNat
  ]

def zeroSummary (_ : SortInt) : SortInt := 0

theorem recurrence_accepts_zeroSummary :
    Klean63Fibfib.Lemmas.targetStatement
      Proof.«_>=Int_» Proof.«_+Int_» zeroSummary := by
  intro I h
  rfl

def falseGe (_ _ : SortInt) : SortBool := false
def identitySummary (n : SortInt) : SortInt := n

theorem recurrence_accepts_false_guard :
    Klean63Fibfib.Lemmas.targetStatement
      falseGe Proof.«_+Int_» identitySummary := by
  intro I h
  contradiction

example : zeroSummary 2 ≠
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» 2 := by
  simp [
    zeroSummary,
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»,
    Proof.FibfibModel.fibfibInt,
    Proof.FibfibModel.fibfibNat
  ]
example : falseGe 0 0 ≠ Proof.«_>=Int_» 0 0 := by decide
example : identitySummary 2 ≠
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» 2 := by
  simp [
    identitySummary,
    Proof.«fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int»,
    Proof.FibfibModel.fibfibInt,
    Proof.FibfibModel.fibfibNat
  ]

end BridgeAudit
