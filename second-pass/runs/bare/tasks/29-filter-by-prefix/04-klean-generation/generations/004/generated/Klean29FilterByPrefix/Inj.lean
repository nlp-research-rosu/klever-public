import Klean29FilterByPrefix.Sorts

instance : Inj SortInt SortKItem where
  inj := SortKItem.inj_SortInt
  retr
    | SortKItem.inj_SortInt x => some x
    | _ => none

instance : Inj SortStrings SortKItem where
  inj := SortKItem.inj_SortStrings
  retr
    | SortKItem.inj_SortStrings x => some x
    | _ => none

instance : Inj SortParams SortKItem where
  inj := SortKItem.inj_SortParams
  retr
    | SortKItem.inj_SortParams x => some x
    | _ => none

instance : Inj SortPrefixCell SortKItem where
  inj := SortKItem.inj_SortPrefixCell
  retr
    | SortKItem.inj_SortPrefixCell x => some x
    | _ => none

instance : Inj SortModule SortKItem where
  inj := SortKItem.inj_SortModule
  retr
    | SortKItem.inj_SortModule x => some x
    | _ => none

instance : Inj SortEnvCell SortKItem where
  inj := SortKItem.inj_SortEnvCell
  retr
    | SortKItem.inj_SortEnvCell x => some x
    | _ => none

instance : Inj SortStmt SortKItem where
  inj := SortKItem.inj_SortStmt
  retr
    | SortKItem.inj_SortStmt x => some x
    | _ => none

instance : Inj SortStmts SortKItem where
  inj := SortKItem.inj_SortStmts
  retr
    | SortKItem.inj_SortStmts x => some x
    | _ => none

instance : Inj SortTCell SortKItem where
  inj := SortKItem.inj_SortTCell
  retr
    | SortKItem.inj_SortTCell x => some x
    | _ => none

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortVal SortKItem where
  inj := SortKItem.inj_SortVal
  retr
    | SortKItem.inj_SortVal x => some x
    | _ => none

instance : Inj SortOutput SortKItem where
  inj
    | SortOutput.inj_SortVal x => SortKItem.inj_SortVal x
    | x => SortKItem.inj_SortOutput x
  retr
    | SortKItem.inj_SortVal x => some (SortOutput.inj_SortVal x)
    | SortKItem.inj_SortOutput x => some x
    | _ => none

instance : Inj SortInputCell SortKItem where
  inj := SortKItem.inj_SortInputCell
  retr
    | SortKItem.inj_SortInputCell x => some x
    | _ => none

instance : Inj SortStrList SortKItem where
  inj := SortKItem.inj_SortStrList
  retr
    | SortKItem.inj_SortStrList x => some x
    | _ => none

instance : Inj SortFunctionsCell SortKItem where
  inj := SortKItem.inj_SortFunctionsCell
  retr
    | SortKItem.inj_SortFunctionsCell x => some x
    | _ => none

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortGeneratedTopCell SortKItem where
  inj := SortKItem.inj_SortGeneratedTopCell
  retr
    | SortKItem.inj_SortGeneratedTopCell x => some x
    | _ => none

instance : Inj SortOutputCell SortKItem where
  inj := SortKItem.inj_SortOutputCell
  retr
    | SortKItem.inj_SortOutputCell x => some x
    | _ => none

instance : Inj SortMap SortKItem where
  inj := SortKItem.inj_SortMap
  retr
    | SortKItem.inj_SortMap x => some x
    | _ => none

instance : Inj SortExpr SortKItem where
  inj
    | SortExpr.inj_SortVal x => SortKItem.inj_SortVal x
    | x => SortKItem.inj_SortExpr x
  retr
    | SortKItem.inj_SortVal x => some (SortExpr.inj_SortVal x)
    | SortKItem.inj_SortExpr x => some x
    | _ => none

instance : Inj SortVal SortExpr where
  inj := SortExpr.inj_SortVal
  retr
    | SortExpr.inj_SortVal x => some x
    | _ => none

instance : Inj SortVal SortOutput where
  inj := SortOutput.inj_SortVal
  retr
    | SortOutput.inj_SortVal x => some x
    | _ => none