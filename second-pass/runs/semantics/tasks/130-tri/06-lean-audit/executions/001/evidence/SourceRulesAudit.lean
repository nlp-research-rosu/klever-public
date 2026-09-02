import Proof

namespace SourceRulesAudit

example : Proof.triAt 0 = 1 := by decide
example : Proof.triAt 1 = 3 := by decide

theorem even_defining_rule
    (I : SortInt)
    (h :
      Proof._andBool_ (Proof.«_>=Int_» I 2)
        (Proof.«_==Int_»
          (Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int» I 2) 0) = true) :
    Proof.«_+Int_» 1
        (Proof.«_/Int_»
          (Proof.«_-Int_» I
            (Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int» I 2)) 2) =
      Proof.triAt I := by
  simp [Proof._andBool_, Proof.«_>=Int_», Proof.«_==Int_»,
    Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int»] at h
  rw [Proof.triAt, if_pos h.2]
  simp [Proof.«_-Int_», Proof.«_+Int_», Proof.«_/Int_»,
    Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int», h.2]
  exact Int.add_comm _ _

theorem odd_defining_rule
    (I : SortInt)
    (h :
      Proof._andBool_ (Proof.«_>=Int_» I 3)
        (Proof.«_==Int_»
          (Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int» I 2) 1) = true) :
    Proof.«_+Int_»
        (Proof.«_+Int_»
          (Proof.«_+Int_»
            (Proof.triAt (Proof.«_-Int_» I 1))
            (Proof.triAt (Proof.«_-Int_» I 2))) 1)
        (Proof.«_/Int_»
          (Proof.«_-Int_» (Proof.«_+Int_» I 1)
            (Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int»
              (Proof.«_+Int_» I 1) 2)) 2) =
      Proof.triAt I := by
  have hFinal := Proof.final
  unfold Klean130Tri.Lemmas.targetStatement at hFinal
  simpa [Proof.«_-Int_», Proof.«pyMod(_,_)_MPY-INT_Int_Int_Int»] using
    hFinal.2 I h

end SourceRulesAudit
