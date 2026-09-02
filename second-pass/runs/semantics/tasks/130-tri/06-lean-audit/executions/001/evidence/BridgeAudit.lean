import Proof

namespace BridgeAudit

#eval Proof.«_-Int_» (-7) 3
#eval Proof.«_-Int_» 7 (-3)
#eval [Proof._andBool_ false false, Proof._andBool_ false true,
  Proof._andBool_ true false, Proof._andBool_ true true]
#eval [Proof.«_>=Int_» (-2) (-3), Proof.«_>=Int_» (-3) (-2),
  Proof.«_>=Int_» 4 4]
#eval [Proof.«_==Int_» (-2) (-2), Proof.«_==Int_» (-2) 2]
#eval [Proof.«_%Int_» 8 3, Proof.«_%Int_» 8 (-3),
  Proof.«_%Int_» (-8) 3, Proof.«_%Int_» (-8) (-3)]
#eval [Proof.«_/Int_» 8 3, Proof.«_/Int_» 8 (-3),
  Proof.«_/Int_» (-8) 3, Proof.«_/Int_» (-8) (-3)]
#eval [Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int» (-3) 2,
  Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int» 3 (-2)]
#eval (List.range 13).map (fun n => Proof.triAt (Int.ofNat n))

example : Proof.«_+Int_» (-7) 3 = -4 := by decide
example : Proof.«_-Int_» (-7) 3 = -10 := by decide
example : Proof.«_%Int_» (-8) 3 = -2 := by decide
example : Proof.«_/Int_» (-8) 3 = -2 := by decide
example : Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int» (-3) 2 = 1 := by decide

def falseAnd (_a _b : SortBool) : SortBool := false

theorem target_is_vacuous_with_false_and :
    Klean130Tri.Lemmas.targetStatement
      Proof.«_-Int_» falseAnd Proof.«_>=Int_» Proof.«_==Int_»
      Proof.«_%Int_» Proof.«_+Int_» Proof.«_/Int_»
      Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int» Proof.triAt := by
  unfold Klean130Tri.Lemmas.targetStatement
  constructor <;> intro I h <;> simp [falseAnd] at h

def zeroTri (_i : SortInt) : SortInt := 0
def identityTri (i : SortInt) : SortInt := i

theorem zeroTri_rejected
    (hTarget :
      Klean130Tri.Lemmas.targetStatement
        Proof.«_-Int_» Proof._andBool_ Proof.«_>=Int_» Proof.«_==Int_»
        Proof.«_%Int_» Proof.«_+Int_» Proof.«_/Int_»
        Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int» zeroTri) :
    False := by
  have h := hTarget.1 2 (by decide)
  simp [Proof.«_+Int_», Proof.«_/Int_», zeroTri] at h

theorem identityTri_rejected
    (hTarget :
      Klean130Tri.Lemmas.targetStatement
        Proof.«_-Int_» Proof._andBool_ Proof.«_>=Int_» Proof.«_==Int_»
        Proof.«_%Int_» Proof.«_+Int_» Proof.«_/Int_»
        Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int» identityTri) :
    False := by
  have h := hTarget.2 3 (by decide)
  simp [Proof.«_-Int_», Proof.«_%Int_», Proof.«_+Int_», Proof.«_/Int_»,
    identityTri] at h

end BridgeAudit
