import Proof

open Proof

abbrev scan :=
  Proof.«primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool»

noncomputable abbrev search :=
  Proof.«primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int»

#eval ("false-flag absorption", [
  scan (-7) 2 false,
  scan 0 2 false,
  scan 4 2 false,
  scan 97 2 false,
  scan 221 2 false
])

#eval ("scan from divisor 2", [
  scan (-7) 2 true,
  scan 0 2 true,
  scan 1 2 true,
  scan 2 2 true,
  scan 3 2 true,
  scan 4 2 true,
  scan 5 2 true,
  scan 9 2 true,
  scan 25 2 true,
  scan 49 2 true,
  scan 97 2 true,
  scan 221 2 true
])

#eval ("suffix starts", [
  scan 9 3 true,
  scan 9 4 true,
  scan 25 3 true,
  scan 25 6 true
])

example : search 0 0 7 11 = 7 := by rfl
example : search 1 0 (-100) 2 = 2 := by rfl
example : search 2 1 42 3 = 3 := by rfl

#check search
#check scan
