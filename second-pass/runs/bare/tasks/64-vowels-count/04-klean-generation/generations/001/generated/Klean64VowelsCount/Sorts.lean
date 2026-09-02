import Klean64VowelsCount.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortPyVal : Type where
  | «boolVal(_)_MPY-SYNTAX_PyVal_Bool» (x0 : SortBool) : SortPyVal
  | «intVal(_)_MPY-SYNTAX_PyVal_Int» (x0 : SortInt) : SortPyVal
  | «strVal(_)_MPY-SYNTAX_PyVal_String» (x0 : SortString) : SortPyVal

mutual
  structure SortEnvCell : Type where
    val : SortMap

  structure SortFunctionsCell : Type where
    val : SortMap

  structure SortGeneratedTopCell : Type where
    py : SortPyCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortList (x : SortList) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortPyCell (x : SortPyCell) : SortKItem
    | inj_SortPyVal (x : SortPyVal) : SortKItem
    | inj_SortStackCell (x : SortStackCell) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#endCall_SEMANTIC_KItem» : SortKItem
    | «#entry(_)_SEMANTIC_KItem_String» (x0 : SortString) : SortKItem
    | «#freezer#compare(_,_,_)_SEMANTIC_Expr_String_PyVal_Expr2_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr1_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr2_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerBoolOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr1_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerCall(_,_)_MPY-SYNTAX_Expr_Expr_Expr1_» (x0 : SortK) : SortKItem
    | «#freezerCompare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp0_» (x0 : SortK) : SortKItem
    | «#freezerIf(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts0_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerReturn(_)_MPY-SYNTAX_Stmt_Expr0_» : SortKItem
    | «#freezerSubscript(_,_)_MPY-SYNTAX_Expr_Expr_Expr0_» (x0 : SortK) : SortKItem
    | «#freezerSubscript(_,_)_MPY-SYNTAX_Expr_Expr_Expr1_» (x0 : SortK) : SortKItem
    | «#freezerSubscript(_,_)_MPY-SYNTAX_Expr_Expr_Slice0_» (x0 : SortK) : SortKItem
    | «#return(_)_SEMANTIC_KItem_PyVal» (x0 : SortPyVal) : SortKItem

  structure SortList : Type where
    coll : List SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortPyCell : Type where
    k : SortKCell
    env : SortEnvCell
    functions : SortFunctionsCell
    stack : SortStackCell

  structure SortStackCell : Type where
    val : SortList
end