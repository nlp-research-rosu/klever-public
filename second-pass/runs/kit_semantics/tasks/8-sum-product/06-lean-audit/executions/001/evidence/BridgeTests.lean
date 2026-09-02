import Proof

namespace BridgeAudit

def vint (i : SortInt) : SortVal := SortVal.inj_SortInt i
def vbool (b : SortBool) : SortVal := SortVal.inj_SortBool b
def kOfVal (v : SortVal) : SortK :=
  SortK.kseq ((@inj SortVal SortKItem) v) SortK.dotk

-- Truth table and unbounded integer hooks.
example : Proof._andBool_ false false = false := rfl
example : Proof._andBool_ false true = false := rfl
example : Proof._andBool_ true false = false := rfl
example : Proof._andBool_ true true = true := rfl
example : Proof.«_+Int_» (-7) 5 = -2 := rfl
example : Proof.«_+Int_» 123456789012345678901234567890 10 =
    123456789012345678901234567900 := rfl
example : Proof.«_*Int_» (-7) 5 = -35 := rfl
example : Proof.«_*Int_» 0 (-999999999999999999999) = 0 := rfl

-- Exact relevant applyBin branches and adversarial non-Int guards.
example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+"
      (vint (-7)) (vint 5) = vint (-2) := rfl
example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "*"
      (vint (-7)) (vint 5) = vint (-35) := rfl
example : Proof.isInt (kOfVal (vint (-7))) = true := rfl
example : Proof.isInt (kOfVal (vbool true)) = false := rfl
example :
    Proof.isInt
      (SortK.kseq (SortKItem.inj_SortInt 4)
        (SortK.kseq (SortKItem.inj_SortInt 5) SortK.dotk)) = false := rfl

-- Injection/projection, definedness, and totalized projection.
example : Proof.«project:Int?» (kOfVal (vint (-7))) = some (-7) := rfl
example : Proof.«project:Int?» (kOfVal (vbool true)) = none := rfl
example :
    Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val» (vint 42) = true := rfl
example :
    Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val» (vbool true) = false := rfl
example : Proof.projectIntTotal (vint (-7)) = -7 := rfl
example : Proof.projectIntTotal (vbool true) = 0 := rfl

-- Counterfactual definitions expose the target's possible shortcuts.  These
-- witnesses distinguish each shortcut from the actual operational meaning.
def badAnd (_ _ : SortBool) : SortBool := false
def badPlus (a _ : SortInt) : SortInt := a
def badMul (a b : SortInt) : SortInt := a + b
def badApplyBin (_ : SortString) (_ _ : SortVal) : SortVal := vint 0
def badDefined (_ : SortVal) : SortBool := false
def badIsInt (_ : SortK) : SortBool := false
def badProjectTotal (_ : SortVal) : SortInt := 0
def badProject (_ : SortK) : Option SortInt := none

example : badAnd true true = false := rfl
example : Proof._andBool_ true true = true := rfl
example : badPlus 7 (-3) = 7 := rfl
example : Proof.«_+Int_» 7 (-3) = 4 := rfl
example : badMul 7 (-3) = 4 := rfl
example : Proof.«_*Int_» 7 (-3) = -21 := rfl
example : badApplyBin "+" (vint 2) (vint 3) = vint 0 := rfl
example :
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+"
      (vint 2) (vint 3) = vint 5 := rfl
example : badDefined (vint 9) = false := rfl
example :
    Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val» (vint 9) = true := rfl
example : badIsInt (kOfVal (vint 9)) = false := rfl
example : Proof.isInt (kOfVal (vint 9)) = true := rfl
example : badProjectTotal (vint 9) = 0 := rfl
example : Proof.projectIntTotal (vint 9) = 9 := rfl
example : badProject (kOfVal (vint 9)) = none := rfl
example : Proof.«project:Int?» (kOfVal (vint 9)) = some 9 := rfl

#eval Proof._andBool_ true true
#eval Proof.«_+Int_» (-7) 5
#eval Proof.«_*Int_» (-7) 5
#eval Proof.«project:Int?» (kOfVal (vint (-7)))
#eval Proof.isInt (kOfVal (vbool true))
#eval Proof.projectIntTotal (vint 123456789012345678901234567890)

end BridgeAudit
