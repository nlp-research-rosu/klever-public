import Klean12Longest.Sorts

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortStmt SortKItem where
  inj := SortKItem.inj_SortStmt
  retr
    | SortKItem.inj_SortStmt x => some x
    | _ => none

instance : Inj SortFunctionCell SortKItem where
  inj := SortKItem.inj_SortFunctionCell
  retr
    | SortKItem.inj_SortFunctionCell x => some x
    | _ => none

instance : Inj SortGeneratedTopCell SortKItem where
  inj := SortKItem.inj_SortGeneratedTopCell
  retr
    | SortKItem.inj_SortGeneratedTopCell x => some x
    | _ => none

instance : Inj SortMpyCell SortKItem where
  inj := SortKItem.inj_SortMpyCell
  retr
    | SortKItem.inj_SortMpyCell x => some x
    | _ => none

instance : Inj SortMap SortKItem where
  inj := SortKItem.inj_SortMap
  retr
    | SortKItem.inj_SortMap x => some x
    | _ => none

instance : Inj SortValues SortKItem where
  inj := SortKItem.inj_SortValues
  retr
    | SortKItem.inj_SortValues x => some x
    | _ => none

instance : Inj SortValue SortKItem where
  inj := SortKItem.inj_SortValue
  retr
    | SortKItem.inj_SortValue x => some x
    | _ => none

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
    | _ => none

instance : Inj SortOutCell SortKItem where
  inj := SortKItem.inj_SortOutCell
  retr
    | SortKItem.inj_SortOutCell x => some x
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

instance : Inj SortOutput SortKItem where
  inj
    | SortOutput.inj_SortValue x => SortKItem.inj_SortValue x
    | x => SortKItem.inj_SortOutput x
  retr
    | SortKItem.inj_SortValue x => some (SortOutput.inj_SortValue x)
    | SortKItem.inj_SortOutput x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortArgsCell SortKItem where
  inj := SortKItem.inj_SortArgsCell
  retr
    | SortKItem.inj_SortArgsCell x => some x
    | _ => none

instance : Inj SortFunction SortKItem where
  inj := SortKItem.inj_SortFunction
  retr
    | SortKItem.inj_SortFunction x => some x
    | _ => none

instance : Inj SortCmpOps SortKItem where
  inj := SortKItem.inj_SortCmpOps
  retr
    | SortKItem.inj_SortCmpOps x => some x
    | _ => none

instance : Inj SortStrings SortKItem where
  inj := SortKItem.inj_SortStrings
  retr
    | SortKItem.inj_SortStrings x => some x
    | _ => none

instance : Inj SortInt SortKItem where
  inj := SortKItem.inj_SortInt
  retr
    | SortKItem.inj_SortInt x => some x
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

instance : Inj SortCmpOp SortKItem where
  inj := SortKItem.inj_SortCmpOp
  retr
    | SortKItem.inj_SortCmpOp x => some x
    | _ => none

instance : Inj SortExprs SortKItem where
  inj := SortKItem.inj_SortExprs
  retr
    | SortKItem.inj_SortExprs x => some x
    | _ => none

instance : Inj SortStmts SortKItem where
  inj := SortKItem.inj_SortStmts
  retr
    | SortKItem.inj_SortStmts x => some x
    | _ => none

instance : Inj SortValue SortOutput where
  inj := SortOutput.inj_SortValue
  retr
    | SortOutput.inj_SortValue x => some x
    | _ => none