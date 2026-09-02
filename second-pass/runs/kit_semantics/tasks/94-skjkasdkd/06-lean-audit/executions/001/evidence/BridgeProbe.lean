import Proof

#eval Proof.«_%Int_» (-5) 3
#eval Int.tmod (-5) 3
#eval Int.emod (-5) 3
#eval Proof.«_%Int_» 17 10
#eval Int.tmod 17 10
#eval match
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      "/" (SortVal.inj_SortInt 1) (SortVal.inj_SortInt 2)
  with
  | SortVal.«noneV_MPY-CORE_Val» => true
  | _ => false
