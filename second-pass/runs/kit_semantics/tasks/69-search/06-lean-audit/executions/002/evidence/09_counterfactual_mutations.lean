import Proof

namespace Counterfactual

def falseAnd (_ _ : SortBool) : SortBool := false
def falseGt (_ _ : SortInt) : SortBool := false
def falseGe (_ _ : SortInt) : SortBool := false
def falseEq (_ _ : SortInt) : SortBool := false
def leftAdd (left _ : SortInt) : SortInt := left
def leftBin (_ : SortString) (left _ : SortVal) : SortVal := left
def falseCmp (_ : SortString) (_ _ : SortVal) : SortBool := false
def falseDefined (_ : SortVal) : SortBool := false
def falseIsInt (_ : SortVal) : SortBool := false
def zeroProject (_ : SortVal) : SortInt := 0
def noneCast (_ : SortK) : Option SortInt := none

/- Each common convenient mutation is separated from the candidate by a
   satisfiable witness inside the exact domain of its bound source rule(s). -/
#guard Proof._andBool_ true true != falseAnd true true
#guard Proof.«_>Int_» 1 0 != falseGt 1 0
#guard Proof.«_>=Int_» 4 4 != falseGe 4 4
#guard Proof.«_==Int_» (-2) (-2) != falseEq (-2) (-2)
#guard Proof.«_+Int_» 2 3 != leftAdd 2 3

#guard
  match
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+"
      (SortVal.inj_SortInt 2) (SortVal.inj_SortInt 3),
    leftBin "+" (SortVal.inj_SortInt 2) (SortVal.inj_SortInt 3)
  with
  | SortVal.inj_SortInt 5, SortVal.inj_SortInt 2 => true
  | _, _ => false

#guard
  Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "=="
      (SortVal.inj_SortInt 8) (SortVal.inj_SortInt 8)
    != falseCmp "==" (SortVal.inj_SortInt 8) (SortVal.inj_SortInt 8)

#guard
  Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val»
      (SortVal.inj_SortInt 9)
    != falseDefined (SortVal.inj_SortInt 9)
#guard
  Proof.«isIntVal(_)_VERIFICATION_Bool_Val» (SortVal.inj_SortInt 9)
    != falseIsInt (SortVal.inj_SortInt 9)
#guard
  Proof.projectIntTotal (SortVal.inj_SortInt 9)
    != zeroProject (SortVal.inj_SortInt 9)
#guard
  Proof.«project:Int?»
      (SortK.kseq (SortKItem.inj_SortInt 9) SortK.dotk)
    != noneCast (SortK.kseq (SortKItem.inj_SortInt 9) SortK.dotk)

end Counterfactual
