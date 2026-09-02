import Klean52BelowThreshold.Sorts

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortLCell SortKItem where
  inj := SortKItem.inj_SortLCell
  retr
    | SortKItem.inj_SortLCell x => some x
    | _ => none

instance : Inj SortCmpOp SortKItem where
  inj := SortKItem.inj_SortCmpOp
  retr
    | SortKItem.inj_SortCmpOp x => some x
    | _ => none

instance : Inj SortSlot SortKItem where
  inj := SortKItem.inj_SortSlot
  retr
    | SortKItem.inj_SortSlot x => some x
    | _ => none

instance : Inj SortValue SortKItem where
  inj := SortKItem.inj_SortValue
  retr
    | SortKItem.inj_SortValue x => some x
    | _ => none

instance : Inj SortParamItems SortKItem where
  inj := SortKItem.inj_SortParamItems
  retr
    | SortKItem.inj_SortParamItems x => some x
    | _ => none

instance : Inj SortBtCell SortKItem where
  inj := SortKItem.inj_SortBtCell
  retr
    | SortKItem.inj_SortBtCell x => some x
    | _ => none

instance : Inj SortThresholdCell SortKItem where
  inj := SortKItem.inj_SortThresholdCell
  retr
    | SortKItem.inj_SortThresholdCell x => some x
    | _ => none

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
    | _ => none

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none

instance : Inj SortGeneratedTopCell SortKItem where
  inj := SortKItem.inj_SortGeneratedTopCell
  retr
    | SortKItem.inj_SortGeneratedTopCell x => some x
    | _ => none

instance : Inj SortXCell SortKItem where
  inj := SortKItem.inj_SortXCell
  retr
    | SortKItem.inj_SortXCell x => some x
    | _ => none

instance : Inj SortPgm SortKItem where
  inj := SortKItem.inj_SortPgm
  retr
    | SortKItem.inj_SortPgm x => some x
    | _ => none

instance : Inj SortIntSeq SortKItem where
  inj := SortKItem.inj_SortIntSeq
  retr
    | SortKItem.inj_SortIntSeq x => some x
    | _ => none

instance : Inj SortResultCell SortKItem where
  inj := SortKItem.inj_SortResultCell
  retr
    | SortKItem.inj_SortResultCell x => some x
    | _ => none

instance : Inj SortInputCell SortKItem where
  inj := SortKItem.inj_SortInputCell
  retr
    | SortKItem.inj_SortInputCell x => some x
    | _ => none

instance : Inj SortTCell SortKItem where
  inj := SortKItem.inj_SortTCell
  retr
    | SortKItem.inj_SortTCell x => some x
    | _ => none

instance : Inj SortProgramCell SortKItem where
  inj := SortKItem.inj_SortProgramCell
  retr
    | SortKItem.inj_SortProgramCell x => some x
    | _ => none

instance : Inj SortStmt SortKItem where
  inj := SortKItem.inj_SortStmt
  retr
    | SortKItem.inj_SortStmt x => some x
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

instance : Inj SortStmts SortKItem where
  inj := SortKItem.inj_SortStmts
  retr
    | SortKItem.inj_SortStmts x => some x
    | _ => none

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortParams SortKItem where
  inj := SortKItem.inj_SortParams
  retr
    | SortKItem.inj_SortParams x => some x
    | _ => none

instance : Inj SortResult SortKItem where
  inj := SortKItem.inj_SortResult
  retr
    | SortKItem.inj_SortResult x => some x
    | _ => none