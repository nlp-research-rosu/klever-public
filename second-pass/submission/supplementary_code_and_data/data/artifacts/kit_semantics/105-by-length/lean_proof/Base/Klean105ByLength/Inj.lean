import Klean105ByLength.Sorts

instance : Inj SortBool SortBound where
  inj := SortBound.inj_SortBool
  retr
    | SortBound.inj_SortBool x => some x
    | _ => none

instance : Inj SortExpr SortBound where
  inj
    | SortExpr.inj_SortBool x => SortBound.inj_SortBool x
    | SortExpr.inj_SortFloat x => SortBound.inj_SortFloat x
    | SortExpr.inj_SortInt x => SortBound.inj_SortInt x
    | SortExpr.inj_SortIterable x => SortBound.inj_SortIterable x
    | SortExpr.inj_SortStr x => SortBound.inj_SortStr x
    | SortExpr.inj_SortVal x => SortBound.inj_SortVal x
    | x => SortBound.inj_SortExpr x
  retr
    | SortBound.inj_SortBool x => some (SortExpr.inj_SortBool x)
    | SortBound.inj_SortFloat x => some (SortExpr.inj_SortFloat x)
    | SortBound.inj_SortInt x => some (SortExpr.inj_SortInt x)
    | SortBound.inj_SortIterable x => some (SortExpr.inj_SortIterable x)
    | SortBound.inj_SortStr x => some (SortExpr.inj_SortStr x)
    | SortBound.inj_SortVal x => some (SortExpr.inj_SortVal x)
    | SortBound.inj_SortExpr x => some x
    | _ => none

instance : Inj SortFloat SortBound where
  inj := SortBound.inj_SortFloat
  retr
    | SortBound.inj_SortFloat x => some x
    | _ => none

instance : Inj SortInt SortBound where
  inj := SortBound.inj_SortInt
  retr
    | SortBound.inj_SortInt x => some x
    | _ => none

instance : Inj SortIterable SortBound where
  inj
    | SortIterable.inj_SortStr x => SortBound.inj_SortStr x
    | x => SortBound.inj_SortIterable x
  retr
    | SortBound.inj_SortStr x => some (SortIterable.inj_SortStr x)
    | SortBound.inj_SortIterable x => some x
    | _ => none

instance : Inj SortStr SortBound where
  inj := SortBound.inj_SortStr
  retr
    | SortBound.inj_SortStr x => some x
    | _ => none

instance : Inj SortVal SortBound where
  inj
    | SortVal.inj_SortBool x => SortBound.inj_SortBool x
    | SortVal.inj_SortFloat x => SortBound.inj_SortFloat x
    | SortVal.inj_SortInt x => SortBound.inj_SortInt x
    | SortVal.inj_SortIterable x => SortBound.inj_SortIterable x
    | SortVal.inj_SortStr x => SortBound.inj_SortStr x
    | x => SortBound.inj_SortVal x
  retr
    | SortBound.inj_SortBool x => some (SortVal.inj_SortBool x)
    | SortBound.inj_SortFloat x => some (SortVal.inj_SortFloat x)
    | SortBound.inj_SortInt x => some (SortVal.inj_SortInt x)
    | SortBound.inj_SortIterable x => some (SortVal.inj_SortIterable x)
    | SortBound.inj_SortStr x => some (SortVal.inj_SortStr x)
    | SortBound.inj_SortVal x => some x
    | _ => none

instance : Inj SortBool SortExpr where
  inj := SortExpr.inj_SortBool
  retr
    | SortExpr.inj_SortBool x => some x
    | _ => none

instance : Inj SortFloat SortExpr where
  inj := SortExpr.inj_SortFloat
  retr
    | SortExpr.inj_SortFloat x => some x
    | _ => none

instance : Inj SortInt SortExpr where
  inj := SortExpr.inj_SortInt
  retr
    | SortExpr.inj_SortInt x => some x
    | _ => none

instance : Inj SortIterable SortExpr where
  inj
    | SortIterable.inj_SortStr x => SortExpr.inj_SortStr x
    | x => SortExpr.inj_SortIterable x
  retr
    | SortExpr.inj_SortStr x => some (SortIterable.inj_SortStr x)
    | SortExpr.inj_SortIterable x => some x
    | _ => none

