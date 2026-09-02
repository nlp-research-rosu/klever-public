import Klean28Concatenate.Sorts

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortPyStmts SortKItem where
  inj := SortKItem.inj_SortPyStmts
  retr
    | SortKItem.inj_SortPyStmts x => some x
    | _ => none

instance : Inj SortPyStmt SortKItem where
  inj := SortKItem.inj_SortPyStmt
  retr
    | SortKItem.inj_SortPyStmt x => some x
    | _ => none

instance : Inj SortParams SortKItem where
  inj := SortKItem.inj_SortParams
  retr
    | SortKItem.inj_SortParams x => some x
    | _ => none

instance : Inj SortPyProgram SortKItem where
  inj := SortKItem.inj_SortPyProgram
  retr
    | SortKItem.inj_SortPyProgram x => some x
    | _ => none

instance : Inj SortPyVal SortKItem where
  inj := SortKItem.inj_SortPyVal
  retr
    | SortKItem.inj_SortPyVal x => some x
    | _ => none

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
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

instance : Inj SortGeneratedTopCell SortKItem where
  inj := SortKItem.inj_SortGeneratedTopCell
  retr
    | SortKItem.inj_SortGeneratedTopCell x => some x
    | _ => none

instance : Inj SortStrList SortKItem where
  inj := SortKItem.inj_SortStrList
  retr
    | SortKItem.inj_SortStrList x => some x
    | _ => none

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none