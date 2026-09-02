import Klean157RightAngleTriangle.Inj

axiom «_*Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «_+Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortFloat

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

axiom «_>Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «_<Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «_==Float_» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «--Float__FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

axiom «Float2Int(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

axiom «ceilFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

axiom «exponentBitsFloat(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

axiom «floorFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

axiom «isNaN(_)_FLOAT_Bool_Float» (x0 : SortFloat) : Option SortBool

axiom «maxValueFloat(_,_)_FLOAT_Float_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortFloat

axiom «precisionFloat(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

def _667184e : Option SortVal := some (SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int» (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "a" (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "b" (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "c" SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames»))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«BoolOp(_,_)_MPY-SYNTAX_Expr_String_Exprs» "or" (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a")) (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b")) (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c"))))) (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b")) (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a")) (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c"))))) (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c")) (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a")) (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b"))))) SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») 0)

noncomputable local instance : DecidableEq SortKItem :=
  Classical.typeDecidableEq SortKItem

private noncomputable def kleanMapLookupModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Option SortKItem :=
  match entries with
  | [] => none
  | (candidate, value) :: rest =>
      if candidate = key then some value
      else kleanMapLookupModel rest key

private noncomputable def kleanMapContainsModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Bool :=
  match entries with
  | [] => false
  | (candidate, _) :: rest =>
      if candidate = key then true
      else kleanMapContainsModel rest key

private noncomputable def kleanMapDisjointModel
    (left right : List (SortKItem × SortKItem)) : Bool :=
  match right with
  | [] => true
  | (key, _) :: rest =>
      if kleanMapContainsModel left key then false
      else kleanMapDisjointModel left rest

private noncomputable def kleanMapDeleteModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => []
  | (candidate, value) :: rest =>
      if candidate = key then kleanMapDeleteModel rest key
      else (candidate, value) :: kleanMapDeleteModel rest key

private noncomputable def kleanMapUpdateModel
    (entries : List (SortKItem × SortKItem))
    (key value : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => [(key, value)]
  | (candidate, oldValue) :: rest =>
      if candidate = key then (key, value) :: rest
      else (candidate, oldValue) :: kleanMapUpdateModel rest key value

noncomputable def «.List» : Option SortList := some ⟨[]⟩

noncomputable def «.Map» : Option SortMap := some ⟨[]⟩

noncomputable def _List_ (x0 : SortList) (x1 : SortList) : Option SortList := some ⟨x0.coll ++ x1.coll⟩

noncomputable def _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap :=
  if kleanMapDisjointModel x0.coll x1.coll then
    some ⟨x0.coll ++ x1.coll⟩
  else none

noncomputable def «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=
  some ⟨[(x0, x1)]⟩

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

noncomputable def _07c1bf0 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_*Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _dc1bc34 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_+Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _e5f1d08 : SortInt → Option SortFloat
  | I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    return _Val0

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def _3994b91 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0

noncomputable def _6b33be1 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0

def _cc1fc26 : SortVal → SortVal → Option SortBool
  | SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_==Int_» I1 I2
    return _Val0
  | _, _ => none

def _27dbfa5 : SortVal → Option SortVal
  | SortVal.inj_SortInt I => do
    let _Val0 <- «_*Int_» I I
    return ((@inj SortInt SortVal) _Val0)
  | _ => none

def «rightAngleTriangleClosure()_VERIFICATION_Val» : Option SortVal := _667184e

def _6f6630c : SortVal → SortVal → Option SortVal
  | SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_+Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def mulF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _07c1bf0 x0 x1

noncomputable def addF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _dc1bc34 x0 x1

noncomputable def intToF (x0 : SortInt) : Option SortFloat := _e5f1d08 x0

noncomputable def _3cdc559 : SortFloat → Option SortBool
  | F => do
    let _Val0 <- «precisionFloat(_)_FLOAT_Int_Float» F
    let _Val1 <- «exponentBitsFloat(_)_FLOAT_Int_Float» F
    let _Val2 <- «maxValueFloat(_,_)_FLOAT_Float_Int_Int» _Val0 _Val1
    let _Val3 <- «_>Float__FLOAT_Bool_Float_Float» F _Val2
    let _Val4 <- «precisionFloat(_)_FLOAT_Int_Float» F
    let _Val5 <- «exponentBitsFloat(_)_FLOAT_Int_Float» F
    let _Val6 <- «maxValueFloat(_,_)_FLOAT_Float_Int_Int» _Val4 _Val5
    let _Val7 <- «--Float__FLOAT_Float_Float» _Val6
    let _Val8 <- «_<Float__FLOAT_Bool_Float_Float» F _Val7
    let _Val9 <- _orBool_ _Val3 _Val8
    return _Val9

noncomputable def eqF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _3994b91 x0 x1

noncomputable def trustedFloatEq (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _6b33be1 x0 x1

noncomputable def _1ce61be : SortVal → Option SortVal
  | SortVal.inj_SortFloat F => do
    let _Val0 <- mulF F F
    return ((@inj SortFloat SortVal) _Val0)
  | _ => none

noncomputable def _ccf42f4 : SortVal → SortVal → Option SortVal
  | SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- addF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _ => none

noncomputable def _19e450b : SortVal → SortVal → Option SortVal
  | SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- addF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _ => none

noncomputable def _d671867 : SortVal → SortVal → Option SortVal
  | SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- addF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _ => none

noncomputable def «isInfinite(_)_FLOAT_Bool_Float» (x0 : SortFloat) : Option SortBool := _3cdc559 x0

noncomputable def _f6dcaf4 : SortVal → SortVal → Option SortBool
  | SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- trustedFloatEq F1 F2
    return _Val0
  | _, _ => none

noncomputable def «ratSquare(_)_VERIFICATION_Val_Val» (x0 : SortVal) : Option SortVal := (_1ce61be x0) <|> (_27dbfa5 x0)

noncomputable def «ratAdd(_,_)_VERIFICATION_Val_Val_Val» (x0 : SortVal) (x1 : SortVal) : Option SortVal := (_19e450b x0 x1) <|> (_6f6630c x0 x1) <|> (_ccf42f4 x0 x1) <|> (_d671867 x0 x1)

noncomputable def _6a82bc3 : SortFloat → Option SortBool
  | F => do
    let _Val0 <- «isNaN(_)_FLOAT_Bool_Float» F
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «isInfinite(_)_FLOAT_Bool_Float» F
    let _Val3 <- notBool_ _Val2
    let _Val4 <- _andBool_ _Val1 _Val3
    return _Val4

noncomputable def floatFinite (x0 : SortFloat) : Option SortBool := _6a82bc3 x0

noncomputable def _e0c5cc2 : SortInt → SortFloat → Option SortBool
  | I, F => do
    let _Val0 <- floatFinite F
    let _Val1 <- notBool_ _Val0
    let _Val2 <- intToF I
    let _Val3 <- eqF _Val2 F
    guard _Val1
    return _Val3

noncomputable def _f18706c : SortInt → SortFloat → Option SortBool
  | I, F => do
    let _Val0 <- floatFinite F
    let _Val1 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val2 <- «ceilFloat(_)_FLOAT_Float_Float» F
    let _Val3 <- «_==Float_» _Val1 _Val2
    let _Val4 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val5 <- «Float2Int(_)_FLOAT_Int_Float» _Val4
    let _Val6 <- «_==Int_» _Val5 I
    let _Val7 <- _andBool_ _Val3 _Val6
    guard _Val0
    return _Val7

noncomputable def eqIF (x0 : SortInt) (x1 : SortFloat) : Option SortBool := (_e0c5cc2 x0 x1) <|> (_f18706c x0 x1)

noncomputable def _27748b6 : SortVal → SortVal → Option SortBool
  | SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- eqIF I F
    return _Val0
  | _, _ => none

noncomputable def _70db95b : SortVal → SortVal → Option SortBool
  | SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- eqIF I F
    return _Val0
  | _, _ => none

noncomputable def «ratEq(_,_)_VERIFICATION_Bool_Val_Val» (x0 : SortVal) (x1 : SortVal) : Option SortBool := (_27748b6 x0 x1) <|> (_70db95b x0 x1) <|> (_cc1fc26 x0 x1) <|> (_f6dcaf4 x0 x1)

noncomputable def _cf7c173 : SortVal → SortVal → SortVal → Option SortBool
  | A, B, C => do
    let _Val0 <- «ratSquare(_)_VERIFICATION_Val_Val» A
    let _Val1 <- «ratSquare(_)_VERIFICATION_Val_Val» B
    let _Val2 <- «ratSquare(_)_VERIFICATION_Val_Val» C
    let _Val3 <- «ratAdd(_,_)_VERIFICATION_Val_Val_Val» _Val1 _Val2
    let _Val4 <- «ratEq(_,_)_VERIFICATION_Bool_Val_Val» _Val0 _Val3
    let _Val5 <- «ratSquare(_)_VERIFICATION_Val_Val» B
    let _Val6 <- «ratSquare(_)_VERIFICATION_Val_Val» A
    let _Val7 <- «ratSquare(_)_VERIFICATION_Val_Val» C
    let _Val8 <- «ratAdd(_,_)_VERIFICATION_Val_Val_Val» _Val6 _Val7
    let _Val9 <- «ratEq(_,_)_VERIFICATION_Bool_Val_Val» _Val5 _Val8
    let _Val10 <- _orBool_ _Val4 _Val9
    let _Val11 <- «ratSquare(_)_VERIFICATION_Val_Val» C
    let _Val12 <- «ratSquare(_)_VERIFICATION_Val_Val» A
    let _Val13 <- «ratSquare(_)_VERIFICATION_Val_Val» B
    let _Val14 <- «ratAdd(_,_)_VERIFICATION_Val_Val_Val» _Val12 _Val13
    let _Val15 <- «ratEq(_,_)_VERIFICATION_Bool_Val_Val» _Val11 _Val14
    let _Val16 <- _orBool_ _Val10 _Val15
    return _Val16

noncomputable def «ratExpected(_,_,_)_VERIFICATION_Bool_Val_Val_Val» (x0 : SortVal) (x1 : SortVal) (x2 : SortVal) : Option SortBool := _cf7c173 x0 x1 x2