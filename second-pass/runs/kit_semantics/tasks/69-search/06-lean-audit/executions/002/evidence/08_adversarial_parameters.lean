import Proof

/- Boolean hook: complete truth table, excluding constant/identity versions. -/
#guard Proof._andBool_ true true
#guard !(Proof._andBool_ true false)
#guard !(Proof._andBool_ false true)
#guard !(Proof._andBool_ false false)

/- Integer hooks: negative, equal, and unequal witnesses. -/
#guard Proof.«_+Int_» (-5) 12 == 7
#guard Proof.«_+Int_» (-5) 12 != -5
#guard Proof.«_==Int_» (-3) (-3)
#guard !(Proof.«_==Int_» (-3) 4)
#guard Proof.«_>=Int_» 4 4
#guard !(Proof.«_>=Int_» (-2) 5)
#guard Proof.«_>Int_» 9 (-7)
#guard !(Proof.«_>Int_» 9 9)

/- The proof-local refinement and total projection agree on the Int injection
   and reject other Val constructors. -/
#guard Proof.«isIntVal(_)_VERIFICATION_Bool_Val» (SortVal.inj_SortInt (-23))
#guard !(Proof.«isIntVal(_)_VERIFICATION_Bool_Val» (SortVal.inj_SortBool true))
#guard Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val» (SortVal.inj_SortInt 8)
#guard !(Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val» SortVal.«noneV_MPY-CORE_Val»)
#guard Proof.projectIntTotal (SortVal.inj_SortInt (-23)) == -23

/- K sort projection: exact singleton Int K sequences succeed; Bool and an
   additional continuation do not masquerade as an Int projection. -/
#guard
  Proof.«project:Int?»
      (SortK.kseq (SortKItem.inj_SortInt (-11)) SortK.dotk) == some (-11)
#guard
  (Proof.«project:Int?»
      (SortK.kseq (SortKItem.inj_SortBool true) SortK.dotk)).isNone
#guard
  (Proof.«project:Int?»
      (SortK.kseq (SortKItem.inj_SortInt 3)
        (SortK.kseq (SortKItem.inj_SortInt 4) SortK.dotk))).isNone

/- Dynamic dispatch on the complete guarded domains of the four frozen rules.
   These witnesses reject constant, identity, wrong-operator, and hard-coded
   implementations. -/
#guard
  match Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+"
      (SortVal.inj_SortInt 14) (SortVal.inj_SortInt (-19)) with
  | SortVal.inj_SortInt (-5) => true
  | _ => false
#guard
  Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "=="
    (SortVal.inj_SortInt 6) (SortVal.inj_SortInt 6)
#guard
  !(Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "=="
    (SortVal.inj_SortInt 6) (SortVal.inj_SortInt 7))
#guard
  Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">="
    (SortVal.inj_SortInt (-4)) (SortVal.inj_SortInt (-4))
#guard
  !(Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">="
    (SortVal.inj_SortInt (-5)) (SortVal.inj_SortInt 2))
#guard
  Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">"
    (SortVal.inj_SortInt 3) (SortVal.inj_SortInt (-8))
#guard
  !(Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">"
    (SortVal.inj_SortInt 3) (SortVal.inj_SortInt 3))

#check (Proof.final :
  Klean69Search.Lemmas.targetStatement Proof._andBool_ Proof.«_>Int_»
    Proof.«_>=Int_» Proof.«_==Int_» Proof.«_+Int_»
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val»
    Proof.«isIntVal(_)_VERIFICATION_Bool_Val» Proof.projectIntTotal
    Proof.«project:Int?»)
