import Klean131Digits.Prelude

inductive SortParams : Type where
  | «Params(_)_MPY-SYNTAX_Params_String» (x0 : SortString) : SortParams

structure SortDigitCell : Type where
  val : SortInt

mutual
  inductive SortCmpOp : Type where
    | «CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortExpr : Type where
    | «BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | «Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (x0 : SortExpr) (x1 : SortCmpOp) : SortExpr
    | «Int(_)_MPY-SYNTAX_Expr_Int» (x0 : SortInt) : SortExpr
    | «Name(_)_MPY-SYNTAX_Expr_String» (x0 : SortString) : SortExpr
end

structure SortNCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

structure SortAccCell : Type where
  val : SortInt

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

inductive SortProgram : Type where
  | «Module(_)_MPY-SYNTAX_Program_Stmts» (x0 : SortStmts) : SortProgram

mutual
  structure SortAnswerCell : Type where
    val : SortK

  structure SortGeneratedTopCell : Type where
    mpy : SortMpyCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortAccCell (x : SortAccCell) : SortKItem
    | inj_SortAnswerCell (x : SortAnswerCell) : SortKItem
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortDigitCell (x : SortDigitCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortNCell (x : SortNCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortProgram (x : SortProgram) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#kxExport0(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem
    | «#kxExport1(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem
    | «#kxExport2(_)_VERIFICATION-KLEAN-EXPORT_KItem_Int» (x0 : SortInt) : SortKItem
    | «#kxExport3(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Int_Int» (x0 : SortInt) (x1 : SortInt) : SortKItem
    | «CheckProgram(_,_)_VERIFICATION_KItem_Program_Program» (x0 : SortProgram) (x1 : SortProgram) : SortKItem
    | «Invoke(_,_,_)_MPY-SYNTAX_KItem_Program_String_Int» (x0 : SortProgram) (x1 : SortString) (x2 : SortInt) : SortKItem
    | ProgramsMatch_VERIFICATION_KItem : SortKItem
    | «binLeft(_,_)_MPY-SEMANTICS_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «binRight(_,_)_MPY-SEMANTICS_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «compareLeft(_,_)_MPY-SEMANTICS_KItem_String_Expr» (x0 : SortString) (x1 : SortExpr) : SortKItem
    | «compareRight(_,_)_MPY-SEMANTICS_KItem_String_Int» (x0 : SortString) (x1 : SortInt) : SortKItem
    | «doReturn_MPY-SEMANTICS_KItem» : SortKItem
    | «eval(_)_MPY-SEMANTICS_KItem_Expr» (x0 : SortExpr) : SortKItem
    | «exec(_)_MPY-SEMANTICS_KItem_Stmts» (x0 : SortStmts) : SortKItem
    | «execStmt(_)_MPY-SEMANTICS_KItem_Stmt» (x0 : SortStmt) : SortKItem
    | «ifCont(_,_)_MPY-SEMANTICS_KItem_Stmts_Stmts» (x0 : SortStmts) (x1 : SortStmts) : SortKItem
    | «loop(_,_)_MPY-SEMANTICS_KItem_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortKItem
    | «loopCont(_,_)_MPY-SEMANTICS_KItem_Expr_Stmts» (x0 : SortExpr) (x1 : SortStmts) : SortKItem
    | «write(_)_MPY-SEMANTICS_KItem_String» (x0 : SortString) : SortKItem

  structure SortMpyCell : Type where
    k : SortKCell
    n : SortNCell
    acc : SortAccCell
    digit : SortDigitCell
    answer : SortAnswerCell
end