instance : Inj SortStr SortExpr where
  inj := SortExpr.inj_SortStr
  retr
    | SortExpr.inj_SortStr x => some x
    | _ => none

instance : Inj SortVal SortExpr where
  inj
    | SortVal.inj_SortBool x => SortExpr.inj_SortBool x
    | SortVal.inj_SortFloat x => SortExpr.inj_SortFloat x
    | SortVal.inj_SortInt x => SortExpr.inj_SortInt x
    | SortVal.inj_SortIterable x => SortExpr.inj_SortIterable x
    | SortVal.inj_SortStr x => SortExpr.inj_SortStr x
    | x => SortExpr.inj_SortVal x
  retr
    | SortExpr.inj_SortBool x => some (SortVal.inj_SortBool x)
    | SortExpr.inj_SortFloat x => some (SortVal.inj_SortFloat x)
    | SortExpr.inj_SortInt x => some (SortVal.inj_SortInt x)
    | SortExpr.inj_SortIterable x => some (SortVal.inj_SortIterable x)
    | SortExpr.inj_SortStr x => some (SortVal.inj_SortStr x)
    | SortExpr.inj_SortVal x => some x
    | _ => none

instance : Inj SortBool SortIndex where
  inj := SortIndex.inj_SortBool
  retr
    | SortIndex.inj_SortBool x => some x
    | _ => none

instance : Inj SortExpr SortIndex where
  inj
    | SortExpr.inj_SortBool x => SortIndex.inj_SortBool x
    | SortExpr.inj_SortFloat x => SortIndex.inj_SortFloat x
    | SortExpr.inj_SortInt x => SortIndex.inj_SortInt x
    | SortExpr.inj_SortIterable x => SortIndex.inj_SortIterable x
    | SortExpr.inj_SortStr x => SortIndex.inj_SortStr x
    | SortExpr.inj_SortVal x => SortIndex.inj_SortVal x
    | x => SortIndex.inj_SortExpr x
  retr
    | SortIndex.inj_SortBool x => some (SortExpr.inj_SortBool x)
    | SortIndex.inj_SortFloat x => some (SortExpr.inj_SortFloat x)
    | SortIndex.inj_SortInt x => some (SortExpr.inj_SortInt x)
    | SortIndex.inj_SortIterable x => some (SortExpr.inj_SortIterable x)
    | SortIndex.inj_SortStr x => some (SortExpr.inj_SortStr x)
    | SortIndex.inj_SortVal x => some (SortExpr.inj_SortVal x)
    | SortIndex.inj_SortExpr x => some x
    | _ => none

instance : Inj SortFloat SortIndex where
  inj := SortIndex.inj_SortFloat
  retr
    | SortIndex.inj_SortFloat x => some x
    | _ => none

instance : Inj SortInt SortIndex where
  inj := SortIndex.inj_SortInt
  retr
    | SortIndex.inj_SortInt x => some x
    | _ => none

instance : Inj SortIterable SortIndex where
  inj
    | SortIterable.inj_SortStr x => SortIndex.inj_SortStr x
    | x => SortIndex.inj_SortIterable x
  retr
    | SortIndex.inj_SortStr x => some (SortIterable.inj_SortStr x)
    | SortIndex.inj_SortIterable x => some x
    | _ => none

instance : Inj SortStr SortIndex where
  inj := SortIndex.inj_SortStr
  retr
    | SortIndex.inj_SortStr x => some x
    | _ => none

instance : Inj SortVal SortIndex where
  inj
    | SortVal.inj_SortBool x => SortIndex.inj_SortBool x
    | SortVal.inj_SortFloat x => SortIndex.inj_SortFloat x
    | SortVal.inj_SortInt x => SortIndex.inj_SortInt x
    | SortVal.inj_SortIterable x => SortIndex.inj_SortIterable x
    | SortVal.inj_SortStr x => SortIndex.inj_SortStr x
    | x => SortIndex.inj_SortVal x
  retr
    | SortIndex.inj_SortBool x => some (SortVal.inj_SortBool x)
    | SortIndex.inj_SortFloat x => some (SortVal.inj_SortFloat x)
    | SortIndex.inj_SortInt x => some (SortVal.inj_SortInt x)
    | SortIndex.inj_SortIterable x => some (SortVal.inj_SortIterable x)
    | SortIndex.inj_SortStr x => some (SortVal.inj_SortStr x)
    | SortIndex.inj_SortVal x => some x
    | _ => none

