import Klean15StringSequence.Inj

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

def _da8f12a : Option SortStmts := some (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "result") (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "result") (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» " ")) (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "str") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "i")))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "i") (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "i") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))

axiom «Int2String(_)_STRING-COMMON_String_Int» (x0 : SortInt) : Option SortString

axiom «_+String__STRING-COMMON_String_String_String» (x0 : SortString) (x1 : SortString) : Option SortString

axiom «.List» : Option SortList

def _a003e4a : Option SortExpr := some (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "i") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<=" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "n")))

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.Map» : Option SortMap

def _ff523b6 : SortInt → Option SortString
  | N => do
    let _Val0 <- «_<Int_» N 0
    guard _Val0
    return ""

def «loopBody()_VERIFICATION_Stmts» : Option SortStmts := _da8f12a

def _fb23a80 : SortInt → SortInt → Option SortInt
  | I, N => do
    let _Val0 <- «_>Int_» I N
    guard _Val0
    return I

def _283ac0f : SortInt → SortInt → SortString → Option SortString
  | I, N, S => do
    let _Val0 <- «_>Int_» I N
    guard _Val0
    return S

def «loopCondition()_VERIFICATION_Expr» : Option SortExpr := _a003e4a

axiom _6e9cc10 : SortInt → SortInt → Option SortInt
axiom «indexAfter(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt

axiom «sequenceFrom(_,_,_)_VERIFICATION_String_Int_Int_String» (x0 : SortInt) (x1 : SortInt) (x2 : SortString) : Option SortString
axiom _d0f8f3d : SortInt → SortInt → SortString → Option SortString

def _ed219ec : Option SortStmts := do
  let _Val0 <- «loopCondition()_VERIFICATION_Expr»
  let _Val1 <- «loopBody()_VERIFICATION_Stmts»
  return (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "n") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 0))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "result") (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "0")) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "i") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» _Val0 _Val1) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "result")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)))))

noncomputable def _dfded0e : SortInt → Option SortString
  | N => do
    let _Val0 <- «_>=Int_» N 0
    let _Val1 <- «sequenceFrom(_,_,_)_VERIFICATION_String_Int_Int_String» 1 N "0"
    guard _Val0
    return _Val1

def «targetBody()_VERIFICATION_Stmts» : Option SortStmts := _ed219ec

noncomputable def «sequence(_)_VERIFICATION_String_Int» (x0 : SortInt) : Option SortString := (_dfded0e x0) <|> (_ff523b6 x0)

def _f95812e : Option SortFunction := do
  let _Val0 <- «targetBody()_VERIFICATION_Stmts»
  return (SortFunction.«function(_,_)_MPY_Function_String_Stmts» "n" _Val0)

def _c7a9d9c : Option SortModule := do
  let _Val0 <- «targetBody()_VERIFICATION_Stmts»
  return (SortModule.«Module(_)_MPY-SYNTAX_Module_Stmts» (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» "string_sequence" (SortParams.«Params(_)_MPY-SYNTAX_Params_String» "n") _Val0) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))

def «targetFunction()_VERIFICATION_Function» : Option SortFunction := _f95812e

def «targetProgram()_VERIFICATION_Module» : Option SortModule := _c7a9d9c