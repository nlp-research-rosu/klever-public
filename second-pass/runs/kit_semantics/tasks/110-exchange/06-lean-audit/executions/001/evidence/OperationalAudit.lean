import Proof

open ProofModel

#eval pyMod (-3) 2
#eval pyMod (-4) 2
#eval numberEven (SortVal.inj_SortInt (-3))
#eval numberEven (SortVal.inj_SortInt (-4))
#eval numberEven (SortVal.inj_SortBool false)
#eval numberEven (SortVal.inj_SortBool true)
#eval floatModTwo (-3.0)
#eval floatModTwo (-4.0)
#eval numberEven (SortVal.inj_SortFloat (-3.0))
#eval numberEven (SortVal.inj_SortFloat (-4.0))
#eval isNumberVal SortVal.«noneV_MPY-CORE_Val»
#eval projectInt?
  (SortK.kseq
    ((@inj SortVal SortKItem) (SortVal.inj_SortInt 7))
    SortK.dotk)
#eval projectInt?
  (SortK.kseq
    ((@inj SortVal SortKItem) (SortVal.inj_SortBool true))
    SortK.dotk)

example :
    applyBin? "%" (SortVal.inj_SortInt (-3)) (SortVal.inj_SortInt 2) =
      some (SortVal.inj_SortInt 1) := by
  rfl

example :
    applyBin? "%" (SortVal.inj_SortBool true) (SortVal.inj_SortInt 2) =
      some (SortVal.inj_SortInt 1) := by
  rfl

example :
    applyBin? "%" (SortVal.inj_SortBool true) (SortVal.inj_SortInt 3) =
      none := by
  rfl

example :
    definedProjectInt (SortVal.inj_SortInt 7) = true ∧
    definedProjectBool (SortVal.inj_SortInt 7) = false ∧
    definedProjectFloat (SortVal.inj_SortInt 7) = false := by
  decide

example :
    projectInt?
        (SortK.kseq
          ((@inj SortVal SortKItem) (SortVal.inj_SortInt 7))
          SortK.dotk) =
      some 7 := by
  rfl

example :
    projectInt?
        (SortK.kseq
          ((@inj SortVal SortKItem) (SortVal.inj_SortBool true))
          SortK.dotk) =
      none := by
  rfl

/- Identity, constant, and hard-coded counterfactual bridges disagree with
   the frozen modulo/equality path on small satisfiable numeric witnesses. -/
example :
    applyCmp "=="
        ((fun _ left _ => left) "%"
          (SortVal.inj_SortInt 2) (SortVal.inj_SortInt 2))
        (SortVal.inj_SortInt 0) ≠
      numberEven (SortVal.inj_SortInt 2) := by
  decide

example :
    (false : SortBool) ≠ numberEven (SortVal.inj_SortInt 2) := by
  decide

example :
    applyCmp "==" (SortVal.inj_SortInt 0) (SortVal.inj_SortInt 0) ≠
      numberEven (SortVal.inj_SortInt 3) := by
  decide

example :
    (false : SortBool) ≠ isNumberVal (SortVal.inj_SortInt 2) := by
  decide
