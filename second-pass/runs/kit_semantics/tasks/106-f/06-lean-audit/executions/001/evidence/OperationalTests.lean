import Proof

namespace OperationalTests

open Proof

abbrev empty : SortValSeq :=
  SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

def consInt (head : Int) (tail : SortValSeq) : SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
    (SortVal.inj_SortInt head) tail

def intValues : SortValSeq → Option (List Int)
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some []
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortInt head) tail =>
      (head :: ·) <$> intValues tail
  | _ => none

abbrev factRun :=
  «factRun(_,_,_)_VERIFICATION_Int_Int_Int_Int»
abbrev pyMod :=
  «pyMod(_,_)_MPY-INT_Int_Int_Int»
abbrev resultRun :=
  «resultRun(_,_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Int_Int_Int»
abbrev totalRun :=
  «totalRun(_,_,_)_VERIFICATION_Int_Int_Int_Int»
abbrev concat :=
  «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»

-- Arithmetic, comparisons, and boolean conjunction distinguish both branches.
example : Proof._andBool_ true false = false := by native_decide
example : Proof.«_<=Int_» (-3) 2 = true := by native_decide
example : Proof.«_<=Int_» 3 2 = false := by native_decide
example : Proof.«_==Int_» (-7) (-7) = true := by native_decide
example : Proof.«_=/=Int_» (-7) 7 = true := by native_decide
example : Proof.«_+Int_» (-7) 4 = -3 := by native_decide
example : Proof.«_*Int_» (-7) 4 = -28 := by native_decide

-- K's Python-style modulo formula on every divisor used by the frozen program.
example : pyMod (-3) 2 = 1 := by native_decide
example : pyMod (-4) 2 = 0 := by native_decide
example : pyMod 3 2 = 1 := by native_decide

-- Summary functions cover entry, multi-step, and already-terminated states.
example : factRun 1 5 1 = 120 := by native_decide
example : factRun 3 2 7 = 7 := by native_decide
example : factRun (-2) 1 1 = 0 := by native_decide
example : totalRun 1 5 0 = 15 := by native_decide
example : totalRun 3 2 7 = 7 := by native_decide
example : totalRun (-2) 1 10 = 8 := by native_decide

example :
    intValues (concat (consInt 1 empty) (consInt 2 empty)) =
      some [1, 2] := by native_decide

example :
    intValues (resultRun empty 1 5 1 0) =
      some [1, 2, 6, 24, 15] := by native_decide
example :
    intValues (resultRun empty 1 5 1 100) =
      some [101, 2, 106, 24, 115] := by native_decide
example :
    intValues (resultRun empty (-2) 2 1 0) =
      some [-2, -3, 0, -2, 0] := by native_decide
example :
    intValues (resultRun (consInt 9 empty) 3 2 7 8) =
      some [9] := by native_decide

-- Explicitly separate the submitted bridge from convenient counterfactuals.
def constantFact (_I _N _F : Int) : Int := 0
def constantTotal (_I _N _T : Int) : Int := 0
def constantModulo (_value _modulus : Int) : Int := 0
def identityConcat (left _right : SortValSeq) : SortValSeq := left
def constantResult
    (_VS : SortValSeq) (_I _N _F _T : Int) : SortValSeq := empty

example : constantFact 1 5 1 ≠ factRun 1 5 1 := by native_decide
example : constantTotal 1 5 0 ≠ totalRun 1 5 0 := by native_decide
example : constantModulo (-3) 2 ≠ pyMod (-3) 2 := by native_decide
example :
    intValues (identityConcat (consInt 1 empty) (consInt 2 empty)) ≠
      intValues (concat (consInt 1 empty) (consInt 2 empty)) := by
  native_decide
example :
    intValues (constantResult empty 1 5 1 0) ≠
      intValues (resultRun empty 1 5 1 0) := by native_decide

#eval pyMod (-3) 2
#eval factRun 1 5 1
#eval totalRun 1 5 0
#eval intValues (resultRun empty 1 5 1 0)
#eval intValues (resultRun empty 1 5 1 100)
#eval intValues (resultRun empty (-2) 2 1 0)

end OperationalTests
