import Proof

#guard Operational.frozenPyMod (-3) 2 == 1
#guard Operational.frozenFloorDiv (-3) 2 == -2

#guard
  let empty := SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  let ab :=
    SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 97
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 empty)
  let abc :=
    SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 97
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 99 empty))
  Operational.frozenStringCmp "in" ab abc == some true

#guard
  match
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      "**" (SortVal.inj_SortInt 2) (SortVal.inj_SortInt 5)
  with
  | SortVal.inj_SortInt 32 => true
  | _ => false

#guard
  match
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      "+" (SortVal.inj_SortBool true) (SortVal.inj_SortInt 4)
  with
  | SortVal.inj_SortInt 5 => true
  | _ => false

#guard
  match
    Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
      "*" (SortVal.inj_SortFloat 2.5) (SortVal.inj_SortInt 4)
  with
  | SortVal.inj_SortFloat result =>
      Operational.frozenFloatEq result 10.0
  | _ => false

#guard
  Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    "<" (SortVal.inj_SortInt 3) (SortVal.inj_SortFloat 3.5)

#guard
  Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    "!=" (SortVal.inj_SortBool true) (SortVal.inj_SortBool false)

#guard
  let left :=
    SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq»
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          (SortVal.inj_SortInt 7)
          SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))
  let right :=
    SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq»
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          (SortVal.inj_SortInt 7)
          SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))
  Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "==" left right

#guard
  let left :=
    SortVal.«setV(_)_MPY-SET_Val_IntSeq»
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 1
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 2
          SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))
  let right :=
    SortVal.«setV(_)_MPY-SET_Val_IntSeq»
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 2
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 1
          SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))
  Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "==" left right

#guard
  let keyOne := SortVal.inj_SortInt 1
  let keyTwo := SortVal.inj_SortInt 2
  let valueTen := SortVal.inj_SortInt 10
  let valueTwenty := SortVal.inj_SortInt 20
  let empty := SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  let leftKeys :=
    SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» keyOne
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» keyTwo empty)
  let leftValues :=
    SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» valueTen
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» valueTwenty empty)
  let rightKeys :=
    SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» keyTwo
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» keyOne empty)
  let rightValues :=
    SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» valueTwenty
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» valueTen empty)
  let left :=
    SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» leftKeys leftValues
  let right :=
    SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» rightKeys rightValues
  Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "==" left right

#guard
  Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    "is not" (SortVal.inj_SortInt 0) SortVal.«noneV_MPY-CORE_Val»
