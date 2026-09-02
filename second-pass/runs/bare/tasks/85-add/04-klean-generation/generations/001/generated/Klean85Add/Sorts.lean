import Klean85Add.Prelude

mutual
  inductive SortBound : Type where
    | inj_SortExpr (x : SortExpr) : SortBound
    | «NoBound_MPY-SYNTAX_Bound» : SortBound

  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Call(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «IfExp(_,_,_)_MPY-SYNTAX_Expr_Expr_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (x0 : SortExpr) (x1 : SortIndex) : SortExpr

  inductive SortIndex : Type where
    | inj_SortExpr (x : SortExpr) : SortIndex
    | «Slice(_,_,_)_MPY-SYNTAX_Index_Bound_Bound_Bound» (x0 : SortBound) (x1 : SortBound) (x2 : SortBound) : SortIndex
end

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortISeq : Type where
  | «cons(_,_)_MPY-SYNTAX_ISeq_Int_ISeq» (x0 : SortInt) (x1 : SortISeq) : SortISeq
  | «nil_MPY-SYNTAX_ISeq» : SortISeq

inductive SortPyVal : Type where
  | «pyBool(_)_MPY-SYNTAX_PyVal_Bool» (x0 : SortBool) : SortPyVal
  | «pyInt(_)_MPY-SYNTAX_PyVal_Int» (x0 : SortInt) : SortPyVal
  | «pyList(_)_MPY-SYNTAX_PyVal_ISeq» (x0 : SortISeq) : SortPyVal

structure SortInputCell : Type where
  val : SortPyVal

mutual
  structure SortCallStackCell : Type where
    val : SortList

  structure SortEnvCell : Type where
    val : SortMap

  structure SortFunctionsCell : Type where
    val : SortMap

  structure SortGeneratedTopCell : Type where
    mpy : SortMpyCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortBound (x : SortBound) : SortKItem
    | inj_SortCallStackCell (x : SortCallStackCell) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortISeq (x : SortISeq) : SortKItem
    | inj_SortIndex (x : SortIndex) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortList (x : SortList) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortPyVal (x : SortPyVal) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_ISeq» (x0 : SortISeq) : SortKItem
    | «binApply(_,_)_MPY_KItem_String_PyVal» (x0 : SortString) (x1 : SortPyVal) : SortKItem
    | «binRight(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | builtInLen_MPY_KItem : SortKItem
    | «cmpApply(_,_)_MPY_KItem_String_PyVal» (x0 : SortString) (x1 : SortPyVal) : SortKItem
    | «cmpRight(_,_)_MPY_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | done_MPY_KItem : SortKItem
    | «eval(_)_MPY_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «indexAt(_)_MPY_KItem_Int» (x0 : SortInt) : SortKItem
    | isShortList_MPY_KItem : SortKItem
    | keepIfEven_MPY_KItem : SortKItem
    | restoreCaller_MPY_KItem : SortKItem
    | «select(_,_)_MPY_KItem_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortKItem
    | «sliceFrom(_)_MPY_KItem_Int» (x0 : SortInt) : SortKItem
    | start_MPY_KItem : SortKItem
    | «userCall(_)_MPY_KItem_String» (x0 : SortString) : SortKItem

  structure SortList : Type where
    coll : List SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    input : SortInputCell
    functions : SortFunctionsCell
    env : SortEnvCell
    callStack : SortCallStackCell
end