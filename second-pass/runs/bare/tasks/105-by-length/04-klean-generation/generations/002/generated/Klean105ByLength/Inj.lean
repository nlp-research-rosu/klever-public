import Klean105ByLength.Sorts

instance : Inj SortValue SortKItem where
  inj
    | SortValue.inj_SortInt x => SortKItem.inj_SortInt x
    | SortValue.inj_SortPyList x => SortKItem.inj_SortPyList x
    | SortValue.inj_SortString x => SortKItem.inj_SortString x
  retr
    | SortKItem.inj_SortInt x => some (SortValue.inj_SortInt x)
    | SortKItem.inj_SortPyList x => some (SortValue.inj_SortPyList x)
    | SortKItem.inj_SortString x => some (SortValue.inj_SortString x)
    | SortKItem.inj_SortValue x => some x
    | _ => none

instance : Inj SortProgram SortKItem where
  inj := SortKItem.inj_SortProgram
  retr
    | SortKItem.inj_SortProgram x => some x
    | _ => none

instance : Inj SortProgramCell SortKItem where
  inj := SortKItem.inj_SortProgramCell
  retr
    | SortKItem.inj_SortProgramCell x => some x
    | _ => none

instance : Inj SortMpyCell SortKItem where
  inj := SortKItem.inj_SortMpyCell
  retr
    | SortKItem.inj_SortMpyCell x => some x
    | _ => none

instance : Inj SortResultCell SortKItem where
  inj := SortKItem.inj_SortResultCell
  retr
    | SortKItem.inj_SortResultCell x => some x
    | _ => none

instance : Inj SortParams SortKItem where
  inj := SortKItem.inj_SortParams
  retr
    | SortKItem.inj_SortParams x => some x
    | _ => none

instance : Inj SortExpr SortKItem where
  inj := SortKItem.inj_SortExpr
  retr
    | SortKItem.inj_SortExpr x => some x
    | _ => none

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
    | _ => none

instance : Inj SortPyVals SortKItem where
  inj := SortKItem.inj_SortPyVals
  retr
    | SortKItem.inj_SortPyVals x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none

instance : Inj SortStmt SortKItem where
  inj := SortKItem.inj_SortStmt
  retr
    | SortKItem.inj_SortStmt x => some x
    | _ => none

instance : Inj SortInt SortKItem where
  inj := SortKItem.inj_SortInt
  retr
    | SortKItem.inj_SortInt x => some x
    | _ => none

instance : Inj SortPyList SortKItem where
  inj := SortKItem.inj_SortPyList
  retr
    | SortKItem.inj_SortPyList x => some x
    | _ => none

instance : Inj SortGeneratedTopCell SortKItem where
  inj := SortKItem.inj_SortGeneratedTopCell
  retr
    | SortKItem.inj_SortGeneratedTopCell x => some x
    | _ => none

instance : Inj SortInputCell SortKItem where
  inj := SortKItem.inj_SortInputCell
  retr
    | SortKItem.inj_SortInputCell x => some x
    | _ => none

instance : Inj SortInt SortValue where
  inj := SortValue.inj_SortInt
  retr
    | SortValue.inj_SortInt x => some x
    | _ => none

instance : Inj SortPyList SortValue where
  inj := SortValue.inj_SortPyList
  retr
    | SortValue.inj_SortPyList x => some x
    | _ => none

instance : Inj SortString SortValue where
  inj := SortValue.inj_SortString
  retr
    | SortValue.inj_SortString x => some x
    | _ => none