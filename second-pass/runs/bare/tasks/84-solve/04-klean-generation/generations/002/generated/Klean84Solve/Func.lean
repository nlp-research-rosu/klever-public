import Klean84Solve.Inj

def _8f4b766 : SortExpr → SortString → SortInt → Option SortValue
  | SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» X, _Uniq0, N => match X == _Uniq0 with
    | true => some (SortValue.«VInt(_)_MPY-SEMANTIC_Value_Int» N)
    | _ => none
  | _, _, _ => none

def _808f518 : SortExpr → SortString → SortInt → Option SortValue
  | SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» I, _Gen0, _Gen1 => some (SortValue.«VInt(_)_MPY-SEMANTIC_Value_Int» I)
  | _, _, _ => none

def _5a33d6f : SortValue → Option SortInt
  | SortValue.«VInt(_)_MPY-SEMANTIC_Value_Int» I => some I
  | _ => none

def _8c831ad : SortExpr → SortString → SortInt → Option SortValue
  | SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» S, _Gen0, _Gen1 => some (SortValue.«VStr(_)_MPY-SEMANTIC_Value_String» S)
  | _, _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _4291191 : SortInt → Option SortValue
  | 0 => some (SortValue.«VStr(_)_MPY-SEMANTIC_Value_String» "0")
  | _ => none

def _bf05fd2 : SortInt → SortInt → Option SortBool
  | LIMIT, _Uniq0 => match LIMIT == _Uniq0 with
    | true => some true
    | _ => none

axiom «_+String__STRING-COMMON_String_String_String» (x0 : SortString) (x1 : SortString) : Option SortString

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

def _a47c5e9 : SortInt → Option SortValue
  | 1 => some (SortValue.«VStr(_)_MPY-SEMANTIC_Value_String» "1")
  | _ => none

def «getInt(_)_MPY-SEMANTIC_Int_Value» (x0 : SortValue) : Option SortInt := _5a33d6f x0

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _fde9a69 : SortValue → SortInt → Option SortValue
  | SortValue.«VStr(_)_MPY-SEMANTIC_Value_String» S, 0 => do
    let _Val0 <- «_+String__STRING-COMMON_String_String_String» S "0"
    return (SortValue.«VStr(_)_MPY-SEMANTIC_Value_String» _Val0)
  | _, _ => none

noncomputable def _3be8a6e : SortValue → SortInt → Option SortValue
  | SortValue.«VStr(_)_MPY-SEMANTIC_Value_String» S, 1 => do
    let _Val0 <- «_+String__STRING-COMMON_String_String_String» S "1"
    return (SortValue.«VStr(_)_MPY-SEMANTIC_Value_String» _Val0)
  | _, _ => none

noncomputable def _4b0aa40 : SortValue → SortValue → Option SortBool
  | SortValue.«VStr(_)_MPY-SEMANTIC_Value_String» S1, SortValue.«VStr(_)_MPY-SEMANTIC_Value_String» S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    return _Val0
  | _, _ => none

