import Klean103RoundedAvg.Inj

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def _f0c90ce : Option SortStmts := some (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "n") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» ">" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "m"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» "-" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "total") (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "n") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "m"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "average") (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "//" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "total") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 2))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "%" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "total") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 2)) (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "%" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "average") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 2)) (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "average") (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "average") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "bin") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "average") SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)))))

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def «roundedAvgBody_ROUNDED-AVG-VERIFICATION_Stmts» : Option SortStmts := _f0c90ce

def _df775df : SortInt → SortInt → Option SortExpr
  | N, M => do
    let _Val0 <- «roundedAvgBody_ROUNDED-AVG-VERIFICATION_Stmts»
    return (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» ((@inj SortVal SortExpr) (SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int» (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "n" (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "m" SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames»)) _Val0 0)) (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» ((@inj SortInt SortExpr) N) (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» ((@inj SortInt SortExpr) M) SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»)))

def «roundedAvgCall(_,_)_ROUNDED-AVG-VERIFICATION_Expr_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortExpr := _df775df x0 x1