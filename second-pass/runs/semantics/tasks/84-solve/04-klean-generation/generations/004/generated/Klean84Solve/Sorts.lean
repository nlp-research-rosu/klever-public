import Klean84Solve.Prelude

inductive SortExc : Type where
  | «AssertionError_MPY-CORE_Exc» : SortExc
  | «NoExc_MPY-CORE_Exc» : SortExc

structure SortExcCell : Type where
  val : SortExc

structure SortEnvCell : Type where
  val : SortInt

structure SortExitCodeCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

structure SortHeapLocCell : Type where
  val : SortInt

inductive SortIntSeq : Type where
  | «.IntSeq_MPY-CORE_IntSeq» : SortIntSeq
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : SortIntSeq

inductive SortOptInt : Type where
  | «noB_MPY-SUBSCRIPT_OptInt» : SortOptInt
  | «someB(_)_MPY-SUBSCRIPT_OptInt_Int» (x0 : SortInt) : SortOptInt

structure SortScopeLocCell : Type where
  val : SortInt

inductive SortParamNames : Type where
  | «.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames» : SortParamNames
  | «_,__MPY-SYNTAX_ParamNames_String_ParamNames» (x0 : SortString) (x1 : SortParamNames) : SortParamNames

inductive SortStr : Type where
  | «str(_)_MPY-CORE_Str_IntSeq» (x0 : SortIntSeq) : SortStr

inductive SortCellVars : Type where
  | «CellVars(_)_MPY-SYNTAX_CellVars_ParamNames» (x0 : SortParamNames) : SortCellVars

inductive SortFreeVars : Type where
  | «FreeVars(_)_MPY-SYNTAX_FreeVars_ParamNames» (x0 : SortParamNames) : SortFreeVars

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_ParamNames» (x0 : SortParamNames) : SortParams

