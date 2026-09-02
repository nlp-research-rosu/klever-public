import Klean133SumSquares.Sorts

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
    | _ => none

instance : Inj SortMap SortKItem where
  inj := SortKItem.inj_SortMap
  retr
    | SortKItem.inj_SortMap x => some x
    | _ => none

instance : Inj SortPyStmts SortKItem where
  inj := SortKItem.inj_SortPyStmts
  retr
    | SortKItem.inj_SortPyStmts x => some x
    | _ => none

instance : Inj SortPList SortKItem where
  inj := SortKItem.inj_SortPList
  retr
    | SortKItem.inj_SortPList x => some x
    | _ => none

instance : Inj SortPyExpr SortKItem where
  inj := SortKItem.inj_SortPyExpr
  retr
    | SortKItem.inj_SortPyExpr x => some x
    | _ => none

instance : Inj SortInt SortKItem where
  inj := SortKItem.inj_SortInt
  retr
    | SortKItem.inj_SortInt x => some x
    | _ => none

instance : Inj SortEnvCell SortKItem where
  inj := SortKItem.inj_SortEnvCell
  retr
    | SortKItem.inj_SortEnvCell x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortGeneratedTopCell SortKItem where
  inj := SortKItem.inj_SortGeneratedTopCell
  retr
    | SortKItem.inj_SortGeneratedTopCell x => some x
    | _ => none

instance : Inj SortEnv SortKItem where
  inj := SortKItem.inj_SortEnv
  retr
    | SortKItem.inj_SortEnv x => some x
    | _ => none

instance : Inj SortPosNat SortKItem where
  inj := SortKItem.inj_SortPosNat
  retr
    | SortKItem.inj_SortPosNat x => some x
    | _ => none

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none

instance : Inj SortPythonCell SortKItem where
  inj := SortKItem.inj_SortPythonCell
  retr
    | SortKItem.inj_SortPythonCell x => some x
    | _ => none

instance : Inj SortPValue SortKItem where
  inj
    | SortPValue.inj_SortNumValue x => SortKItem.inj_SortNumValue x
    | x => SortKItem.inj_SortPValue x
  retr
    | SortKItem.inj_SortNumValue x => some (SortPValue.inj_SortNumValue x)
    | SortKItem.inj_SortPValue x => some x
    | _ => none

instance : Inj SortNumValue SortKItem where
  inj := SortKItem.inj_SortNumValue
  retr
    | SortKItem.inj_SortNumValue x => some x
    | _ => none

instance : Inj SortPyStmt SortKItem where
  inj := SortKItem.inj_SortPyStmt
  retr
    | SortKItem.inj_SortPyStmt x => some x
    | _ => none

instance : Inj SortFunctionsCell SortKItem where
  inj := SortKItem.inj_SortFunctionsCell
  retr
    | SortKItem.inj_SortFunctionsCell x => some x
    | _ => none

instance : Inj SortNumValue SortPValue where
  inj := SortPValue.inj_SortNumValue
  retr
    | SortPValue.inj_SortNumValue x => some x
    | _ => none