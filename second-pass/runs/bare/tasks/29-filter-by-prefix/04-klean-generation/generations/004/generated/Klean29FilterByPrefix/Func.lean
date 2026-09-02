import Klean29FilterByPrefix.Inj

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def _6de230d : Option SortStmts := some (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (SortExpr.«Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "string") "startswith") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "«prefix»")) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Expr(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (SortExpr.«Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "result") "append") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "string"))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)

def _3135ea6 : SortStrList → SortString → SortStrList → Option SortStrList
  | SortStrList.«nil_MPY-SYNTAX_StrList», _Gen0, ACC => some ACC
  | _, _, _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.Map» : Option SortMap

def «loopBody()_VERIFICATION_Stmts» : Option SortStmts := _6de230d

def «filterAcc(_,_,_)_VERIFICATION_StrList_StrList_String_StrList» (x0 : SortStrList) (x1 : SortString) (x2 : SortStrList) : Option SortStrList := _3135ea6 x0 x1 x2

def _22d274c : Option SortModule := do
  let _Val0 <- «loopBody()_VERIFICATION_Stmts»
  return (SortModule.«Module(_)_MPY-SYNTAX_Module_Stmts» (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«ImportFrom(_,_)_MPY-SYNTAX_Stmt_String_Strings» "typing" (SortStrings.«_,__MPY-SYNTAX_Strings_String_Strings» "List" SortStrings.«.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings»)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» "filter_by_prefix" (SortParams.«Params(_)_MPY-SYNTAX_Params_Strings» (SortStrings.«_,__MPY-SYNTAX_Strings_String_Strings» "strings" (SortStrings.«_,__MPY-SYNTAX_Strings_String_Strings» "«prefix»" SortStrings.«.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings»))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "result") SortExpr.«ListExpr()_MPY-SYNTAX_Expr») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«For(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "string") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "strings") _Val0) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "result")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)))

def _0523407 : SortStrList → SortString → Option SortStrList
  | INPUT, PREFIX => do
    let _Val0 <- «filterAcc(_,_,_)_VERIFICATION_StrList_StrList_String_StrList» INPUT PREFIX SortStrList.«nil_MPY-SYNTAX_StrList»
    return _Val0

def «solutionProgram()_VERIFICATION_Module» : Option SortModule := _22d274c

def «filterByPrefix(_,_)_VERIFICATION_StrList_StrList_String» (x0 : SortStrList) (x1 : SortString) : Option SortStrList := _0523407 x0 x1