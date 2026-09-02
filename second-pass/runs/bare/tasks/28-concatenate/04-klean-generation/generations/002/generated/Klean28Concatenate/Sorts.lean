import Klean28Concatenate.Prelude

inductive SortPyExpr : Type where
  | «BinOp(_,_,_)_MPY-SYNTAX_PyExpr_String_PyExpr_PyExpr» (x0 : SortString) (x1 : SortPyExpr) (x2 : SortPyExpr) : SortPyExpr
  | «Name(_)_MPY-SYNTAX_PyExpr_String» (x0 : SortString) : SortPyExpr
  | «Str(_)_MPY-SYNTAX_PyExpr_String» (x0 : SortString) : SortPyExpr

inductive SortStrList : Type where
  | «.StrList_MPY-SYNTAX_StrList» : SortStrList
  | «_::__MPY-SYNTAX_StrList_String_StrList» (x0 : SortString) (x1 : SortStrList) : SortStrList

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_String» (x0 : SortString) : SortParams

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortPyVal : Type where
  | «lVal(_)_MPY-SYNTAX_PyVal_StrList» (x0 : SortStrList) : SortPyVal
  | «sVal(_)_MPY-SYNTAX_PyVal_String» (x0 : SortString) : SortPyVal

mutual
  inductive SortPyStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_PyStmt_PyExpr_PyExpr» (x0 : SortPyExpr) (x1 : SortPyExpr) : SortPyStmt
    | «For(_,_,_)_MPY-SYNTAX_PyStmt_PyExpr_PyExpr_PyStmts» (x0 : SortPyExpr) (x1 : SortPyExpr) (x2 : SortPyStmts) : SortPyStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_PyStmt_String_Params_PyStmts» (x0 : SortString) (x1 : SortParams) (x2 : SortPyStmts) : SortPyStmt
    | «ImportFrom(_,_)_MPY-SYNTAX_PyStmt_String_String» (x0 : SortString) (x1 : SortString) : SortPyStmt
    | «Return(_)_MPY-SYNTAX_PyStmt_PyExpr» (x0 : SortPyExpr) : SortPyStmt

  inductive SortPyStmts : Type where
    | «.List{"___MPY-SYNTAX_PyStmts_PyStmt_PyStmts"}_PyStmts» : SortPyStmts
    | «___MPY-SYNTAX_PyStmts_PyStmt_PyStmts» (x0 : SortPyStmt) (x1 : SortPyStmts) : SortPyStmts
end

inductive SortPyProgram : Type where
  | «Module(_)_MPY-SYNTAX_PyProgram_PyStmts» (x0 : SortPyStmts) : SortPyProgram

mutual
  structure SortGeneratedTopCell : Type where
    k : SortKCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPyExpr (x : SortPyExpr) : SortKItem
    | inj_SortPyProgram (x : SortPyProgram) : SortKItem
    | inj_SortPyStmt (x : SortPyStmt) : SortKItem
    | inj_SortPyStmts (x : SortPyStmts) : SortKItem
    | inj_SortPyVal (x : SortPyVal) : SortKItem
    | inj_SortStrList (x : SortStrList) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#kxExport0(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_String_StrList» (x0 : SortString) (x1 : SortStrList) : SortKItem
    | «addLeft(_)_MPY-SYNTAX_KItem_PyExpr» (x0 : SortPyExpr) : SortKItem
    | «addRight(_)_MPY-SYNTAX_KItem_PyVal» (x0 : SortPyVal) : SortKItem
    | «assignTo(_)_MPY-SYNTAX_KItem_String» (x0 : SortString) : SortKItem
    | «bindLoop(_,_)_MPY-SYNTAX_KItem_String_PyVal» (x0 : SortString) (x1 : SortPyVal) : SortKItem
    | «cleanup_MPY-SYNTAX_KItem» : SortKItem
    | «finishReturn_MPY-SYNTAX_KItem» : SortKItem
    | «invoke(_,_)_MPY-SYNTAX_KItem_String_PyVal» (x0 : SortString) (x1 : SortPyVal) : SortKItem
    | «load(_)_MPY-SYNTAX_KItem_PyProgram» (x0 : SortPyProgram) : SortKItem
    | «loop(_,_,_)_MPY-SYNTAX_KItem_String_StrList_PyStmts» (x0 : SortString) (x1 : SortStrList) (x2 : SortPyStmts) : SortKItem
    | «moduleLoaded_MPY-SYNTAX_KItem» : SortKItem
    | «startFor(_,_)_MPY-SYNTAX_KItem_String_PyStmts» (x0 : SortString) (x1 : SortPyStmts) : SortKItem
end