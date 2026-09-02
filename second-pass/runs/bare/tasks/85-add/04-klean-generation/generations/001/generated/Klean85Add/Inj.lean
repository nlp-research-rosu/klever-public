import Klean85Add.Sorts

instance : Inj SortFunctionsCell SortKItem where
  inj := SortKItem.inj_SortFunctionsCell
  retr
    | SortKItem.inj_SortFunctionsCell x => some x
    | _ => none

instance : Inj SortEnvCell SortKItem where
  inj := SortKItem.inj_SortEnvCell
  retr
    | SortKItem.inj_SortEnvCell x => some x
    | _ => none

instance : Inj SortISeq SortKItem where
  inj := SortKItem.inj_SortISeq
  retr
    | SortKItem.inj_SortISeq x => some x
    | _ => none

instance : Inj SortExpr SortKItem where
  inj := SortKItem.inj_SortExpr
  retr
    | SortKItem.inj_SortExpr x => some x
    | _ => none

instance : Inj SortCallStackCell SortKItem where
  inj := SortKItem.inj_SortCallStackCell
  retr
    | SortKItem.inj_SortCallStackCell x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortGeneratedCounterCell SortKItem where
  inj := SortKItem.inj_SortGeneratedCounterCell
  retr
    | SortKItem.inj_SortGeneratedCounterCell x => some x
    | _ => none

instance : Inj SortIndex SortKItem where
  inj
    | SortIndex.inj_SortExpr x => SortKItem.inj_SortExpr x
    | x => SortKItem.inj_SortIndex x
  retr
    | SortKItem.inj_SortExpr x => some (SortIndex.inj_SortExpr x)
    | SortKItem.inj_SortIndex x => some x
    | _ => none

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none

instance : Inj SortList SortKItem where
  inj := SortKItem.inj_SortList
  retr
    | SortKItem.inj_SortList x => some x
    | _ => none

instance : Inj SortCmpOp SortKItem where
  inj := SortKItem.inj_SortCmpOp
  retr
    | SortKItem.inj_SortCmpOp x => some x
    | _ => none

instance : Inj SortInt SortKItem where
  inj := SortKItem.inj_SortInt
  retr
    | SortKItem.inj_SortInt x => some x
    | _ => none

instance : Inj SortInputCell SortKItem where
  inj := SortKItem.inj_SortInputCell
  retr
    | SortKItem.inj_SortInputCell x => some x
    | _ => none

instance : Inj SortGeneratedTopCell SortKItem where
  inj := SortKItem.inj_SortGeneratedTopCell
  retr
    | SortKItem.inj_SortGeneratedTopCell x => some x
    | _ => none

instance : Inj SortPyVal SortKItem where
  inj := SortKItem.inj_SortPyVal
  retr
    | SortKItem.inj_SortPyVal x => some x
    | _ => none

instance : Inj SortBound SortKItem where
  inj
    | SortBound.inj_SortExpr x => SortKItem.inj_SortExpr x
    | x => SortKItem.inj_SortBound x
  retr
    | SortKItem.inj_SortExpr x => some (SortBound.inj_SortExpr x)
    | SortKItem.inj_SortBound x => some x
    | _ => none

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortMap SortKItem where
  inj := SortKItem.inj_SortMap
  retr
    | SortKItem.inj_SortMap x => some x
    | _ => none

instance : Inj SortMpyCell SortKItem where
  inj := SortKItem.inj_SortMpyCell
  retr
    | SortKItem.inj_SortMpyCell x => some x
    | _ => none

instance : Inj SortExpr SortIndex where
  inj := SortIndex.inj_SortExpr
  retr
    | SortIndex.inj_SortExpr x => some x
    | _ => none

instance : Inj SortExpr SortBound where
  inj := SortBound.inj_SortExpr
  retr
    | SortBound.inj_SortExpr x => some x
    | _ => none