import Klean26RemoveDuplicates.Sorts

instance : Inj SortPyCell SortKItem where
  inj := SortKItem.inj_SortPyCell
  retr
    | SortKItem.inj_SortPyCell x => some x
    | _ => none

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortCmpOps SortKItem where
  inj := SortKItem.inj_SortCmpOps
  retr
    | SortKItem.inj_SortCmpOps x => some x
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

instance : Inj SortCompFor SortKItem where
  inj := SortKItem.inj_SortCompFor
  retr
    | SortKItem.inj_SortCompFor x => some x
    | _ => none

instance : Inj SortStmts SortKItem where
  inj := SortKItem.inj_SortStmts
  retr
    | SortKItem.inj_SortStmts x => some x
    | _ => none

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none

instance : Inj SortEnv SortKItem where
  inj := SortKItem.inj_SortEnv
  retr
    | SortKItem.inj_SortEnv x => some x
    | _ => none

instance : Inj SortFunction SortKItem where
  inj := SortKItem.inj_SortFunction
  retr
    | SortKItem.inj_SortFunction x => some x
    | _ => none

instance : Inj SortCellVars SortKItem where
  inj := SortKItem.inj_SortCellVars
  retr
    | SortKItem.inj_SortCellVars x => some x
    | _ => none

instance : Inj SortInts SortKItem where
  inj := SortKItem.inj_SortInts
  retr
    | SortKItem.inj_SortInts x => some x
    | _ => none

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
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

instance : Inj SortFreeVars SortKItem where
  inj := SortKItem.inj_SortFreeVars
  retr
    | SortKItem.inj_SortFreeVars x => some x
    | _ => none

instance : Inj SortCmpOp SortKItem where
  inj := SortKItem.inj_SortCmpOp
  retr
    | SortKItem.inj_SortCmpOp x => some x
    | _ => none

instance : Inj SortOutputCell SortKItem where
  inj := SortKItem.inj_SortOutputCell
  retr
    | SortKItem.inj_SortOutputCell x => some x
    | _ => none

instance : Inj SortExprs SortKItem where
  inj := SortKItem.inj_SortExprs
  retr
    | SortKItem.inj_SortExprs x => some x
    | _ => none

instance : Inj SortEnvCell SortKItem where
  inj := SortKItem.inj_SortEnvCell
  retr
    | SortKItem.inj_SortEnvCell x => some x
    | _ => none

instance : Inj SortCompFors SortKItem where
  inj := SortKItem.inj_SortCompFors
  retr
    | SortKItem.inj_SortCompFors x => some x
    | _ => none

instance : Inj SortPyVal SortKItem where
  inj := SortKItem.inj_SortPyVal
  retr
    | SortKItem.inj_SortPyVal x => some x
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

instance : Inj SortStrings SortKItem where
  inj := SortKItem.inj_SortStrings
  retr
    | SortKItem.inj_SortStrings x => some x
    | _ => none

instance : Inj SortFunctionCell SortKItem where
  inj := SortKItem.inj_SortFunctionCell
  retr
    | SortKItem.inj_SortFunctionCell x => some x
    | _ => none