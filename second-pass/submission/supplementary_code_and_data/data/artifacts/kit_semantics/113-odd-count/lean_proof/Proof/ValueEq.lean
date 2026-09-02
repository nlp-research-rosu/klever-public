import Klean113OddCount.Lemmas

namespace Proof.ValueEq

def intSeqStructuralEq : SortIntSeq → SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» ah atail,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» bh btail =>
      ah == bh && intSeqStructuralEq atail btail
  | _, _ => false

def paramNamesStructuralEq : SortParamNames → SortParamNames → Bool
  | SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames»,
      SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames» =>
      true
  | SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» ah atail,
      SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» bh btail =>
      ah == bh && paramNamesStructuralEq atail btail
  | _, _ => false

def strStructuralEq : SortStr → SortStr → Bool
  | SortStr.«str(_)_MPY-CORE_Str_IntSeq» left,
      SortStr.«str(_)_MPY-CORE_Str_IntSeq» right =>
      intSeqStructuralEq left right

def paramsStructuralEq : SortParams → SortParams → Bool
  | SortParams.«Params(_)_MPY-SYNTAX_Params_ParamNames» left,
      SortParams.«Params(_)_MPY-SYNTAX_Params_ParamNames» right =>
      paramNamesStructuralEq left right

def cellVarsStructuralEq : SortCellVars → SortCellVars → Bool
  | SortCellVars.«CellVars(_)_MPY-SYNTAX_CellVars_ParamNames» left,
      SortCellVars.«CellVars(_)_MPY-SYNTAX_CellVars_ParamNames» right =>
      paramNamesStructuralEq left right

def freeVarsStructuralEq : SortFreeVars → SortFreeVars → Bool
  | SortFreeVars.«FreeVars(_)_MPY-SYNTAX_FreeVars_ParamNames» left,
      SortFreeVars.«FreeVars(_)_MPY-SYNTAX_FreeVars_ParamNames» right =>
      paramNamesStructuralEq left right

/- functions.k constructs captured closure maps solely from String keys and
   cellRef values. These cases therefore cover every reachable captured map. -/
def capturedKItemStructuralEq : SortKItem → SortKItem → Bool
  | SortKItem.inj_SortString left, SortKItem.inj_SortString right =>
      left == right
  | SortKItem.inj_SortVal
      (SortVal.«cellRef(_)_MPY-CORE_Val_Int» left),
      SortKItem.inj_SortVal
        (SortVal.«cellRef(_)_MPY-CORE_Val_Int» right) =>
      left == right
  | _, _ => false

def capturedEntriesStructuralEq :
    List (SortKItem × SortKItem) → List (SortKItem × SortKItem) → Bool
  | [], [] => true
  | (lk, lv) :: lt, (rk, rv) :: rt =>
      capturedKItemStructuralEq lk rk &&
        capturedKItemStructuralEq lv rv &&
        capturedEntriesStructuralEq lt rt
  | _, _ => false

def capturedMapStructuralEq : SortMap → SortMap → Bool
  | ⟨left⟩, ⟨right⟩ => capturedEntriesStructuralEq left right