instance : Inj SortStr SortIterable where
  inj := SortIterable.inj_SortStr
  retr
    | SortIterable.inj_SortStr x => some x
    | _ => none

instance : Inj SortApplyK SortKItem where
  inj := SortKItem.inj_SortApplyK
  retr
    | SortKItem.inj_SortApplyK x => some x
    | _ => none

instance : Inj SortBool SortKItem where
  inj := SortKItem.inj_SortBool
  retr
    | SortKItem.inj_SortBool x => some x
    | _ => none

instance : Inj SortBound SortKItem where
  inj
    | SortBound.inj_SortBool x => SortKItem.inj_SortBool x
    | SortBound.inj_SortExpr x => SortKItem.inj_SortExpr x
    | SortBound.inj_SortFloat x => SortKItem.inj_SortFloat x
    | SortBound.inj_SortInt x => SortKItem.inj_SortInt x
    | SortBound.inj_SortIterable x => SortKItem.inj_SortIterable x
    | SortBound.inj_SortStr x => SortKItem.inj_SortStr x
    | SortBound.inj_SortVal x => SortKItem.inj_SortVal x
    | x => SortKItem.inj_SortBound x
  retr
    | SortKItem.inj_SortBool x => some (SortBound.inj_SortBool x)
    | SortKItem.inj_SortExpr x => some (SortBound.inj_SortExpr x)
    | SortKItem.inj_SortFloat x => some (SortBound.inj_SortFloat x)
    | SortKItem.inj_SortInt x => some (SortBound.inj_SortInt x)
    | SortKItem.inj_SortIterable x => some (SortBound.inj_SortIterable x)
    | SortKItem.inj_SortStr x => some (SortBound.inj_SortStr x)
    | SortKItem.inj_SortVal x => some (SortBound.inj_SortVal x)
    | SortKItem.inj_SortBound x => some x
    | _ => none

instance : Inj SortCellVars SortKItem where
  inj := SortKItem.inj_SortCellVars
  retr
    | SortKItem.inj_SortCellVars x => some x
    | _ => none

instance : Inj SortCmpOp SortKItem where
  inj := SortKItem.inj_SortCmpOp
  retr
    | SortKItem.inj_SortCmpOp x => some x
    | _ => none

instance : Inj SortEntries SortKItem where
  inj := SortKItem.inj_SortEntries
  retr
    | SortKItem.inj_SortEntries x => some x
    | _ => none

instance : Inj SortEntry SortKItem where
  inj := SortKItem.inj_SortEntry
  retr
    | SortKItem.inj_SortEntry x => some x
    | _ => none

instance : Inj SortEnvCell SortKItem where
  inj := SortKItem.inj_SortEnvCell
  retr
    | SortKItem.inj_SortEnvCell x => some x
    | _ => none

instance : Inj SortExc SortKItem where
  inj := SortKItem.inj_SortExc
  retr
    | SortKItem.inj_SortExc x => some x
    | _ => none

instance : Inj SortExcCell SortKItem where
  inj := SortKItem.inj_SortExcCell
  retr
    | SortKItem.inj_SortExcCell x => some x
    | _ => none

instance : Inj SortExitCodeCell SortKItem where
  inj := SortKItem.inj_SortExitCodeCell
  retr
    | SortKItem.inj_SortExitCodeCell x => some x
    | _ => none

