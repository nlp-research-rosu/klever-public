import Klean77Iscube.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_String» (x0 : SortString) : SortParams

inductive SortValue : Type where
  | «BoolVal(_)_MPY_Value_Bool» (x0 : SortBool) : SortValue
  | «IntVal(_)_MPY_Value_Int» (x0 : SortInt) : SortValue

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | inj_SortValue (x : SortValue) : SortExpr
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
    | «UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortExpr
end

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | «If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | «Return(_)_MPY-SYNTAX_Stmt_Expr» (x0 : SortExpr) : SortStmt
    | «While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortStmt

  inductive SortStmts : Type where
    | «.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» : SortStmts
    | «___MPY-SYNTAX_Stmts_Stmt_Stmts» (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

mutual
  structure SortEnvCell : Type where
    val : SortMap

  structure SortFunsCell : Type where
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
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortFunsCell (x : SortFunsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortValue (x : SortValue) : SortKItem
    | «#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr1_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerBinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr2_» (x0 : SortK) (x1 : SortK) : SortKItem
    | «#freezerCompare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp0_» (x0 : SortK) : SortKItem
    | «#freezerUnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr1_» (x0 : SortK) : SortKItem
    | «assignTo(_)_MPY_KItem_String» (x0 : SortString) : SortKItem
    | «compareKont(_,_)_MPY_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «exec(_)_MPY_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «ifKont(_,_)_MPY_KItem_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) : SortKItem
    | «invoke(_)_MPY_KItem_Value» (x0 : SortValue) : SortKItem
    | returnKont_MPY_KItem : SortKItem
    | «whileKont(_,_)_MPY_KItem_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortMpyCell : Type where
    k : SortKCell
    funs : SortFunsCell
    env : SortEnvCell
    result : SortResultCell

  structure SortResultCell : Type where
    val : SortK
end