import Klean90NextSmallest.Sorts

instance : Inj SortDistinctCell SortKItem where
  inj := SortKItem.inj_SortDistinctCell
  retr
    | SortKItem.inj_SortDistinctCell x => some x
    | _ => none

instance : Inj SortMpyCell SortKItem where
  inj := SortKItem.inj_SortMpyCell
  retr
    | SortKItem.inj_SortMpyCell x => some x
    | _ => none

instance : Inj SortExpr SortKItem where
  inj := SortKItem.inj_SortExpr
  retr
    | SortKItem.inj_SortExpr x => some x
    | _ => none

instance : Inj SortInt SortKItem where
  inj := SortKItem.inj_SortInt
  retr
    | SortKItem.inj_SortInt x => some x
    | _ => none

instance : Inj SortStmt SortKItem where
  inj := SortKItem.inj_SortStmt
  retr
    | SortKItem.inj_SortStmt x => some x
    | _ => none

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
    | _ => none

instance : Inj SortOutcome SortKItem where
  inj
    | SortOutcome.inj_SortBool x => SortKItem.inj_SortBool x
    | SortOutcome.inj_SortInt x => SortKItem.inj_SortInt x
    | SortOutcome.inj_SortPyVal x => SortKItem.inj_SortPyVal x
    | x => SortKItem.inj_SortOutcome x
  retr
    | SortKItem.inj_SortBool x => some (SortOutcome.inj_SortBool x)
    | SortKItem.inj_SortInt x => some (SortOutcome.inj_SortInt x)
    | SortKItem.inj_SortPyVal x => some (SortOutcome.inj_SortPyVal x)
    | SortKItem.inj_SortOutcome x => some x
    | _ => none

instance : Inj SortParams SortKItem where
  inj := SortKItem.inj_SortParams
  retr
    | SortKItem.inj_SortParams x => some x
    | _ => none

instance : Inj SortGeneratedTopCell SortKItem where
  inj := SortKItem.inj_SortGeneratedTopCell
  retr
    | SortKItem.inj_SortGeneratedTopCell x => some x
    | _ => none

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortIntList SortKItem where
  inj := SortKItem.inj_SortIntList
  retr
    | SortKItem.inj_SortIntList x => some x
    | _ => none

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none

instance : Inj SortCmpOp SortKItem where
  inj := SortKItem.inj_SortCmpOp
  retr
    | SortKItem.inj_SortCmpOp x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortInputCell SortKItem where
  inj := SortKItem.inj_SortInputCell
  retr
    | SortKItem.inj_SortInputCell x => some x
    | _ => none

instance : Inj SortPyVal SortKItem where
  inj
    | SortPyVal.inj_SortBool x => SortKItem.inj_SortBool x
    | SortPyVal.inj_SortInt x => SortKItem.inj_SortInt x
    | x => SortKItem.inj_SortPyVal x
  retr
    | SortKItem.inj_SortBool x => some (SortPyVal.inj_SortBool x)
    | SortKItem.inj_SortInt x => some (SortPyVal.inj_SortInt x)
    | SortKItem.inj_SortPyVal x => some x
    | _ => none

instance : Inj SortStmts SortKItem where
  inj := SortKItem.inj_SortStmts
  retr
    | SortKItem.inj_SortStmts x => some x
    | _ => none

instance : Inj SortResultCell SortKItem where
  inj := SortKItem.inj_SortResultCell
  retr
    | SortKItem.inj_SortResultCell x => some x
    | _ => none

instance : Inj SortBool SortPyVal where
  inj := SortPyVal.inj_SortBool
  retr
    | SortPyVal.inj_SortBool x => some x
    | _ => none

instance : Inj SortInt SortPyVal where
  inj := SortPyVal.inj_SortInt
  retr
    | SortPyVal.inj_SortInt x => some x
    | _ => none

instance : Inj SortPyVal SortOutcome where
  inj
    | SortPyVal.inj_SortBool x => SortOutcome.inj_SortBool x
    | SortPyVal.inj_SortInt x => SortOutcome.inj_SortInt x
    | x => SortOutcome.inj_SortPyVal x
  retr
    | SortOutcome.inj_SortBool x => some (SortPyVal.inj_SortBool x)
    | SortOutcome.inj_SortInt x => some (SortPyVal.inj_SortInt x)
    | SortOutcome.inj_SortPyVal x => some x
    | _ => none

instance : Inj SortBool SortOutcome where
  inj := SortOutcome.inj_SortBool
  retr
    | SortOutcome.inj_SortBool x => some x
    | _ => none

instance : Inj SortInt SortOutcome where
  inj := SortOutcome.inj_SortInt
  retr
    | SortOutcome.inj_SortInt x => some x
    | _ => none