mutual
  def valueStructuralEq : SortVal → SortVal → Bool
    | SortVal.inj_SortBool left, SortVal.inj_SortBool right =>
        left == right
    | SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
        left.toBits == right.toBits
    | SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
        left == right
    | SortVal.inj_SortIterable left, SortVal.inj_SortIterable right =>
        iterableStructuralEq left right
    | SortVal.inj_SortStr left, SortVal.inj_SortStr right =>
        strStructuralEq left right
    | SortVal.«boundMethodV(_,_)_MPY-CORE_Val_Val_String» lv lm,
        SortVal.«boundMethodV(_,_)_MPY-CORE_Val_Val_String» rv rm =>
        valueStructuralEq lv rv && lm == rm
    | SortVal.«builtinV(_)_MPY-CORE_Val_String» left,
        SortVal.«builtinV(_)_MPY-CORE_Val_String» right =>
        left == right
    | SortVal.«cellRef(_)_MPY-CORE_Val_Int» left,
        SortVal.«cellRef(_)_MPY-CORE_Val_Int» right =>
        left == right
    | SortVal.«cellsMark(_)_MPY-CORE_Val_ParamNames» left,
        SortVal.«cellsMark(_)_MPY-CORE_Val_ParamNames» right =>
        paramNamesStructuralEq left right
    | SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int» lp lb li,
        SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int» rp rb ri =>
        paramNamesStructuralEq lp rp && statementsStructuralEq lb rb &&
          li == ri
    | SortVal.«closureValC(_,_,_,_)_MPY-FUNCTIONS_Val_ParamNames_ParamNames_Stmts_Map»
          lp lc lb lm,
        SortVal.«closureValC(_,_,_,_)_MPY-FUNCTIONS_Val_ParamNames_ParamNames_Stmts_Map»
          rp rc rb rm =>
        paramNamesStructuralEq lp rp && paramNamesStructuralEq lc rc &&
          statementsStructuralEq lb rb && capturedMapStructuralEq lm rm
    | SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» lk lv,
        SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» rk rv =>
        valueSequenceStructuralEq lk rk && valueSequenceStructuralEq lv rv
    | SortVal.«kwV(_,_)_MPY-CORE_Val_String_Val» ln lv,
        SortVal.«kwV(_,_)_MPY-CORE_Val_String_Val» rn rv =>
        ln == rn && valueStructuralEq lv rv
    | SortVal.«md5Obj(_)_MPY-BUILTINS_Val_IntSeq» left,
        SortVal.«md5Obj(_)_MPY-BUILTINS_Val_IntSeq» right =>
        intSeqStructuralEq left right
    | SortVal.«noneV_MPY-CORE_Val», SortVal.«noneV_MPY-CORE_Val» =>
        true
    | SortVal.«ref(_)_MPY-CORE_Val_Int» left,
        SortVal.«ref(_)_MPY-CORE_Val_Int» right =>
        left == right
    | SortVal.«setV(_)_MPY-SET_Val_IntSeq» left,
        SortVal.«setV(_)_MPY-SET_Val_IntSeq» right =>
        intSeqStructuralEq left right
    | SortVal.«typeV(_)_MPY-CORE_Val_String» left,
        SortVal.«typeV(_)_MPY-CORE_Val_String» right =>
        left == right
    | _, _ => false
  termination_by structural left _ => left

  def valueSequenceStructuralEq : SortValSeq → SortValSeq → Bool
    | SortValSeq.«.ValSeq_MPY-CORE_ValSeq»,
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => true
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» lh lt,
        SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» rh rt =>
        valueStructuralEq lh rh && valueSequenceStructuralEq lt rt
    | _, _ => false
  termination_by structural left _ => left

  def iterableStructuralEq : SortIterable → SortIterable → Bool
    | SortIterable.inj_SortStr left, SortIterable.inj_SortStr right =>
        strStructuralEq left right
    | SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» left,
        SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» right =>
        valueSequenceStructuralEq left right
    | SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» la lb lc,
        SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» ra rb rc =>
        la == ra && lb == rb && lc == rc
    | SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» left,
        SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» right =>
        valueSequenceStructuralEq left right
    | SortIterable.«zipObj(_,_)_MPY-CORE_Iterable_ValSeq_ValSeq» la lb,
        SortIterable.«zipObj(_,_)_MPY-CORE_Iterable_ValSeq_ValSeq» ra rb =>
        valueSequenceStructuralEq la ra && valueSequenceStructuralEq lb rb
    | SortIterable.«zipObjS(_,_)_MPY-CORE_Iterable_IntSeq_IntSeq» la lb,
        SortIterable.«zipObjS(_,_)_MPY-CORE_Iterable_IntSeq_IntSeq» ra rb =>
        intSeqStructuralEq la ra && intSeqStructuralEq lb rb
    | _, _ => false
  termination_by structural left _ => left

  def statementsStructuralEq : SortStmts → SortStmts → Bool
    | SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»,
        SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» => true
    | SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» lh lt,
        SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» rh rt =>
        statementStructuralEq lh rh && statementsStructuralEq lt rt
    | _, _ => false
  termination_by structural left _ => left

  def statementStructuralEq : SortStmt → SortStmt → Bool
    | SortStmt.«Assert(_)_MPY-SYNTAX_Stmt_Expr» left,
        SortStmt.«Assert(_)_MPY-SYNTAX_Stmt_Expr» right =>
        expressionStructuralEq left right
    | SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» la lb,
        SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» ra rb =>
        expressionStructuralEq la ra && expressionStructuralEq lb rb
    | SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» la lo lb,
        SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» ra ro rb =>
        expressionStructuralEq la ra && lo == ro &&
          expressionStructuralEq lb rb
    | SortStmt.«Break_MPY-SYNTAX_Stmt», SortStmt.«Break_MPY-SYNTAX_Stmt» =>
        true
    | SortStmt.«Continue_MPY-SYNTAX_Stmt»,
        SortStmt.«Continue_MPY-SYNTAX_Stmt» => true
    | SortStmt.«Expr(_)_MPY-SYNTAX_Stmt_Expr» left,
        SortStmt.«Expr(_)_MPY-SYNTAX_Stmt_Expr» right =>
        expressionStructuralEq left right
    | SortStmt.«For(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts» la lb lc,
        SortStmt.«For(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts» ra rb rc =>
        expressionStructuralEq la ra && expressionStructuralEq lb rb &&
          statementsStructuralEq lc rc
    | SortStmt.«FuncDef(_,_,_,_,_)_MPY-SYNTAX_Stmt_String_Params_CellVars_FreeVars_Stmts»
          ln lp lc lf lb,
        SortStmt.«FuncDef(_,_,_,_,_)_MPY-SYNTAX_Stmt_String_Params_CellVars_FreeVars_Stmts»
          rn rp rc rf rb =>
        ln == rn && paramsStructuralEq lp rp && cellVarsStructuralEq lc rc &&
          freeVarsStructuralEq lf rf && statementsStructuralEq lb rb
    | SortStmt.«FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» ln lp lb,
        SortStmt.«FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» rn rp rb =>
        ln == rn && paramsStructuralEq lp rp && statementsStructuralEq lb rb
    | SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» lc lt le,
        SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» rc rt re =>
        expressionStructuralEq lc rc && statementsStructuralEq lt rt &&
          statementsStructuralEq le re
    | SortStmt.«Import(_)_MPY-SYNTAX_Stmt_String» left,
        SortStmt.«Import(_)_MPY-SYNTAX_Stmt_String» right =>
        left == right
    | SortStmt.«ImportFrom(_,_)_MPY-SYNTAX_Stmt_String_ParamNames» lm lp,
        SortStmt.«ImportFrom(_,_)_MPY-SYNTAX_Stmt_String_ParamNames» rm rp =>
        lm == rm && paramNamesStructuralEq lp rp
    | SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» left,
        SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» right =>
        expressionStructuralEq left right
    | SortStmt.«While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» lc lb,
        SortStmt.«While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» rc rb =>
        expressionStructuralEq lc rc && statementsStructuralEq lb rb
    | _, _ => false
  termination_by structural left _ => left

  def expressionStructuralEq : SortExpr → SortExpr → Bool
    | SortExpr.inj_SortBool left, SortExpr.inj_SortBool right =>
        left == right
    | SortExpr.inj_SortFloat left, SortExpr.inj_SortFloat right =>
        left.toBits == right.toBits
    | SortExpr.inj_SortInt left, SortExpr.inj_SortInt right =>
        left == right
    | SortExpr.inj_SortIterable left, SortExpr.inj_SortIterable right =>
        iterableStructuralEq left right
    | SortExpr.inj_SortStr left, SortExpr.inj_SortStr right =>
        strStructuralEq left right
    | SortExpr.inj_SortVal left, SortExpr.inj_SortVal right =>
        valueStructuralEq left right
    | SortExpr.«Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» le ln,
        SortExpr.«Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» re rn =>
        expressionStructuralEq le re && ln == rn
    | SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» lo la lb,
        SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» ro ra rb =>
        lo == ro && expressionStructuralEq la ra &&
          expressionStructuralEq lb rb
    | SortExpr.«Bool(_)_MPY-SYNTAX_Expr_Bool» left,
        SortExpr.«Bool(_)_MPY-SYNTAX_Expr_Bool» right =>
        left == right
    | SortExpr.«BoolOp(_,_)_MPY-SYNTAX_Expr_String_Exprs» lo la,
        SortExpr.«BoolOp(_,_)_MPY-SYNTAX_Expr_String_Exprs» ro ra =>
        lo == ro && expressionsStructuralEq la ra
    | SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» lf la,
        SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» rf ra =>
        expressionStructuralEq lf rf && expressionsStructuralEq la ra
    | SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» le lc,
        SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» re rc =>
        expressionStructuralEq le re && comparisonOpStructuralEq lc rc
    | SortExpr.«DictExpr(_)_MPY-SYNTAX_Expr_Entries» left,
        SortExpr.«DictExpr(_)_MPY-SYNTAX_Expr_Entries» right =>
        entriesStructuralEq left right
    | SortExpr.«Float(_)_MPY-SYNTAX_Expr_Float» left,
        SortExpr.«Float(_)_MPY-SYNTAX_Expr_Float» right =>
        left.toBits == right.toBits
    | SortExpr.«IfExp(_,_,_)_MPY-SYNTAX_Expr_Expr_Expr_Expr» lc lt le,
        SortExpr.«IfExp(_,_,_)_MPY-SYNTAX_Expr_Expr_Expr_Expr» rc rt re =>
        expressionStructuralEq lc rc && expressionStructuralEq lt rt &&
          expressionStructuralEq le re
    | SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» left,
        SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» right =>
        left == right
    | SortExpr.«KwArg(_,_)_MPY-SYNTAX_Expr_String_Expr» ln lv,
        SortExpr.«KwArg(_,_)_MPY-SYNTAX_Expr_String_Expr» rn rv =>
        ln == rn && expressionStructuralEq lv rv
    | SortExpr.«Lambda(_,_,_,_)_MPY-SYNTAX_Expr_Params_CellVars_FreeVars_Expr»
          lp lc lf lb,
        SortExpr.«Lambda(_,_,_,_)_MPY-SYNTAX_Expr_Params_CellVars_FreeVars_Expr»
          rp rc rf rb =>
        paramsStructuralEq lp rp && cellVarsStructuralEq lc rc &&
          freeVarsStructuralEq lf rf && expressionStructuralEq lb rb
    | SortExpr.«Lambda(_,_)_MPY-SYNTAX_Expr_Params_Expr» lp lb,
        SortExpr.«Lambda(_,_)_MPY-SYNTAX_Expr_Params_Expr» rp rb =>
        paramsStructuralEq lp rp && expressionStructuralEq lb rb
    | SortExpr.«ListExpr(_)_MPY-SYNTAX_Expr_Exprs» left,
        SortExpr.«ListExpr(_)_MPY-SYNTAX_Expr_Exprs» right =>
        expressionsStructuralEq left right
    | SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» left,
        SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» right =>
        left == right
    | SortExpr.«NoneVal_MPY-SYNTAX_Expr», SortExpr.«NoneVal_MPY-SYNTAX_Expr» =>
        true
    | SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» left,
        SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» right =>
        left == right
    | SortExpr.«Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» le li,
        SortExpr.«Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» re ri =>
        expressionStructuralEq le re && indexStructuralEq li ri
    | SortExpr.«TupleExpr(_)_MPY-SYNTAX_Expr_Exprs» left,
        SortExpr.«TupleExpr(_)_MPY-SYNTAX_Expr_Exprs» right =>
        expressionsStructuralEq left right
    | SortExpr.«UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» lo le,
        SortExpr.«UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» ro re =>
        lo == ro && expressionStructuralEq le re
    | SortExpr.«closureExpr(_,_)_MPY-FUNCTIONS_Expr_ParamNames_Stmts» lp lb,
        SortExpr.«closureExpr(_,_)_MPY-FUNCTIONS_Expr_ParamNames_Stmts» rp rb =>
        paramNamesStructuralEq lp rp && statementsStructuralEq lb rb
    | _, _ => false
  termination_by structural left _ => left

  def expressionsStructuralEq : SortExprs → SortExprs → Bool
    | SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»,
        SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs» => true
    | SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» lh lt,
        SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» rh rt =>
        expressionStructuralEq lh rh && expressionsStructuralEq lt rt
    | _, _ => false
  termination_by structural left _ => left

  def comparisonOpStructuralEq : SortCmpOp → SortCmpOp → Bool
    | SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» lo le,
        SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» ro re =>
        lo == ro && expressionStructuralEq le re
  termination_by structural left _ => left

  def entriesStructuralEq : SortEntries → SortEntries → Bool
    | SortEntries.«.List{"_,__MPY-SYNTAX_Entries_Entry_Entries"}_Entries»,
        SortEntries.«.List{"_,__MPY-SYNTAX_Entries_Entry_Entries"}_Entries» =>
        true
    | SortEntries.«_,__MPY-SYNTAX_Entries_Entry_Entries» lh lt,
        SortEntries.«_,__MPY-SYNTAX_Entries_Entry_Entries» rh rt =>
        entryStructuralEq lh rh && entriesStructuralEq lt rt
    | _, _ => false
  termination_by structural left _ => left

  def entryStructuralEq : SortEntry → SortEntry → Bool
    | SortEntry.«Entry(_,_)_MPY-SYNTAX_Entry_Expr_Expr» lk lv,
        SortEntry.«Entry(_,_)_MPY-SYNTAX_Entry_Expr_Expr» rk rv =>
        expressionStructuralEq lk rk && expressionStructuralEq lv rv
  termination_by structural left _ => left

  def indexStructuralEq : SortIndex → SortIndex → Bool
    | SortIndex.inj_SortBool left, SortIndex.inj_SortBool right =>
        left == right
    | SortIndex.inj_SortExpr left, SortIndex.inj_SortExpr right =>
        expressionStructuralEq left right
    | SortIndex.inj_SortFloat left, SortIndex.inj_SortFloat right =>
        left.toBits == right.toBits
    | SortIndex.inj_SortInt left, SortIndex.inj_SortInt right =>
        left == right
    | SortIndex.inj_SortIterable left, SortIndex.inj_SortIterable right =>
        iterableStructuralEq left right
    | SortIndex.inj_SortStr left, SortIndex.inj_SortStr right =>
        strStructuralEq left right
    | SortIndex.inj_SortVal left, SortIndex.inj_SortVal right =>
        valueStructuralEq left right
    | SortIndex.«Slice(_,_,_)_MPY-SYNTAX_Index_Bound_Bound_Bound» la lb lc,
        SortIndex.«Slice(_,_,_)_MPY-SYNTAX_Index_Bound_Bound_Bound» ra rb rc =>
        boundStructuralEq la ra && boundStructuralEq lb rb &&
          boundStructuralEq lc rc
    | _, _ => false
  termination_by structural left _ => left

  def boundStructuralEq : SortBound → SortBound → Bool
    | SortBound.inj_SortBool left, SortBound.inj_SortBool right =>
        left == right
    | SortBound.inj_SortExpr left, SortBound.inj_SortExpr right =>
        expressionStructuralEq left right
    | SortBound.inj_SortFloat left, SortBound.inj_SortFloat right =>
        left.toBits == right.toBits
    | SortBound.inj_SortInt left, SortBound.inj_SortInt right =>
        left == right
    | SortBound.inj_SortIterable left, SortBound.inj_SortIterable right =>
        iterableStructuralEq left right
    | SortBound.inj_SortStr left, SortBound.inj_SortStr right =>
        strStructuralEq left right
    | SortBound.inj_SortVal left, SortBound.inj_SortVal right =>
        valueStructuralEq left right
    | SortBound.«NoBound_MPY-SYNTAX_Bound»,
        SortBound.«NoBound_MPY-SYNTAX_Bound» => true
    | _, _ => false
  termination_by structural left _ => left
end

end Proof.ValueEq
