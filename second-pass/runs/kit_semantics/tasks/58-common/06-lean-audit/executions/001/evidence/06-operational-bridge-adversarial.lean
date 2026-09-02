import Proof

namespace BridgeAudit

-- Ground checks for the actual candidate bridges.
#eval [
  Proof._orBool_ false false,
  Proof._orBool_ false true,
  Proof._orBool_ true false,
  Proof._orBool_ true true
]
#eval [Proof.notBool_ false, Proof.notBool_ true]

example : Proof._orBool_ false false = false := rfl
example : Proof._orBool_ false true = true := rfl
example : Proof._orBool_ true false = true := rfl
example : Proof._orBool_ true true = true := rfl

example : Proof.notBool_ false = true := rfl
example : Proof.notBool_ true = false := rfl

example : Proof.«_==K_» SortK.dotk SortK.dotk = true := by
  simp [Proof.«_==K_»]

example :
    Proof.«_==K_»
      SortK.dotk
      (SortK.kseq (SortKItem.inj_SortBool false) SortK.dotk) = false := by
  simp [Proof.«_==K_»]

example :
    Proof.«_==K_»
      (SortK.kseq (SortKItem.inj_SortBool false) SortK.dotk)
      (SortK.kseq (SortKItem.inj_SortBool false) SortK.dotk) = true := by
  simp [Proof.«_==K_»]

example :
    Proof.«_==K_»
      (SortK.kseq (SortKItem.inj_SortBool false) SortK.dotk)
      (SortK.kseq (SortKItem.inj_SortBool true) SortK.dotk) = false := by
  simp [Proof.«_==K_»]

def falseValK : SortK :=
  SortK.kseq
    ((@inj SortVal SortKItem) (SortVal.inj_SortBool false))
    SortK.dotk

def trueValK : SortK :=
  SortK.kseq
    ((@inj SortVal SortKItem) (SortVal.inj_SortBool true))
    SortK.dotk

-- A concrete satisfiable witness for the generated rule guard.
example :
    Proof.notBool_ (Proof.«_==K_» falseValK trueValK) = true := by
  have injected_ne :
      ((@inj SortVal SortKItem) (SortVal.inj_SortBool false)) ≠
      ((@inj SortVal SortKItem) (SortVal.inj_SortBool true)) := by
    change SortKItem.inj_SortBool false ≠ SortKItem.inj_SortBool true
    simp
  simp [Proof.notBool_, Proof.«_==K_», falseValK, trueValK,
    injected_ne]

-- Counterfactual convenience bridges.  These deliberately demonstrate that
-- the generated proposition alone does not enforce operational adequacy.
def rightProjection (_left right : SortBool) : SortBool := right

noncomputable def constantTrueEq
    (_left _right : SortK) : SortBool := true

def constantFalseNot (_value : SortBool) : SortBool := false

theorem rightProjectionStillProves :
    Klean58Common.Lemmas.targetStatement
      rightProjection Proof.«_==K_» Proof.notBool_ := by
  simp [Klean58Common.Lemmas.targetStatement, rightProjection]

theorem constantEqualityStillProves :
    Klean58Common.Lemmas.targetStatement
      Proof._orBool_ constantTrueEq Proof.notBool_ := by
  simp [Klean58Common.Lemmas.targetStatement, constantTrueEq,
    Proof._orBool_, Proof.notBool_]

theorem constantNegationStillProves :
    Klean58Common.Lemmas.targetStatement
      Proof._orBool_ Proof.«_==K_» constantFalseNot := by
  simp [Klean58Common.Lemmas.targetStatement, constantFalseNot]

end BridgeAudit
