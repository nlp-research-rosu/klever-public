import Proof

#eval match
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      "/" (SortVal.inj_SortInt 1) (SortVal.inj_SortInt 2)
  with
  | SortVal.inj_SortInt 999 => true
  | _ => false