mutual
  noncomputable def _07b982c : SortExpr → SortString → SortInt → Option SortValue
    | SortExpr.«Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (SortExpr.«TupleExpr(_)_MPY-SYNTAX_Expr_NeExprs» ES) E2, X, N => do
      let _Val0 <- «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» E2 X N
      let _Val1 <- «getInt(_)_MPY-SEMANTIC_Int_Value» _Val0
      let _Val2 <- «evalNthExpr(_,_,_,_)_MPY-SEMANTIC_Value_NeExprs_Int_String_Int» ES _Val1 X N
      return _Val2
    | _, _, _ => none

  noncomputable def _09eb096 : SortNeExprs → SortString → SortInt → Option SortVList
    | SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» E ES, X, N => do
      let _Val0 <- «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» E X N
      let _Val1 <- «evalExprs(_,_,_)_MPY-SEMANTIC_VList_NeExprs_String_Int» ES X N
      return (SortVList.«VCons(_,_)_MPY-SEMANTIC_VList_Value_VList» _Val0 _Val1)
    | _, _, _ => none

  noncomputable def _2415f27 : SortExpr → SortString → SortInt → Option SortValue
    | SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "//" E1 E2, X, N => do
      let _Val0 <- «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» E1 X N
      let _Val1 <- «getInt(_)_MPY-SEMANTIC_Int_Value» _Val0
      let _Val2 <- «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» E2 X N
      let _Val3 <- «getInt(_)_MPY-SEMANTIC_Int_Value» _Val2
      let _Val4 <- «_/Int_» _Val1 _Val3
      return (SortValue.«VInt(_)_MPY-SEMANTIC_Value_Int» _Val4)
    | _, _, _ => none

  noncomputable def _37de231 : SortNeExprs → SortInt → SortString → SortInt → Option SortValue
    | SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» _Gen0 ES, I, X, N => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «evalNthExpr(_,_,_,_)_MPY-SEMANTIC_Value_NeExprs_Int_String_Int» ES _Val1 X N
      guard _Val0
      return _Val2
    | _, _, _, _ => none

  noncomputable def _55526b2 : SortExpr → SortString → SortInt → Option SortValue
    | SortExpr.«TupleExpr(_)_MPY-SYNTAX_Expr_NeExprs» ES, X, N => do
      let _Val0 <- «evalExprs(_,_,_)_MPY-SEMANTIC_VList_NeExprs_String_Int» ES X N
      return (SortValue.«VTuple(_)_MPY-SEMANTIC_Value_VList» _Val0)
    | _, _, _ => none

  noncomputable def _5d78945 : SortExpr → SortString → SortInt → Option SortValue
    | SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "%" E1 E2, X, N => do
      let _Val0 <- «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» E1 X N
      let _Val1 <- «getInt(_)_MPY-SEMANTIC_Int_Value» _Val0
      let _Val2 <- «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» E2 X N
      let _Val3 <- «getInt(_)_MPY-SEMANTIC_Int_Value» _Val2
      let _Val4 <- «_%Int_» _Val1 _Val3
      return (SortValue.«VInt(_)_MPY-SEMANTIC_Value_Int» _Val4)
    | _, _, _ => none

  noncomputable def _7061ac0 : SortExpr → SortString → SortInt → Option SortValue
    | SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" E1 E2, X, N => do
      let _Val0 <- «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» E1 X N
      let _Val1 <- «getInt(_)_MPY-SEMANTIC_Int_Value» _Val0
      let _Val2 <- «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» E2 X N
      let _Val3 <- «getInt(_)_MPY-SEMANTIC_Int_Value» _Val2
      let _Val4 <- «_+Int_» _Val1 _Val3
      return (SortValue.«VInt(_)_MPY-SEMANTIC_Value_Int» _Val4)
    | _, _, _ => none

  noncomputable def _8e5458b : SortNeExprs → SortInt → SortString → SortInt → Option SortValue
    | SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» E _Gen0, 0, X, N => do
      let _Val0 <- «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» E X N
      return _Val0
    | _, _, _, _ => none

  noncomputable def «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» (x0 : SortExpr) (x1 : SortString) (x2 : SortInt) : Option SortValue := (_07b982c x0 x1 x2) <|> (_2415f27 x0 x1 x2) <|> (_55526b2 x0 x1 x2) <|> (_5d78945 x0 x1 x2) <|> (_7061ac0 x0 x1 x2) <|> (_808f518 x0 x1 x2) <|> (_8c831ad x0 x1 x2) <|> (_8f4b766 x0 x1 x2)

  noncomputable def «evalExprs(_,_,_)_MPY-SEMANTIC_VList_NeExprs_String_Int» (x0 : SortNeExprs) (x1 : SortString) (x2 : SortInt) : Option SortVList := (_09eb096 x0 x1 x2) <|> (_d6c7e7e x0 x1 x2)

  noncomputable def «evalNthExpr(_,_,_,_)_MPY-SEMANTIC_Value_NeExprs_Int_String_Int» (x0 : SortNeExprs) (x1 : SortInt) (x2 : SortString) (x3 : SortInt) : Option SortValue := (_37de231 x0 x1 x2 x3) <|> (_8e5458b x0 x1 x2 x3) <|> (_cb76530 x0 x1 x2 x3)

  noncomputable def _cb76530 : SortNeExprs → SortInt → SortString → SortInt → Option SortValue
    | SortNeExprs.inj_SortExpr E, 0, X, N => do
      let _Val0 <- «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» E X N
      return _Val0
    | _, _, _, _ => none

  noncomputable def _d6c7e7e : SortNeExprs → SortString → SortInt → Option SortVList
    | SortNeExprs.inj_SortExpr E, X, N => do
      let _Val0 <- «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» E X N
      return (SortVList.«VCons(_,_)_MPY-SEMANTIC_VList_Value_VList» _Val0 SortVList.«VNil_MPY-SEMANTIC_VList»)
    | _, _, _ => none
