import Klean151DoubleTheDifference.Sorts

instance : Inj SortExpr SortKItem where
  inj := SortKItem.inj_SortExpr
  retr
    | SortKItem.inj_SortExpr x => some x
    | _ => none

instance : Inj SortResultCell SortKItem where
  inj := SortKItem.inj_SortResultCell
  retr
    | SortKItem.inj_SortResultCell x => some x
    | _ => none

instance : Inj SortStrings SortKItem where
  inj := SortKItem.inj_SortStrings
  retr
    | SortKItem.inj_SortStrings x => some x
    | _ => none

instance : Inj SortFloat SortKItem where
  inj := SortKItem.inj_SortFloat
  retr
    | SortKItem.inj_SortFloat x => some x
    | _ => none

instance : Inj SortCmpOps SortKItem where
  inj := SortKItem.inj_SortCmpOps
  retr
    | SortKItem.inj_SortCmpOps x => some x
    | _ => none

instance : Inj SortResult SortKItem where
  inj
    | SortResult.inj_SortVal x => SortKItem.inj_SortVal x
    | x => SortKItem.inj_SortResult x
  retr
    | SortKItem.inj_SortVal x => some (SortResult.inj_SortVal x)
    | SortKItem.inj_SortResult x => some x
    | _ => none

instance : Inj SortVal SortKItem where
  inj := SortKItem.inj_SortVal
  retr
    | SortKItem.inj_SortVal x => some x
    | _ => none

instance : Inj SortStmt SortKItem where
  inj := SortKItem.inj_SortStmt
  retr
    | SortKItem.inj_SortStmt x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortFunctionSlot SortKItem where
  inj := SortKItem.inj_SortFunctionSlot
  retr
    | SortKItem.inj_SortFunctionSlot x => some x
    | _ => none

instance : Inj SortInt SortKItem where
  inj := SortKItem.inj_SortInt
  retr
    | SortKItem.inj_SortInt x => some x
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

instance : Inj SortVals SortKItem where
  inj := SortKItem.inj_SortVals
  retr
    | SortKItem.inj_SortVals x => some x
    | _ => none

instance : Inj SortStmts SortKItem where
  inj := SortKItem.inj_SortStmts
  retr
    | SortKItem.inj_SortStmts x => some x
    | _ => none

instance : Inj SortValSlot SortKItem where
  inj
    | SortValSlot.inj_SortVal x => SortKItem.inj_SortVal x
    | x => SortKItem.inj_SortValSlot x
  retr
    | SortKItem.inj_SortVal x => some (SortValSlot.inj_SortVal x)
    | SortKItem.inj_SortValSlot x => some x
    | _ => none

instance : Inj SortCmpOp SortKItem where
  inj := SortKItem.inj_SortCmpOp
  retr
    | SortKItem.inj_SortCmpOp x => some x
    | _ => none

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortExprs SortKItem where
  inj := SortKItem.inj_SortExprs
  retr
    | SortKItem.inj_SortExprs x => some x
    | _ => none

instance : Inj SortTotalCell SortKItem where
  inj := SortKItem.inj_SortTotalCell
  retr
    | SortKItem.inj_SortTotalCell x => some x
    | _ => none

instance : Inj SortValueCell SortKItem where
  inj := SortKItem.inj_SortValueCell
  retr
    | SortKItem.inj_SortValueCell x => some x
    | _ => none

instance : Inj SortLstCell SortKItem where
  inj := SortKItem.inj_SortLstCell
  retr
    | SortKItem.inj_SortLstCell x => some x
    | _ => none

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
    | _ => none

instance : Inj SortFunctionCell SortKItem where
  inj := SortKItem.inj_SortFunctionCell
  retr
    | SortKItem.inj_SortFunctionCell x => some x
    | _ => none

instance : Inj SortPyCell SortKItem where
  inj := SortKItem.inj_SortPyCell
  retr
    | SortKItem.inj_SortPyCell x => some x
    | _ => none

instance : Inj SortParams SortKItem where
  inj := SortKItem.inj_SortParams
  retr
    | SortKItem.inj_SortParams x => some x
    | _ => none

instance : Inj SortVal SortResult where
  inj := SortResult.inj_SortVal
  retr
    | SortResult.inj_SortVal x => some x
    | _ => none

instance : Inj SortVal SortValSlot where
  inj := SortValSlot.inj_SortVal
  retr
    | SortValSlot.inj_SortVal x => some x
    | _ => none