instance : Inj SortExpr SortKItem where
  inj
    | SortExpr.inj_SortBool x => SortKItem.inj_SortBool x
    | SortExpr.inj_SortFloat x => SortKItem.inj_SortFloat x
    | SortExpr.inj_SortInt x => SortKItem.inj_SortInt x
    | SortExpr.inj_SortIterable x => SortKItem.inj_SortIterable x
    | SortExpr.inj_SortStr x => SortKItem.inj_SortStr x
    | SortExpr.inj_SortVal x => SortKItem.inj_SortVal x
    | x => SortKItem.inj_SortExpr x
  retr
    | SortKItem.inj_SortBool x => some (SortExpr.inj_SortBool x)
    | SortKItem.inj_SortFloat x => some (SortExpr.inj_SortFloat x)
    | SortKItem.inj_SortInt x => some (SortExpr.inj_SortInt x)
    | SortKItem.inj_SortIterable x => some (SortExpr.inj_SortIterable x)
    | SortKItem.inj_SortStr x => some (SortExpr.inj_SortStr x)
    | SortKItem.inj_SortVal x => some (SortExpr.inj_SortVal x)
    | SortKItem.inj_SortExpr x => some x
    | _ => none

instance : Inj SortExprs SortKItem where
  inj := SortKItem.inj_SortExprs
  retr
    | SortKItem.inj_SortExprs x => some x
    | _ => none

instance : Inj SortFloat SortKItem where
  inj := SortKItem.inj_SortFloat
  retr
    | SortKItem.inj_SortFloat x => some x
    | _ => none

instance : Inj SortFreeVars SortKItem where
  inj := SortKItem.inj_SortFreeVars
  retr
    | SortKItem.inj_SortFreeVars x => some x
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

instance : Inj SortHeapCell SortKItem where
  inj := SortKItem.inj_SortHeapCell
  retr
    | SortKItem.inj_SortHeapCell x => some x
    | _ => none

instance : Inj SortHeapLocCell SortKItem where
  inj := SortKItem.inj_SortHeapLocCell
  retr
    | SortKItem.inj_SortHeapLocCell x => some x
    | _ => none

instance : Inj SortIndex SortKItem where
  inj
    | SortIndex.inj_SortBool x => SortKItem.inj_SortBool x
    | SortIndex.inj_SortExpr x => SortKItem.inj_SortExpr x
    | SortIndex.inj_SortFloat x => SortKItem.inj_SortFloat x
    | SortIndex.inj_SortInt x => SortKItem.inj_SortInt x
    | SortIndex.inj_SortIterable x => SortKItem.inj_SortIterable x
    | SortIndex.inj_SortStr x => SortKItem.inj_SortStr x
    | SortIndex.inj_SortVal x => SortKItem.inj_SortVal x
    | x => SortKItem.inj_SortIndex x
  retr
    | SortKItem.inj_SortBool x => some (SortIndex.inj_SortBool x)
    | SortKItem.inj_SortExpr x => some (SortIndex.inj_SortExpr x)
    | SortKItem.inj_SortFloat x => some (SortIndex.inj_SortFloat x)
    | SortKItem.inj_SortInt x => some (SortIndex.inj_SortInt x)
    | SortKItem.inj_SortIterable x => some (SortIndex.inj_SortIterable x)
    | SortKItem.inj_SortStr x => some (SortIndex.inj_SortStr x)
    | SortKItem.inj_SortVal x => some (SortIndex.inj_SortVal x)
    | SortKItem.inj_SortIndex x => some x
    | _ => none

instance : Inj SortInt SortKItem where
  inj := SortKItem.inj_SortInt
  retr
    | SortKItem.inj_SortInt x => some x
    | _ => none

instance : Inj SortIntSeq SortKItem where
  inj := SortKItem.inj_SortIntSeq
  retr
    | SortKItem.inj_SortIntSeq x => some x
    | _ => none

instance : Inj SortIterable SortKItem where
  inj
    | SortIterable.inj_SortStr x => SortKItem.inj_SortStr x
    | x => SortKItem.inj_SortIterable x
  retr
    | SortKItem.inj_SortStr x => some (SortIterable.inj_SortStr x)
    | SortKItem.inj_SortIterable x => some x
    | _ => none

instance : Inj SortKCell SortKItem where
  inj := SortKItem.inj_SortKCell
  retr
    | SortKItem.inj_SortKCell x => some x
    | _ => none

instance : Inj SortList SortKItem where
  inj := SortKItem.inj_SortList
  retr
    | SortKItem.inj_SortList x => some x
    | _ => none

instance : Inj SortMap SortKItem where
  inj := SortKItem.inj_SortMap
  retr
    | SortKItem.inj_SortMap x => some x
    | _ => none

