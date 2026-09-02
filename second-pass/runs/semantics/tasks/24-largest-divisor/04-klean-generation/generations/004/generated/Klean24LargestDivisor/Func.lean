import Klean24LargestDivisor.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def _f7caa22 : Option SortStmts := some (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Expr(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "Return the largest positive divisor of n that is smaller than n.")) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "divisor") (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "-" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "n") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "%" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "n") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "divisor")) (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "!=" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 0))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "divisor") "-" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "divisor")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))))

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def «largestDivisorBody()_VERIFICATION_Stmts» : Option SortStmts := _f7caa22

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def _b7eb23b : SortInt → SortInt → Option SortInt
  | N, D => do
    let _Val0 <- «_>Int_» D 0
    let _Val1 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» N D
    let _Val2 <- «_==Int_» _Val1 0
    let _Val3 <- _andBool_ _Val0 _Val2
    guard _Val3
    return D

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

axiom _9a654f1 : SortInt → SortInt → Option SortInt
axiom «firstDivisorAtOrBelow(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt

noncomputable def _3f7185d : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_-Int_» N 1
    let _Val1 <- «firstDivisorAtOrBelow(_,_)_VERIFICATION_Int_Int_Int» N _Val0
    return _Val1

noncomputable def «largestProperDivisor(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _3f7185d x0