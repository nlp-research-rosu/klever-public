import Klean132IsNested.Sorts

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
    | _ => none

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortCmpOps SortKItem where
  inj := SortKItem.inj_SortCmpOps
  retr
    | SortKItem.inj_SortCmpOps x => some x
    | _ => none

instance : Inj SortResultCell SortKItem where
  inj := SortKItem.inj_SortResultCell
  retr
    | SortKItem.inj_SortResultCell x => some x
    | _ => none

instance : Inj SortGeneratedTopCell SortKItem where
  inj := SortKItem.inj_SortGeneratedTopCell
  retr
    | SortKItem.inj_SortGeneratedTopCell x => some x
    | _ => none

instance : Inj SortPyCell SortKItem where
  inj := SortKItem.inj_SortPyCell
  retr
    | SortKItem.inj_SortPyCell x => some x
    | _ => none

instance : Inj SortCmpOp SortKItem where
  inj := SortKItem.inj_SortCmpOp
  retr
    | SortKItem.inj_SortCmpOp x => some x
    | _ => none

instance : Inj SortStmt SortKItem where
  inj := SortKItem.inj_SortStmt
  retr
    | SortKItem.inj_SortStmt x => some x
    | _ => none

instance : Inj SortResult SortKItem where
  inj := SortKItem.inj_SortResult
  retr
    | SortKItem.inj_SortResult x => some x
    | _ => none

instance : Inj SortStrings SortKItem where
  inj := SortKItem.inj_SortStrings
  retr
    | SortKItem.inj_SortStrings x => some x
    | _ => none

instance : Inj SortStmts SortKItem where
  inj := SortKItem.inj_SortStmts
  retr
    | SortKItem.inj_SortStmts x => some x
    | _ => none

instance : Inj SortParams SortKItem where
  inj := SortKItem.inj_SortParams
  retr
    | SortKItem.inj_SortParams x => some x
    | _ => none

instance : Inj SortBracket SortKItem where
  inj := SortKItem.inj_SortBracket
  retr
    | SortKItem.inj_SortBracket x => some x
    | _ => none

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none

instance : Inj SortBString SortKItem where
  inj := SortKItem.inj_SortBString
  retr
    | SortKItem.inj_SortBString x => some x
    | _ => none

instance : Inj SortEnvCell SortKItem where
  inj := SortKItem.inj_SortEnvCell
  retr
    | SortKItem.inj_SortEnvCell x => some x
    | _ => none

instance : Inj SortMap SortKItem where
  inj := SortKItem.inj_SortMap
  retr
    | SortKItem.inj_SortMap x => some x
    | _ => none

instance : Inj SortInt SortKItem where
  inj := SortKItem.inj_SortInt
  retr
    | SortKItem.inj_SortInt x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortFunctionsCell SortKItem where
  inj := SortKItem.inj_SortFunctionsCell
  retr
    | SortKItem.inj_SortFunctionsCell x => some x
    | _ => none

instance : Inj SortExpr SortKItem where
  inj := SortKItem.inj_SortExpr
  retr
    | SortKItem.inj_SortExpr x => some x
    | _ => none