instance : Inj SortModule SortKItem where
  inj := SortKItem.inj_SortModule
  retr
    | SortKItem.inj_SortModule x => some x
    | _ => none

instance : Inj SortOptInt SortKItem where
  inj := SortKItem.inj_SortOptInt
  retr
    | SortKItem.inj_SortOptInt x => some x
    | _ => none

instance : Inj SortParamNames SortKItem where
  inj := SortKItem.inj_SortParamNames
  retr
    | SortKItem.inj_SortParamNames x => some x
    | _ => none

instance : Inj SortParams SortKItem where
  inj := SortKItem.inj_SortParams
  retr
    | SortKItem.inj_SortParams x => some x
    | _ => none

instance : Inj SortRetCell SortKItem where
  inj := SortKItem.inj_SortRetCell
  retr
    | SortKItem.inj_SortRetCell x => some x
    | _ => none

instance : Inj SortRetState SortKItem where
  inj := SortKItem.inj_SortRetState
  retr
    | SortKItem.inj_SortRetState x => some x
    | _ => none

instance : Inj SortScopeLocCell SortKItem where
  inj := SortKItem.inj_SortScopeLocCell
  retr
    | SortKItem.inj_SortScopeLocCell x => some x
    | _ => none

instance : Inj SortScopesCell SortKItem where
  inj := SortKItem.inj_SortScopesCell
  retr
    | SortKItem.inj_SortScopesCell x => some x
    | _ => none

instance : Inj SortStackCell SortKItem where
  inj := SortKItem.inj_SortStackCell
  retr
    | SortKItem.inj_SortStackCell x => some x
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

instance : Inj SortStr SortKItem where
  inj := SortKItem.inj_SortStr
  retr
    | SortKItem.inj_SortStr x => some x
    | _ => none

instance : Inj SortString SortKItem where
  inj := SortKItem.inj_SortString
  retr
    | SortKItem.inj_SortString x => some x
    | _ => none

instance : Inj SortVal SortKItem where
  inj
    | SortVal.inj_SortBool x => SortKItem.inj_SortBool x
    | SortVal.inj_SortFloat x => SortKItem.inj_SortFloat x
    | SortVal.inj_SortInt x => SortKItem.inj_SortInt x
    | SortVal.inj_SortIterable x => SortKItem.inj_SortIterable x
    | SortVal.inj_SortStr x => SortKItem.inj_SortStr x
    | x => SortKItem.inj_SortVal x
  retr
    | SortKItem.inj_SortBool x => some (SortVal.inj_SortBool x)
    | SortKItem.inj_SortFloat x => some (SortVal.inj_SortFloat x)
    | SortKItem.inj_SortInt x => some (SortVal.inj_SortInt x)
    | SortKItem.inj_SortIterable x => some (SortVal.inj_SortIterable x)
    | SortKItem.inj_SortStr x => some (SortVal.inj_SortStr x)
    | SortKItem.inj_SortVal x => some x
    | _ => none

instance : Inj SortValSeq SortKItem where
  inj := SortKItem.inj_SortValSeq
  retr
    | SortKItem.inj_SortValSeq x => some x
    | _ => none

instance : Inj SortVals SortKItem where
  inj := SortKItem.inj_SortVals
  retr
    | SortKItem.inj_SortVals x => some x
    | _ => none

instance : Inj SortBool SortVal where
  inj := SortVal.inj_SortBool
  retr
    | SortVal.inj_SortBool x => some x
    | _ => none

instance : Inj SortFloat SortVal where
  inj := SortVal.inj_SortFloat
  retr
    | SortVal.inj_SortFloat x => some x
    | _ => none

instance : Inj SortInt SortVal where
  inj := SortVal.inj_SortInt
  retr
    | SortVal.inj_SortInt x => some x
    | _ => none

instance : Inj SortIterable SortVal where
  inj
    | SortIterable.inj_SortStr x => SortVal.inj_SortStr x
    | x => SortVal.inj_SortIterable x
  retr
    | SortVal.inj_SortStr x => some (SortIterable.inj_SortStr x)
    | SortVal.inj_SortIterable x => some x
    | _ => none

instance : Inj SortStr SortVal where
  inj := SortVal.inj_SortStr
  retr
    | SortVal.inj_SortStr x => some x
    | _ => none