mutual
  inductive SortApplyK : Type where
    | «toCall(_)_MPY-CORE_ApplyK_Val» (x0 : SortVal) : SortApplyK
    | «toList_MPY-LIST_ApplyK» : SortApplyK
    | «toTuple_MPY-TUPLE_ApplyK» : SortApplyK

  inductive SortBound : Type where
    | inj_SortBool (x : SortBool) : SortBound
    | inj_SortExpr (x : SortExpr) : SortBound
    | inj_SortFloat (x : SortFloat) : SortBound
    | inj_SortInt (x : SortInt) : SortBound
    | inj_SortIterable (x : SortIterable) : SortBound
    | inj_SortStr (x : SortStr) : SortBound
    | inj_SortVal (x : SortVal) : SortBound
    | «NoBound_MPY-SYNTAX_Bound» : SortBound

  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortEntries : Type where
    | «.List{"_,__MPY-SYNTAX_Entries_Entry_Entries"}_Entries» : SortEntries
    | «_,__MPY-SYNTAX_Entries_Entry_Entries» (x0 : SortEntry) (x1 : SortEntries) : SortEntries

  inductive SortEntry : Type where
    | «Entry(_,_)_MPY-SYNTAX_Entry_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortEntry

  inductive SortExpr : Type where
    | inj_SortBool (x : SortBool) : SortExpr
    | inj_SortFloat (x : SortFloat) : SortExpr
    | inj_SortInt (x : SortInt) : SortExpr
    | inj_SortIterable (x : SortIterable) : SortExpr
    | inj_SortStr (x : SortStr) : SortExpr
    | inj_SortVal (x : SortVal) : SortExpr
    | «Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» (x0 : SortExpr) (x1 : SortString) : SortExpr
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Bool(_)_MPY-SYNTAX_Expr_Bool» (x0 : SortBool) : SortExpr
    | «BoolOp(_,_)_MPY-SYNTAX_Expr_String_Exprs» (x0 : SortString) (x1 : SortExprs) : SortExpr
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «DictExpr(_)_MPY-SYNTAX_Expr_Entries» (x0 : SortEntries) : SortExpr
    | «Float(_)_MPY-SYNTAX_Expr_Float» (x0 : SortFloat) : SortExpr
    | «IfExp(_,_,_)_MPY-SYNTAX_Expr_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «KwArg(_,_)_MPY-SYNTAX_Expr_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortExpr
    | «Lambda(_,_,_,_)_MPY-SYNTAX_Expr_Params_CellVars_FreeVars_Expr» (x0 : SortParams) (x1 : SortCellVars) (x2 : SortFreeVars) (x3 : SortExpr) : SortExpr
    | «Lambda(_,_)_MPY-SYNTAX_Expr_Params_Expr» (x0 : SortParams) (x1 : SortExpr) : SortExpr
    | «ListExpr(_)_MPY-SYNTAX_Expr_Exprs» (x0 : SortExprs) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «NoneVal_MPY-SYNTAX_Expr» : SortExpr
    | «Str(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (x0 : SortExpr) (x1 : SortIndex) : SortExpr
    | «TupleExpr(_)_MPY-SYNTAX_Expr_Exprs» (x0 : SortExprs) : SortExpr
    | «UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortExpr
    | «closureExpr(_,_)_MPY-FUNCTIONS_Expr_ParamNames_Stmts» (x0 : SortParamNames) (x1 : SortStmts) : SortExpr

  inductive SortExprs : Type where
    | «.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs» : SortExprs
    | «_,__MPY-SYNTAX_Exprs_Expr_Exprs» (x0 : SortExpr) (x1 : SortExprs) : SortExprs

  structure SortGeneratedTopCell : Type where
    k : SortKCell
    env : SortEnvCell
    scopes : SortScopesCell
    scopeLoc : SortScopeLocCell
    heap : SortHeapCell
    heapLoc : SortHeapLocCell
    stack : SortStackCell
    ret : SortRetCell
    exc : SortExcCell
    exitCode : SortExitCodeCell
    generatedCounter : SortGeneratedCounterCell

  structure SortHeapCell : Type where
    val : SortMap

  inductive SortIndex : Type where
    | inj_SortBool (x : SortBool) : SortIndex
    | inj_SortExpr (x : SortExpr) : SortIndex
    | inj_SortFloat (x : SortFloat) : SortIndex
    | inj_SortInt (x : SortInt) : SortIndex
    | inj_SortIterable (x : SortIterable) : SortIndex
    | inj_SortStr (x : SortStr) : SortIndex
    | inj_SortVal (x : SortVal) : SortIndex
    | «Slice(_,_,_)_MPY-SYNTAX_Index_Bound_Bound_Bound» (x0 : SortBound) (x1 : SortBound) (x2 : SortBound) : SortIndex

  inductive SortIterable : Type where
    | inj_SortStr (x : SortStr) : SortIterable
    | «list(_)_MPY-CORE_Iterable_ValSeq» (x0 : SortValSeq) : SortIterable
    | «rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : SortIterable
    | «tuple(_)_MPY-CORE_Iterable_ValSeq» (x0 : SortValSeq) : SortIterable
    | «zipObj(_,_)_MPY-CORE_Iterable_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : SortIterable
    | «zipObjS(_,_)_MPY-CORE_Iterable_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : SortIterable

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortApplyK (x : SortApplyK) : SortKItem
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortBound (x : SortBound) : SortKItem
    | inj_SortCellVars (x : SortCellVars) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortEntries (x : SortEntries) : SortKItem
    | inj_SortEntry (x : SortEntry) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExc (x : SortExc) : SortKItem
    | inj_SortExcCell (x : SortExcCell) : SortKItem
    | inj_SortExitCodeCell (x : SortExitCodeCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortFloat (x : SortFloat) : SortKItem
    | inj_SortFreeVars (x : SortFreeVars) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortHeapCell (x : SortHeapCell) : SortKItem
    | inj_SortHeapLocCell (x : SortHeapLocCell) : SortKItem
    | inj_SortIndex (x : SortIndex) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortIntSeq (x : SortIntSeq) : SortKItem
    | inj_SortIterable (x : SortIterable) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortList (x : SortList) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortModule (x : SortModule) : SortKItem
    | inj_SortOptInt (x : SortOptInt) : SortKItem
    | inj_SortParamNames (x : SortParamNames) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortRetCell (x : SortRetCell) : SortKItem
    | inj_SortRetState (x : SortRetState) : SortKItem
    | inj_SortScopeLocCell (x : SortScopeLocCell) : SortKItem
    | inj_SortScopesCell (x : SortScopesCell) : SortKItem
    | inj_SortStackCell (x : SortStackCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortStr (x : SortStr) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortVal (x : SortVal) : SortKItem
    | inj_SortValSeq (x : SortValSeq) : SortKItem
    | inj_SortVals (x : SortVals) : SortKItem
    | «#allAcc(_)_MPY-BUILTINS_KItem_Iterable» (x0 : SortIterable) : SortKItem
    | «#allCont_MPY-BUILTINS_KItem» : SortKItem
    | «#alloc(_)_MPY-CORE_KItem_Val» (x0 : SortVal) : SortKItem
    | «#allocCells(_)_MPY-CALL_KItem_ParamNames» (x0 : SortParamNames) : SortKItem
    | «#anyAcc(_)_MPY-BUILTINS_KItem_Iterable» (x0 : SortIterable) : SortKItem
    | «#anyCont_MPY-BUILTINS_KItem» : SortKItem
    | «#applyK(_,_)_MPY-CORE_KItem_ApplyK_Vals» (x0 : SortApplyK) (x1 : SortVals) : SortKItem
    | «#bindImports(_)_MPY-CONTROLS_KItem_ParamNames» (x0 : SortParamNames) : SortKItem
    | «#bindP(_,_)_MPY-FUNCTIONS_KItem_ParamNames_Vals» (x0 : SortParamNames) (x1 : SortVals) : SortKItem
    | «#bindTgt(_,_)_MPY-TUPLE_KItem_Expr_Val» (x0 : SortExpr) (x1 : SortVal) : SortKItem
    | «#branch(_,_,_)_MPY-CONTROLS_KItem_Bool_Stmts_Stmts» (x0 : SortBool) (x1 : SortStmts) (x2 : SortStmts) : SortKItem
    | «#brk_MPY-CONTROLS_KItem» : SortKItem
    | «#callee(_)_MPY-CALL_KItem_Exprs» (x0 : SortExprs) : SortKItem
    | «#cellW(_,_)_MPY-CORE_KItem_Val_Val» (x0 : SortVal) (x1 : SortVal) : SortKItem
    | «#cont_MPY-CONTROLS_KItem» : SortKItem
    | «#dictAcc(_,_,_)_MPY-DICT_KItem_Entries_ValSeq_ValSeq» (x0 : SortEntries) (x1 : SortValSeq) (x2 : SortValSeq) : SortKItem
    | «#dictKey(_,_,_,_)_MPY-DICT_KItem_Expr_Entries_ValSeq_ValSeq» (x0 : SortExpr) (x1 : SortEntries) (x2 : SortValSeq) (x3 : SortValSeq) : SortKItem
    | «#dictVal(_,_,_,_)_MPY-DICT_KItem_Val_Entries_ValSeq_ValSeq» (x0 : SortVal) (x1 : SortEntries) (x2 : SortValSeq) (x3 : SortValSeq) : SortKItem
    | «#dsetK(_,_)_MPY-DICT_KItem_String_Val» (x0 : SortString) (x1 : SortVal) : SortKItem
    | «#dsetV(_,_,_)_MPY-DICT_KItem_Val_Val_Val» (x0 : SortVal) (x1 : SortVal) (x2 : SortVal) : SortKItem
    | «#endcall_MPY-FUNCTIONS_KItem» : SortKItem
    | «#evalArgCont(_,_,_)_MPY-CORE_KItem_Exprs_Vals_ApplyK» (x0 : SortExprs) (x1 : SortVals) (x2 : SortApplyK) : SortKItem
    | «#evalArgs(_,_,_)_MPY-CORE_KItem_Exprs_Vals_ApplyK» (x0 : SortExprs) (x1 : SortVals) (x2 : SortApplyK) : SortKItem
    | «#evalB(_)_MPY-SUBSCRIPT_KItem_Bound» (x0 : SortBound) : SortKItem
    | «#freezerAssert(_)_MPY-SYNTAX_Stmt_Expr0_» : SortKItem
    | «#freezerAssign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr1_» (x0 : SortK) : SortKItem
    | «#freezerAttribute(_,_)_MPY-SYNTAX_Expr_Expr_String0_» (x0 : SortK) : SortKItem
    | «#freezerAugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr2_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr1_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr2_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerBoolOp(_,_)_MPY-SYNTAX_Expr_String_Exprs1_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerCompare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp0_» (x0 : SortK) : SortKItem
    | «#freezerCompare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp2_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerExpr(_)_MPY-SYNTAX_Stmt_Expr0_» : SortKItem
    | «#freezerFor(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts1_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerIf(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts0_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerIfExp(_,_,_)_MPY-SYNTAX_Expr_Expr_Expr_Expr0_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerReturn(_)_MPY-SYNTAX_Stmt_Expr0_» : SortKItem
    | «#freezerSubscript(_,_)_MPY-SYNTAX_Expr_Expr_Index0_» (x0 : SortK) : SortKItem
    | «#freezerSubscript(_,_)_MPY-SYNTAX_Expr_Expr_Index1_» (x0 : SortK) : SortKItem
    | «#freezerUnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr1_» (x0 : SortK) : SortKItem
    | «#iterDone_MPY-ITER_KItem» : SortKItem
    | «#iterNext(_)_MPY-ITER_KItem_Iterable» (x0 : SortIterable) : SortKItem
    | «#iterYield(_,_)_MPY-ITER_KItem_Val_Iterable» (x0 : SortVal) (x1 : SortIterable) : SortKItem
    | «#kwTag(_)_MPY-CORE_KItem_String» (x0 : SortString) : SortKItem
    | «#kxExport0(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport2(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#loadAll(_)_MPY-CORE_KItem_Module» (x0 : SortModule) : SortKItem
    | «#look(_,_)_MPY-CORE_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «#loop(_,_,_)_MPY-CONTROLS_KItem_Val_Expr_Stmts» (x0 : SortVal) (x1 : SortExpr) (x2 : SortStmts) : SortKItem
    | «#loopLbl(_)_MPY-CONTROLS_KItem_K» (x0 : SortK) : SortKItem
    | «#loopStep(_,_)_MPY-CONTROLS_KItem_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortKItem
    | «#mathCeil_MPY-FLOAT_KItem» : SortKItem
    | «#mathFloor_MPY-FLOAT_KItem» : SortKItem
    | «#mathPow1(_)_MPY-FLOAT_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «#mathPow2(_)_MPY-FLOAT_KItem_Val» (x0 : SortVal) : SortKItem
    | «#mathSqrt_MPY-FLOAT_KItem» : SortKItem
    | «#maxAcc(_,_)_MPY-BUILTINS_KItem_Iterable_Int» (x0 : SortIterable) (x1 : SortInt) : SortKItem
    | «#maxAcc0(_)_MPY-BUILTINS_KItem_Iterable» (x0 : SortIterable) : SortKItem
    | «#maxAccF(_,_)_MPY-FLOAT_KItem_Iterable_Float» (x0 : SortIterable) (x1 : SortFloat) : SortKItem
    | «#maxCont(_)_MPY-BUILTINS_KItem_Int» (x0 : SortInt) : SortKItem
    | «#maxCont0_MPY-BUILTINS_KItem» : SortKItem
    | «#maxContF(_)_MPY-FLOAT_KItem_Float» (x0 : SortFloat) : SortKItem
    | «#md5_MPY-BUILTINS_KItem» : SortKItem
    | «#memberAcc(_,_)_MPY-LIST_KItem_Val_Iterable» (x0 : SortVal) (x1 : SortIterable) : SortKItem
    | «#memberCont(_)_MPY-LIST_KItem_Val» (x0 : SortVal) : SortKItem
    | «#minAcc(_,_)_MPY-BUILTINS_KItem_Iterable_Int» (x0 : SortIterable) (x1 : SortInt) : SortKItem
    | «#minAcc0(_)_MPY-BUILTINS_KItem_Iterable» (x0 : SortIterable) : SortKItem
    | «#minAccF(_,_)_MPY-FLOAT_KItem_Iterable_Float» (x0 : SortIterable) (x1 : SortFloat) : SortKItem
    | «#minCont(_)_MPY-BUILTINS_KItem_Int» (x0 : SortInt) : SortKItem
    | «#minCont0_MPY-BUILTINS_KItem» : SortKItem
    | «#minContF(_)_MPY-FLOAT_KItem_Float» (x0 : SortFloat) : SortKItem
    | «#mkClosure(_,_,_,_,_,_)_MPY-FUNCTIONS_KItem_String_ParamNames_ParamNames_ParamNames_Stmts_Map» (x0 : SortString) (x1 : SortParamNames) (x2 : SortParamNames) (x3 : SortParamNames) (x4 : SortStmts) (x5 : SortMap) : SortKItem
    | «#mkLambda(_,_,_,_,_)_MPY-FUNCTIONS_KItem_ParamNames_ParamNames_ParamNames_Stmts_Map» (x0 : SortParamNames) (x1 : SortParamNames) (x2 : SortParamNames) (x3 : SortStmts) (x4 : SortMap) : SortKItem
    | «#notB_MPY-LIST_KItem» : SortKItem
    | «#pop_MPY-FUNCTIONS_KItem» : SortKItem
    | «#slHi(_,_,_)_MPY-SUBSCRIPT_KItem_Val_OptInt_Bound» (x0 : SortVal) (x1 : SortOptInt) (x2 : SortBound) : SortKItem
    | «#slLo(_,_,_)_MPY-SUBSCRIPT_KItem_Val_Bound_Bound» (x0 : SortVal) (x1 : SortBound) (x2 : SortBound) : SortKItem
    | «#slStep(_,_,_)_MPY-SUBSCRIPT_KItem_Val_OptInt_OptInt» (x0 : SortVal) (x1 : SortOptInt) (x2 : SortOptInt) : SortKItem
    | «#sumAcc(_,_)_MPY-BUILTINS_KItem_Iterable_Int» (x0 : SortIterable) (x1 : SortInt) : SortKItem
    | «#sumAccF(_,_)_MPY-FLOAT_KItem_Iterable_Float» (x0 : SortIterable) (x1 : SortFloat) : SortKItem
    | «#sumCont(_)_MPY-BUILTINS_KItem_Int» (x0 : SortInt) : SortKItem
    | «#sumContF(_)_MPY-FLOAT_KItem_Float» (x0 : SortFloat) : SortKItem
    | «#toSome_MPY-SUBSCRIPT_KItem» : SortKItem
    | «#unpackSeq(_,_)_MPY-TUPLE_KItem_Exprs_ValSeq» (x0 : SortExprs) (x1 : SortValSeq) : SortKItem
    | «#while(_,_)_MPY-CONTROLS_KItem_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortKItem
    | «#whileCond(_,_)_MPY-CONTROLS_KItem_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortKItem
    | «frame(_,_,_)_MPY-FUNCTIONS_KItem_K_Int_Int» (x0 : SortK) (x1 : SortInt) (x2 : SortInt) : SortKItem

  structure SortList : Type where
    coll : List SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  inductive SortModule : Type where
    | «Module(_)_MPY-SYNTAX_Module_Stmts» (x0 : SortStmts) : SortModule

  structure SortRetCell : Type where
    val : SortRetState

  inductive SortRetState : Type where
    | «noRet_MPY-CORE_RetState» : SortRetState
    | «retV(_)_MPY-CORE_RetState_Val» (x0 : SortVal) : SortRetState

  structure SortScopesCell : Type where
    val : SortMap

  structure SortStackCell : Type where
    val : SortList

  inductive SortStmt : Type where
    | «Assert(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (x0 : SortExpr) (x1 : SortString) (x2 : SortExpr) : SortStmt
    | «Break_MPY-SYNTAX_Stmt» : SortStmt
    | «Continue_MPY-SYNTAX_Stmt» : SortStmt
    | «Expr(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt
    | «For(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortStmts) : SortStmt
    | «FuncDef(_,_,_,_,_)_MPY-SYNTAX_Stmt_String_Params_CellVars_FreeVars_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortCellVars) (x3 : SortFreeVars) (x4 : SortStmts) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | «Import(_)_MPY-SYNTAX_Stmt_String» (x0 : SortString) : SortStmt
    | «ImportFrom(_,_)_MPY-SYNTAX_Stmt_String_ParamNames» (x0 : SortString) (x1 : SortParamNames) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt
    | «While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts

  inductive SortVal : Type where
    | inj_SortBool (x : SortBool) : SortVal
    | inj_SortFloat (x : SortFloat) : SortVal
    | inj_SortInt (x : SortInt) : SortVal
    | inj_SortIterable (x : SortIterable) : SortVal
    | inj_SortStr (x : SortStr) : SortVal
    | «boundMethodV(_,_)_MPY-CORE_Val_Val_String» (x0 : SortVal) (x1 : SortString) : SortVal
    | «builtinV(_)_MPY-CORE_Val_String» (x0 : SortString) : SortVal
    | «cellRef(_)_MPY-CORE_Val_Int» (x0 : SortInt) : SortVal
    | «cellsMark(_)_MPY-CORE_Val_ParamNames» (x0 : SortParamNames) : SortVal
    | «closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int» (x0 : SortParamNames) (x1 : SortStmts) (x2 : SortInt) : SortVal
    | «closureValC(_,_,_,_)_MPY-FUNCTIONS_Val_ParamNames_ParamNames_Stmts_Map» (x0 : SortParamNames) (x1 : SortParamNames) (x2 : SortStmts) (x3 : SortMap) : SortVal
    | «dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : SortVal
    | «kwV(_,_)_MPY-CORE_Val_String_Val» (x0 : SortString) (x1 : SortVal) : SortVal
    | «md5Obj(_)_MPY-BUILTINS_Val_IntSeq» (x0 : SortIntSeq) : SortVal
    | «noneV_MPY-CORE_Val» : SortVal
    | «ref(_)_MPY-CORE_Val_Int» (x0 : SortInt) : SortVal
    | «setV(_)_MPY-SET_Val_IntSeq» (x0 : SortIntSeq) : SortVal
    | «typeV(_)_MPY-CORE_Val_String» (x0 : SortString) : SortVal

  inductive SortValSeq : Type where
    | «.ValSeq_MPY-CORE_ValSeq» : SortValSeq
    | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (x0 : SortVal) (x1 : SortValSeq) : SortValSeq

  inductive SortVals : Type where
    | «.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» : SortVals
    | «_,__MPY-CORE_Vals_Val_Vals» (x0 : SortVal) (x1 : SortVals) : SortVals
end