end

def _53dc009 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» 0 N
    let _Val1 <- «_<Int_» N 10
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return N

noncomputable def «appendOracleBit(_,_)_VERIFICATION_Value_Value_Int» (x0 : SortValue) (x1 : SortInt) : Option SortValue := (_3be8a6e x0 x1) <|> (_fde9a69 x0 x1)

noncomputable def «sameValue(_,_)_VERIFICATION_Bool_Value_Value» (x0 : SortValue) (x1 : SortValue) : Option SortBool := _4b0aa40 x0 x1

noncomputable def _7194558 : SortPgm → SortInt → Option SortValue
  | SortPgm.«Module(_)_MPY-SYNTAX_Pgm_FuncDef» (SortFuncDef.«FuncDef(_,_,_)_MPY-SYNTAX_FuncDef_String_Params_Stmt» "solve" (SortParams.«Params(_)_MPY-SYNTAX_Params_String» X) (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» E)), N => do
    let _Val0 <- «evalExpr(_,_,_)_MPY-SEMANTIC_Value_Expr_String_Int» E X N
    return _Val0
  | _, _ => none

axiom «oracleDigitSum(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt
axiom _ab0177b : SortInt → Option SortInt

axiom _567128d : SortInt → Option SortValue
axiom «oracleBinaryPositive(_)_VERIFICATION_Value_Int» (x0 : SortInt) : Option SortValue

noncomputable def «runProgram(_,_)_MPY-SEMANTIC_Value_Pgm_Int» (x0 : SortPgm) (x1 : SortInt) : Option SortValue := _7194558 x0 x1

noncomputable def _2cc83e5 : SortInt → Option SortValue
  | N => do
    let _Val0 <- «_>Int_» N 0
    let _Val1 <- «oracleBinaryPositive(_)_VERIFICATION_Value_Int» N
    guard _Val0
    return _Val1

noncomputable def «oracleBinary(_)_VERIFICATION_Value_Int» (x0 : SortInt) : Option SortValue := (_2cc83e5 x0) <|> (_4291191 x0)

noncomputable def _881906b : SortInt → Option SortBool
  | N => do
    let _Val0 <- «runProgram(_,_)_MPY-SEMANTIC_Value_Pgm_Int» (SortPgm.«Module(_)_MPY-SYNTAX_Pgm_FuncDef» (SortFuncDef.«FuncDef(_,_,_)_MPY-SYNTAX_FuncDef_String_Params_Stmt» "solve" (SortParams.«Params(_)_MPY-SYNTAX_Params_String» "N") (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Expr» (SortExpr.«TupleExpr(_)_MPY-SYNTAX_Expr_NeExprs» (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "0") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "1") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "10") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "11") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "100") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "101") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "110") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "111") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "1000") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "1001") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "1010") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "1011") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "1100") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "1101") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "1110") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "1111") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "10000") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "10001") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "10010") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "10011") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "10100") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "10101") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "10110") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "10111") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "11000") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "11001") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "11010") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "11011") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "11100") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "11101") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "11110") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "11111") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "100000") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "100001") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "100010") (SortNeExprs.«_,__MPY-SYNTAX_NeExprs_Expr_NeExprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "100011") ((@inj SortExpr SortNeExprs) (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "100100"))))))))))))))))))))))))))))))))))))))) (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "%" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "N") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 10)) (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "%" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "//" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "N") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 10)) (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 10))) (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "%" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "//" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "N") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 100)) (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 10))) (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "%" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "//" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "N") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1000)) (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 10))) (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "%" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "//" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "N") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 10000)) (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 10))))))) N
    let _Val1 <- «oracleDigitSum(_)_VERIFICATION_Int_Int» N
    let _Val2 <- «oracleBinary(_)_VERIFICATION_Value_Int» _Val1
    let _Val3 <- «sameValue(_,_)_VERIFICATION_Bool_Value_Value» _Val0 _Val2
    return _Val3

noncomputable def «checkInput(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _881906b x0

axiom _15bb319 : SortInt → SortInt → Option SortBool
axiom «checkRange(_,_)_VERIFICATION_Bool_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortBool