import Klean115MaxFill.Sorts

instance : Inj SortExpr SortKItem where
  inj := SortKItem.inj_SortExpr
  retr
    | SortKItem.inj_SortExpr x => some x
    | _ => none

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortVals SortKItem where
  inj := SortKItem.inj_SortVals
  retr
    | SortKItem.inj_SortVals x => some x
    | _ => none

instance : Inj SortFunctionsCell SortKItem where
  inj := SortKItem.inj_SortFunctionsCell
  retr
    | SortKItem.inj_SortFunctionsCell x => some x
    | _ => none

instance : Inj SortFunction SortKItem where
  inj := SortKItem.inj_SortFunction
  retr
    | SortKItem.inj_SortFunction x => some x
    | _ => none

instance : Inj SortModule SortKItem where
  inj := SortKItem.inj_SortModule
  retr
    | SortKItem.inj_SortModule x => some x
    | _ => none

instance : Inj SortMap SortKItem where
  inj := SortKItem.inj_SortMap
  retr
    | SortKItem.inj_SortMap x => some x
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

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none

instance : Inj SortArgVals SortKItem where
  inj := SortKItem.inj_SortArgVals
  retr
    | SortKItem.inj_SortArgVals x => some x
    | _ => none

instance : Inj SortMaxFillCell SortKItem where
  inj := SortKItem.inj_SortMaxFillCell
  retr
    | SortKItem.inj_SortMaxFillCell x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortRows SortKItem where
  inj := SortKItem.inj_SortRows
  retr
    | SortKItem.inj_SortRows x => some x
    | _ => none

instance : Inj SortParamList SortKItem where
  inj := SortKItem.inj_SortParamList
  retr
    | SortKItem.inj_SortParamList x => some x
    | _ => none

instance : Inj SortParams SortKItem where
  inj := SortKItem.inj_SortParams
  retr
    | SortKItem.inj_SortParams x => some x
    | _ => none

instance : Inj SortArgsCell SortKItem where
  inj := SortKItem.inj_SortArgsCell
  retr
    | SortKItem.inj_SortArgsCell x => some x
    | _ => none

instance : Inj SortExprList SortKItem where
  inj := SortKItem.inj_SortExprList
  retr
    | SortKItem.inj_SortExprList x => some x
    | _ => none

instance : Inj SortInts SortKItem where
  inj := SortKItem.inj_SortInts
  retr
    | SortKItem.inj_SortInts x => some x
    | _ => none

instance : Inj SortCmpOps SortKItem where
  inj := SortKItem.inj_SortCmpOps
  retr
    | SortKItem.inj_SortCmpOps x => some x
    | _ => none

instance : Inj SortStmts SortKItem where
  inj := SortKItem.inj_SortStmts
  retr
    | SortKItem.inj_SortStmts x => some x
    | _ => none

instance : Inj SortVal SortKItem where
  inj
    | SortVal.inj_SortRow x => SortKItem.inj_SortRow x
    | x => SortKItem.inj_SortVal x
  retr
    | SortKItem.inj_SortRow x => some (SortVal.inj_SortRow x)
    | SortKItem.inj_SortVal x => some x
    | _ => none

instance : Inj SortEnvCell SortKItem where
  inj := SortKItem.inj_SortEnvCell
  retr
    | SortKItem.inj_SortEnvCell x => some x
    | _ => none

instance : Inj SortCmpOp SortKItem where
  inj := SortKItem.inj_SortCmpOp
  retr
    | SortKItem.inj_SortCmpOp x => some x
    | _ => none

instance : Inj SortRow SortKItem where
  inj := SortKItem.inj_SortRow
  retr
    | SortKItem.inj_SortRow x => some x
    | _ => none

instance : Inj SortGeneratedTopCell SortKItem where
  inj := SortKItem.inj_SortGeneratedTopCell
  retr
    | SortKItem.inj_SortGeneratedTopCell x => some x
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

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
    | _ => none

instance : Inj SortResultCell SortKItem where
  inj := SortKItem.inj_SortResultCell
  retr
    | SortKItem.inj_SortResultCell x => some x
    | _ => none

instance : Inj SortExpr SortIndex where
  inj := SortIndex.inj_SortExpr
  retr
    | SortIndex.inj_SortExpr x => some x

instance : Inj SortRow SortVal where
  inj := SortVal.inj_SortRow
  retr
    | SortVal.inj_SortRow x => some x
    | _ => none