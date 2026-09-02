import Klean64VowelsCount.Sorts

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortPyCell SortKItem where
  inj := SortKItem.inj_SortPyCell
  retr
    | SortKItem.inj_SortPyCell x => some x
    | _ => none

instance : Inj SortList SortKItem where
  inj := SortKItem.inj_SortList
  retr
    | SortKItem.inj_SortList x => some x
    | _ => none

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
    | _ => none

instance : Inj SortInt SortKItem where
  inj := SortKItem.inj_SortInt
  retr
    | SortKItem.inj_SortInt x => some x
    | _ => none

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none

instance : Inj SortEnvCell SortKItem where
  inj := SortKItem.inj_SortEnvCell
  retr
    | SortKItem.inj_SortEnvCell x => some x
    | _ => none

instance : Inj SortFunctionsCell SortKItem where
  inj := SortKItem.inj_SortFunctionsCell
  retr
    | SortKItem.inj_SortFunctionsCell x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortPyVal SortKItem where
  inj := SortKItem.inj_SortPyVal
  retr
    | SortKItem.inj_SortPyVal x => some x
    | _ => none

instance : Inj SortGeneratedTopCell SortKItem where
  inj := SortKItem.inj_SortGeneratedTopCell
  retr
    | SortKItem.inj_SortGeneratedTopCell x => some x
    | _ => none

instance : Inj SortMap SortKItem where
  inj := SortKItem.inj_SortMap
  retr
    | SortKItem.inj_SortMap x => some x
    | _ => none

instance : Inj SortStackCell SortKItem where
  inj := SortKItem.inj_SortStackCell
  retr
    | SortKItem.inj_SortStackCell x => some x
    | _ => none