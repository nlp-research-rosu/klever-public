import Klean36FizzBuzz.Prelude

structure SortResultCell : Type where
  val : SortInt

structure SortInputCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Bool(_)_MPY-SYNTAX_Expr_Bool» (x0 : SortBool) : SortExpr
    | «BoolOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
end

mutual
  inductive SortStmt : Type where
    | «Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | «FuncDef(_,Params(_),_)_MPY-SYNTAX_Stmt_String_String_Stmts» (x0 : SortString) (x1 : SortString) (x2 : SortStmts) : SortStmt
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

  structure SortFizzCell : Type where
    k : SortKCell
    input : SortInputCell
    env : SortEnvCell
    result : SortResultCell

  structure SortGeneratedTopCell : Type where
    fizz : SortFizzCell
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
    | inj_SortFizzCell (x : SortFizzCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport2(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem
    | «#kxExport3(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «assignTo(_)_SEMANTIC_KItem_String» (x0 : SortString) : SortKItem
    | «binLeft(_,_)_SEMANTIC_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «binRight(_,_)_SEMANTIC_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «compareLeft(_,_)_SEMANTIC_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «compareRight(_,_)_SEMANTIC_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «ifThenElse(_,_)_SEMANTIC_KItem_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) : SortKItem
    | «orElse(_)_SEMANTIC_KItem_Expr» (x0 : SortExpr) : SortKItem
    | returnValue_SEMANTIC_KItem : SortKItem
    | «whileBody(_,_)_SEMANTIC_KItem_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)
end