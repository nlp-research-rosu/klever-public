import Klean114Minsubarraysum.Sorts

instance : Inj SortList SortKItem where
  inj := SortKItem.inj_SortList
  retr
    | SortKItem.inj_SortList x => some x
    | _ => none

instance : Inj SortCmpOps SortKItem where
  inj := SortKItem.inj_SortCmpOps
  retr
    | SortKItem.inj_SortCmpOps x => some x
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

instance : Inj SortEnvCell SortKItem where
  inj := SortKItem.inj_SortEnvCell
  retr
    | SortKItem.inj_SortEnvCell x => some x
    | _ => none

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
    | _ => none

instance : Inj SortExpr SortKItem where
  inj := SortKItem.inj_SortExpr
  retr
    | SortKItem.inj_SortExpr x => some x
    | _ => none

instance : Inj SortDepth SortKItem where
  inj := SortKItem.inj_SortDepth
  retr
    | SortKItem.inj_SortDepth x => some x
    | _ => none

instance : Inj SortValue SortKItem where
  inj := SortKItem.inj_SortValue
  retr
    | SortKItem.inj_SortValue x => some x
    | _ => none

instance : Inj SortStmts SortKItem where
  inj := SortKItem.inj_SortStmts
  retr
    | SortKItem.inj_SortStmts x => some x
    | _ => none

instance : Inj SortIntList SortKItem where
  inj := SortKItem.inj_SortIntList
  retr
    | SortKItem.inj_SortIntList x => some x
    | _ => none

instance : Inj SortGeneratedTopCell SortKItem where
  inj := SortKItem.inj_SortGeneratedTopCell
  retr
    | SortKItem.inj_SortGeneratedTopCell x => some x
    | _ => none

instance : Inj SortArgsCell SortKItem where
  inj := SortKItem.inj_SortArgsCell
  retr
    | SortKItem.inj_SortArgsCell x => some x
    | _ => none

instance : Inj SortCallDepthCell SortKItem where
  inj := SortKItem.inj_SortCallDepthCell
  retr
    | SortKItem.inj_SortCallDepthCell x => some x
    | _ => none

instance : Inj SortPyCell SortKItem where
  inj := SortKItem.inj_SortPyCell
  retr
    | SortKItem.inj_SortPyCell x => some x
    | _ => none

instance : Inj SortEntryCell SortKItem where
  inj := SortKItem.inj_SortEntryCell
  retr
    | SortKItem.inj_SortEntryCell x => some x
    | _ => none

instance : Inj SortStrings SortKItem where
  inj := SortKItem.inj_SortStrings
  retr
    | SortKItem.inj_SortStrings x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortExprs SortKItem where
  inj := SortKItem.inj_SortExprs
  retr
    | SortKItem.inj_SortExprs x => some x
    | _ => none

instance : Inj SortIndex SortKItem where
  inj
    | SortIndex.inj_SortExpr x => SortKItem.inj_SortExpr x
  retr
    | SortKItem.inj_SortExpr x => some (SortIndex.inj_SortExpr x)
    | SortKItem.inj_SortIndex x => some x
    | _ => none

instance : Inj SortValues SortKItem where
  inj := SortKItem.inj_SortValues
  retr
    | SortKItem.inj_SortValues x => some x
    | _ => none

instance : Inj SortInt SortKItem where
  inj := SortKItem.inj_SortInt
  retr
    | SortKItem.inj_SortInt x => some x
    | _ => none

instance : Inj SortCallStackCell SortKItem where
  inj := SortKItem.inj_SortCallStackCell
  retr
    | SortKItem.inj_SortCallStackCell x => some x
    | _ => none

instance : Inj SortStmt SortKItem where
  inj := SortKItem.inj_SortStmt
  retr
    | SortKItem.inj_SortStmt x => some x
    | _ => none

instance : Inj SortFunctionsCell SortKItem where
  inj := SortKItem.inj_SortFunctionsCell
  retr
    | SortKItem.inj_SortFunctionsCell x => some x
    | _ => none

instance : Inj SortParams SortKItem where
  inj := SortKItem.inj_SortParams
  retr
    | SortKItem.inj_SortParams x => some x
    | _ => none

instance : Inj SortMap SortKItem where
  inj := SortKItem.inj_SortMap
  retr
    | SortKItem.inj_SortMap x => some x
    | _ => none

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortExpr SortIndex where
  inj := SortIndex.inj_SortExpr
  retr
    | SortIndex.inj_SortExpr x => some x