import Klean71TriangleArea.Inj

def _000c84b : Option SortModule := some (SortModule.«Module(_)_MPY-SYNTAX_Module_Stmts» (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Import(_)_MPY-SYNTAX_Stmt_String» "math") (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» "triangle_area" (SortParams.«Params(_)_MPY-SYNTAX_Params_ParamNames» (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "a" (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "b" (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "c" SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames»)))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«BoolOp(_,_)_MPY-SYNTAX_Expr_String_Exprs» "or" (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b")) (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<=" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c"))) (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c")) (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<=" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b"))) (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c")) (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<=" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a"))) SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»)))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» "-" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "semi_perimeter") (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "/" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b")) (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c")) (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 2))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "area") (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "math") "sqrt") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "*" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "semi_perimeter") (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "-" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "semi_perimeter") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a"))) (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "-" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "semi_perimeter") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b"))) (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "-" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "semi_perimeter") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "c"))) SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "round") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "area") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 2) SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»)))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)))

def _0c827ea : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», A => some A
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _dcbe275 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _0092bdb : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

axiom «absFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

def _0105150 : SortString → SortString → Option SortBool
  | _Gen0, _Gen1 => some false

def _dc25660 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», ACC => some ACC
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable local instance : DecidableEq SortK :=
  Classical.typeDecidableEq SortK
noncomputable def «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool :=
  some (decide (x0 = x1))

def _073f426 : SortString → SortInt → SortInt → Option SortInt
  | _Gen0, A, _Gen1 => some A

def _076da9f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

def _fd49342 : SortValSeq → SortVal → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some false
  | _, _ => none

axiom «_*Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

axiom «_>Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «_<Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «--Float__FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

axiom «Float2Int(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

axiom «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortFloat

axiom «exponentBitsFloat(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

axiom «floorFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

axiom «isNaN(_)_FLOAT_Bool_Float» (x0 : SortFloat) : Option SortBool

axiom «maxValueFloat(_,_)_FLOAT_Float_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortFloat

axiom «precisionFloat(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

def _c3be6f0 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», A => some A
  | _, _ => none

def _c5937bc : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 _Gen0, A => some A
  | _, _ => none

def _5a819d8 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

def _f69553d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _0f9305e : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

def _5dd92ea : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», A => some A
  | _, _ => none

def _e688eef : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 1
  | _ => none

def _218dc3a : SortString → Option SortIntSeq
  | "" => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «Int2String(_)_STRING-COMMON_String_Int» (x0 : SortInt) : Option SortString

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _b12fe18 : SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42 _Gen0 => some true
  | _ => none

def _e281c7f : SortIntSeq → Option SortBool
  | _Gen0 => some false

def _e46b672 : SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 _Gen0 => some true
  | _ => none

def _eceab8b : SortIntSeq → Option SortOpSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq»
  | _ => none

def _fd6d3a4 : SortIntSeq → Option SortBool
  | _Gen0 => some false

def _34926f2 : SortOpSeq → SortString → Option SortOpSeq
  | SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq», O => some (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» O SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq»)
  | _, _ => none

def _84535a7 : SortIntSeq → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», N => some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _, _ => none

axiom «_^Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _18fc027 : SortInt → SortEvPair → Option SortEvPair
  | N, SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))
  | _, _ => none

axiom «_^Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

def _4613fdc : SortValSeq → SortValSeq → SortValSeq → SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, _Gen1 => some true
  | _, _, _, _ => none

def _48f0ffc : SortVal → SortVals → Option SortVal
  | M, SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some M
  | _, _ => none

def _4b7fd38 : SortBool → Option SortInt
  | false => some 0
  | _ => none

def _73f627a : SortBool → Option SortInt
  | true => some 1
  | _ => none

def _80a1ae7 : SortInt → SortIntSeq → Option SortBool
  | _Gen0, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

axiom «_==Bool_» (x0 : SortBool) (x1 : SortBool) : Option SortBool

axiom «_==Float_» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «ceilFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

def _b662ad7 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

def _c71764f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _f3f7875 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1 => some true
  | _, _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

axiom «_-Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

axiom «_+Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

def _1de0a86 : SortEvPair → Option SortInt
  | _Gen0 => some 0

def _1f82817 : SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

def _2553414 : SortOpSeq → SortIntSeq → Option SortEvPair
  | SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq», NDS => some (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq» NDS)
  | _, _ => none

def _75246f8 : SortEvPair → Option SortEvPair
  | SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _ => none

def _89140a8 : SortEvPair → Option SortInt
  | SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» _Gen0 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N _Gen1) => some N
  | _ => none

def _8ad47ba : SortString → SortInt → SortEvPair → Option SortEvPair
  | O, N, SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS NDS => some (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» O OPS) (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N NDS))

def _eda2bc1 : SortEvPair → Option SortEvPair
  | SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _ => none

def _eeba85e : SortOpSeq → SortIntSeq → Option SortEvPair
  | _Gen0, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _, _ => none

def _28cc140 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», ACC => some ACC
  | _, _ => none

def _5e2c753 : SortIntSeq → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», C => some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _, _ => none

def _28eddda : SortString → SortVals → Option SortVal
  | "range", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some ((@inj SortIterable SortVal) (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» 0 I 1))
  | _, _ => none

axiom «exponentFloat(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

axiom «_/Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

def _f73c85c : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

def _37dc11b : SortInt → SortIntSeq → Option SortIntSeq
  | 0, ACC => some ACC
  | _, _ => none

def _a13a52f : SortVal → SortVals → Option SortVal
  | M, SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some M
  | _, _ => none

def _437b04b : SortString → SortVals → Option SortVal
  | "str", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS))
  | _, _ => none

def _495da55 : SortK → Option SortBool
  | K => some false

def _49c55eb : SortInt → Option SortIntSeq
  | 0 => some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _ => none

def _4b80f98 : SortString → SortVals → Option SortVal
  | "zip", SortVals.«_,__MPY-CORE_Vals_Val_Vals» _Pat0 (SortVals.«_,__MPY-CORE_Vals_Val_Vals» _Pat1 SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» B) => some ((@inj SortIterable SortVal) (SortIterable.«zipObj(_,_)_MPY-CORE_Iterable_ValSeq_ValSeq» A B))
    | _, _ => none
  | _, _ => none

def _583f938 : SortString → SortVals → Option SortVal
  | "ord", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some ((@inj SortInt SortVal) C)
  | _, _ => none

def _613283e : SortK → Option SortBool
  | K => some false

def _6d20a96 : SortString → SortVals → Option SortVal
  | "float", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortFloat F) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some ((@inj SortFloat SortVal) F)
  | _, _ => none

def _853fa53 : SortString → SortVals → Option SortVal
  | "range", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt A) (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt B) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => some ((@inj SortIterable SortVal) (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» A B 1))
  | _, _ => none

def _8978072 : SortVal → Option SortBool
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Gen0) => some true
  | _ => none

def _95cb29f : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortStr Str) SortK.dotk => some true
  | _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

axiom «_>=Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «absInt(_)_INT-COMMON_Int_Int» (x0 : SortInt) : Option SortInt

axiom «rootFloat(_,_)_FLOAT_Float_Float_Int» (x0 : SortFloat) (x1 : SortInt) : Option SortFloat

axiom «signFloat(_)_FLOAT_Bool_Float» (x0 : SortFloat) : Option SortBool

def _a971c50 : SortString → SortVals → Option SortVal
  | "zip", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A)) (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => some ((@inj SortIterable SortVal) (SortIterable.«zipObjS(_,_)_MPY-CORE_Iterable_IntSeq_IntSeq» A B))
  | _, _ => none

def _b48ab39 : SortIntSeq → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _Gen0 => some C
  | _ => none

def _c788a4b : SortVal → Option SortBool
  | _Gen0 => some false

def _d2fc3ce : SortVal → Option SortBool
  | SortVal.inj_SortBool _Gen0 => some true
  | _ => none

def _d74a36c : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortFloat Float) SortK.dotk => some true
  | _ => none

def _dadad71 : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortBool Bool) SortK.dotk => some true
  | _ => none

def _e10ded0 : SortK → Option SortBool
  | K => some false

def _e4f0a30 : SortString → SortVals → Option SortVal
  | "int", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some ((@inj SortInt SortVal) I)
  | _, _ => none

def _ec93494 : SortVal → Option SortBool
  | SortVal.inj_SortInt _Gen0 => some true
  | _ => none

def _ef206f4 : SortK → Option SortFloat
  | SortK.kseq (SortKItem.inj_SortFloat K) SortK.dotk => some K
  | _ => none

def _fbb3e9c : SortVal → Option SortBool
  | _Gen0 => some false

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

axiom proofIntToF (x0 : SortInt) : Option SortFloat

def «triangleProgram()_VERIFICATION_Module» : Option SortModule := _000c84b

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _614d946 : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_-Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

def _778079e : SortString → SortInt → SortInt → Option SortInt
  | "-", A, B => do
    let _Val0 <- «_-Int_» A B
    return _Val0
  | _, _, _ => none

def _b37e75d : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_==Int_» I1 I2
    return _Val0
  | _, _, _ => none

def _151fb31 : SortString → SortInt → SortInt → Option SortInt
  | "+", A, B => do
    let _Val0 <- «_+Int_» A B
    return _Val0
  | _, _, _ => none

def _bc844c7 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_+Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

def _13d6ee6 : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_*Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

def _19c50ab : SortString → SortInt → SortInt → Option SortInt
  | "*", A, B => do
    let _Val0 <- «_*Int_» A B
    return _Val0
  | _, _, _ => none

mutual
  def _6778888 : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, A => do
      let _Val0 <- «_*Int_» A 10
      let _Val1 <- «_-Int_» C 48
      let _Val2 <- «_+Int_» _Val0 _Val1
      let _Val3 <- «fracAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» R _Val2
      return _Val3
    | _, _ => none

  def «fracAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_0c827ea x0 x1) <|> (_6778888 x0 x1)
end

noncomputable def _00d63fc : SortFloat → Option SortFloat
  | F => do
    let _Val0 <- «absFloat(_)_FLOAT_Float_Float» F
    return _Val0

mutual
  def _01ae2fc : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, ACC => do
      let _Val0 <- «_*Int_» ACC 10
      let _Val1 <- «_-Int_» C 48
      let _Val2 <- «_+Int_» _Val0 _Val1
      let _Val3 <- «intDigAcc(_,_)_MPY-BUILTINS_Int_IntSeq_Int» R _Val2
      return _Val3
    | _, _ => none

  def «intDigAcc(_,_)_MPY-BUILTINS_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_01ae2fc x0 x1) <|> (_dc25660 x0 x1)
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _6b454b2 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_>Int_» I1 I2
    return _Val0
  | _, _, _ => none

def _b6ff738 : SortInt → SortInt → SortInt → Option SortInt
  | Q, R, B => do
    let _Val0 <- «_*Int_» 2 R
    let _Val1 <- «_>Int_» _Val0 B
    let _Val2 <- «_+Int_» Q 1
    guard _Val1
    return _Val2

def _cc09b1d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_>Int_» A B
    guard _Val0
    return false
  | _, _ => none

def _41490e6 : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_<Int_» I1 I2
    return _Val0
  | _, _, _ => none

def _9f6192d : SortInt → SortInt → SortInt → Option SortInt
  | Q, R, B => do
    let _Val0 <- «_*Int_» 2 R
    let _Val1 <- «_<Int_» _Val0 B
    guard _Val1
    return Q

def _c875e09 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_<Int_» A B
    guard _Val0
    return true
  | _, _ => none

noncomputable def _03e60c5 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) B) SortK.dotk)
    return _Val0
  | _, _, _ => none

noncomputable def _220c8a2 : SortString → SortVal → SortVal → Option SortBool
  | "is", V, SortVal.«noneV_MPY-CORE_Val» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) SortVal.«noneV_MPY-CORE_Val») SortK.dotk)
    return _Val0
  | _, _, _ => none

noncomputable def _57afa07 : SortString → SortVal → SortVal → Option SortBool
  | "==", V, SortVal.«noneV_MPY-CORE_Val» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) SortVal.«noneV_MPY-CORE_Val») SortK.dotk)
    return _Val0
  | _, _, _ => none

noncomputable def _6b7e0d4 : SortString → SortVal → SortVal → Option SortBool
  | "==", _Pat0, _Pat1 => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» B) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) B) SortK.dotk)
      return _Val0
    | _, _ => none
  | _, _, _ => none

noncomputable def _78864a2 : SortValSeq → SortVal → Option SortBool
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A _Gen0, K => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
    guard _Val0
    return true
  | _, _ => none

noncomputable def _dbd242d : SortValSeq → SortValSeq → SortVal → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» B _Gen1, K => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
    guard _Val0
    return B
  | _, _, _ => none

noncomputable def _f64794f : SortString → SortVal → SortVal → Option SortBool
  | "==", _Pat0, _Pat1 => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» B) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) B) SortK.dotk)
      return _Val0
    | _, _ => none
  | _, _, _ => none

noncomputable def _07c1bf0 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_*Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

def _0ae23e4 : SortString → SortVal → SortVal → Option SortBool
  | ">=", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_>=Int_» I1 I2
    return _Val0
  | _, _, _ => none

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def _fee1f6e : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_>Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

noncomputable def _5667141 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_<Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

noncomputable def _e5f1d08 : SortInt → Option SortFloat
  | I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    return _Val0

noncomputable def _85cabd6 : SortVal → Option SortInt
  | SortVal.inj_SortFloat F => do
    let _Val0 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val1 <- «Float2Int(_)_FLOAT_Int_Float» _Val0
    return _Val1
  | _ => none

mutual
  def «fscAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_5dd92ea x0 x1) <|> (_dcd0f49 x0 x1)

  def _dcd0f49 : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 R, A => do
      let _Val0 <- «_*Int_» A 10
      let _Val1 <- «fscAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» R _Val0
      return _Val1
    | _, _ => none
end

mutual
  def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

def _1c34a14 : SortString → SortVal → SortVal → Option SortBool
  | "<=", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_<=Int_» I1 I2
    return _Val0
  | _, _, _ => none

def «evHead47(_)_MPY-BUILTINS_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_e46b672 x0) <|> (_e281c7f x0)

def «evHead42(_)_MPY-BUILTINS_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_b12fe18 x0) <|> (_fd6d3a4 x0)

mutual
  def _358ff3c : SortOpSeq → SortString → Option SortOpSeq
    | SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» H T, O => do
      let _Val0 <- «appendOpE(_,_)_MPY-BUILTINS_OpSeq_OpSeq_String» T O
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» H _Val0)
    | _, _ => none

  def «appendOpE(_,_)_MPY-BUILTINS_OpSeq_OpSeq_String» (x0 : SortOpSeq) (x1 : SortString) : Option SortOpSeq := (_34926f2 x0 x1) <|> (_358ff3c x0 x1)
end

mutual
  def _781a952 : SortIntSeq → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H T, N => do
      let _Val0 <- «appendIE(_,_)_MPY-BUILTINS_IntSeq_IntSeq_Int» T N
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H _Val0)
    | _, _ => none

  def «appendIE(_,_)_MPY-BUILTINS_IntSeq_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortIntSeq := (_781a952 x0 x1) <|> (_84535a7 x0 x1)
end

noncomputable def _1e60d22 : SortInt → SortEvPair → Option SortEvPair
  | N, SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» M REST) => do
    let _Val0 <- «_^Int_» N M
    return (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Val0 REST))
  | _, _ => none

noncomputable def _4f03d42 : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_>=Int_» I2 0
    let _Val1 <- «_^Int_» I1 I2
    guard _Val0
    return ((@inj SortInt SortVal) _Val1)
  | _, _, _ => none

noncomputable def _d72724a : SortString → SortInt → SortInt → Option SortInt
  | "**", A, B => do
    let _Val0 <- «_^Int_» A B
    return _Val0
  | _, _, _ => none

noncomputable def _9daeaea : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_^Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

def «boolAsInt(_)_MPY-CORE_Int_Bool» (x0 : SortBool) : Option SortInt := (_4b7fd38 x0) <|> (_73f627a x0)

noncomputable def _9e5ad0c : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortBool B1, SortVal.inj_SortBool B2 => do
    let _Val0 <- «_==Bool_» B1 B2
    return _Val0
  | _, _, _ => none

noncomputable def _3994b91 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0

noncomputable def _b558675 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0
  | _, _, _ => none

noncomputable def _3836331 : SortVal → Option SortInt
  | SortVal.inj_SortFloat F => do
    let _Val0 <- «ceilFloat(_)_FLOAT_Float_Float» F
    let _Val1 <- «Float2Int(_)_FLOAT_Int_Float» _Val0
    return _Val1
  | _ => none

mutual
  def _5d69a53 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «vsLen(_)_MPY-CORE_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_5d69a53 x0) <|> (_b662ad7 x0)
end

noncomputable def _fabe8f9 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_-Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

noncomputable def _dc1bc34 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_+Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

def «firstNdE(_)_MPY-BUILTINS_Int_EvPair» (x0 : SortEvPair) : Option SortInt := (_89140a8 x0) <|> (_1de0a86 x0)

def «powCarryE(_,_,_)_MPY-BUILTINS_EvPair_String_Int_EvPair» (x0 : SortString) (x1 : SortInt) (x2 : SortEvPair) : Option SortEvPair := _8ad47ba x0 x1 x2

mutual
  def «snocCode(_,_)_MPY-SET_IntSeq_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortIntSeq := (_5e2c753 x0 x1) <|> (_cd5036e x0 x1)

  def _cd5036e : SortIntSeq → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H T, C => do
      let _Val0 <- «snocCode(_,_)_MPY-SET_IntSeq_IntSeq_Int» T C
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H _Val0)
    | _, _ => none
end

noncomputable def _291b93a : SortFloat → Option SortInt
  | F => do
    let _Val0 <- «exponentFloat(_)_FLOAT_Int_Float» F
    let _Val1 <- «_-Int_» 52 _Val0
    return _Val1

noncomputable def _2b8c3d8 : SortInt → SortFloat → Option SortFloat
  | I, F => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    let _Val1 <- «_/Float__FLOAT_Float_Float_Float» _Val0 F
    return _Val1

noncomputable def _ca2a05d : SortFloat → SortInt → Option SortFloat
  | F, I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    let _Val1 <- «_/Float__FLOAT_Float_Float_Float» F _Val0
    return _Val1

noncomputable def _d8a2a0c : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_/Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _ea38624 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_/Float__FLOAT_Float_Float_Float» F1 F2
    let _Val1 <- «floorFloat(_)_FLOAT_Float_Float» _Val0
    let _Val2 <- «_*Float__FLOAT_Float_Float_Float» _Val1 F2
    let _Val3 <- «_-Float__FLOAT_Float_Float_Float» F1 _Val2
    return _Val3

noncomputable def _edb22f9 : SortInt → SortInt → Option SortFloat
  | I1, I2 => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I1 53 11
    let _Val1 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I2 53 11
    let _Val2 <- «_/Float__FLOAT_Float_Float_Float» _Val0 _Val1
    return _Val2

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

noncomputable def _d16bd47 : SortString → SortVals → Option SortVal
  | "abs", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «absInt(_)_INT-COMMON_Int_Int» I
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _fc1f1e4 : SortFloat → Option SortFloat
  | F => do
    let _Val0 <- «rootFloat(_,_)_FLOAT_Float_Float_Int» F 2
    return _Val0

def «headIS(_)_MPY-FLOAT_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := _b48ab39 x0

def «isStrV(_)_MPY-BUILTINS_Bool_Val» (x0 : SortVal) : Option SortBool := (_8978072 x0) <|> (_c788a4b x0)

def isFloat (x0 : SortK) : Option SortBool := (_d74a36c x0) <|> (_613283e x0)

def isBool (x0 : SortK) : Option SortBool := (_dadad71 x0) <|> (_495da55 x0)

def isStr (x0 : SortK) : Option SortBool := (_95cb29f x0) <|> (_e10ded0 x0)

def «project:Float» (x0 : SortK) : Option SortFloat := _ef206f4 x0

def «isIntV(_)_MPY-BUILTINS_Bool_Val» (x0 : SortVal) : Option SortBool := (_d2fc3ce x0) <|> (_ec93494 x0) <|> (_fbb3e9c x0)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

noncomputable def _31fe72e : SortBool → SortBool → Option SortBool
  | B1, B2 => do
    let _Val0 <- «_==Bool_» B1 B2
    let _Val1 <- notBool_ _Val0
    return _Val1

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def _57f520f : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) B) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _7a57b51 : SortString → SortVal → SortVal → Option SortBool
  | "!=", _Pat0, _Pat1 => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» B) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) B) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      return _Val1
    | _, _ => none
  | _, _, _ => none

noncomputable def _882c519 : SortString → SortVal → SortVal → Option SortBool
  | "!=", V, SortVal.«noneV_MPY-CORE_Val» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) SortVal.«noneV_MPY-CORE_Val») SortK.dotk)
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _9f9c54d : SortString → SortVal → SortVal → Option SortBool
  | "!=", _Pat0, _Pat1 => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» B) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) B) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      return _Val1
    | _, _ => none
  | _, _, _ => none

noncomputable def _c0092c8 : SortString → SortVal → SortVal → Option SortBool
  | "is not", V, SortVal.«noneV_MPY-CORE_Val» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) SortVal.«noneV_MPY-CORE_Val») SortK.dotk)
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _c91e9fa : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- «_==Float_» F1 F2
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _f390a9b : SortString → SortString → Option SortBool
  | S1, S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    let _Val1 <- notBool_ _Val0
    return _Val1

def _6ef1389 : SortIntSeq → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 R => do
    let _Val0 <- «fracAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» R 0
    return _Val0
  | _ => none

noncomputable def absF (x0 : SortFloat) : Option SortFloat := _00d63fc x0

def _162db39 : SortInt → SortInt → SortInt → Option SortInt
  | Q, R, B => do
    let _Val0 <- «_*Int_» 2 R
    let _Val1 <- «_==Int_» _Val0 B
    let _Val2 <- _modInt_ Q 2
    let _Val3 <- «_==Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    guard _Val4
    return Q

def _18746b8 : SortInt → SortInt → SortInt → Option SortInt
  | LO, HI, ST => do
    let _Val0 <- «_>Int_» ST 0
    let _Val1 <- «_>Int_» HI LO
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_-Int_» HI LO
    let _Val4 <- «_+Int_» _Val3 ST
    let _Val5 <- «_-Int_» _Val4 1
    let _Val6 <- «_/Int_» _Val5 ST
    guard _Val2
    return _Val6

mutual
  def _3a4bf2f : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  def «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_3a4bf2f x0 x1) <|> (_5a819d8 x0 x1) <|> (_f69553d x0 x1)
end

def _72eff8b : SortString → SortVals → Option SortVal
  | "int", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «_<=Int_» 48 C
    let _Val1 <- «_<=Int_» C 57
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_-Int_» C 48
    guard _Val2
    return ((@inj SortInt SortVal) _Val3)
  | _, _ => none

def _bb50555 : SortString → SortVals → Option SortVal
  | "chr", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «_<=Int_» 0 I
    let _Val1 <- «_<Int_» I 128
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
  | _, _ => none

def _c0365fe : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_>=Int_» C 48
    let _Val1 <- «_<=Int_» C 57
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

def _d31716c : SortInt → SortInt → SortInt → Option SortInt
  | LO, HI, ST => do
    let _Val0 <- «_<Int_» ST 0
    let _Val1 <- «_<Int_» HI LO
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_-Int_» LO HI
    let _Val4 <- «_-Int_» _Val3 ST
    let _Val5 <- «_-Int_» _Val4 1
    let _Val6 <- «_-Int_» 0 ST
    let _Val7 <- «_/Int_» _Val5 _Val6
    guard _Val2
    return _Val7

mutual
  def _6a28f31 : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      guard _Val0
      return _Val1
    | _, _ => none

  def «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_0092bdb x0 x1) <|> (_6a28f31 x0 x1) <|> (_c71764f x0 x1) <|> (_c875e09 x0 x1) <|> (_cc09b1d x0 x1) <|> (_f3f7875 x0 x1)
end

mutual
  noncomputable def _07ab7bb : SortValSeq → SortVal → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A R, K => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» R K
      guard _Val1
      return _Val2
    | _, _ => none

  noncomputable def «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortBool := (_07ab7bb x0 x1) <|> (_78864a2 x0 x1) <|> (_fd49342 x0 x1)
end

mutual
  noncomputable def «dGet(_,_,_)_MPY-DICT_Val_ValSeq_ValSeq_Val» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortVal) : Option SortVal := (_a22e93c x0 x1 x2) <|> (_dbd242d x0 x1 x2)

  noncomputable def _a22e93c : SortValSeq → SortValSeq → SortVal → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A KR, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 VR, K => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «dGet(_,_,_)_MPY-DICT_Val_ValSeq_ValSeq_Val» KR VR K
      guard _Val1
      return _Val2
    | _, _, _ => none
end

noncomputable def mulF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _07c1bf0 x0 x1

noncomputable def _1ab1a90 : SortString → Option SortBool
  | OP => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» OP "=="
    let _Val1 <- «_==String__STRING-COMMON_Bool_String_String» OP "!="
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_==String__STRING-COMMON_Bool_String_String» OP "<"
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «_==String__STRING-COMMON_Bool_String_String» OP "<="
    let _Val6 <- _orBool_ _Val4 _Val5
    let _Val7 <- «_==String__STRING-COMMON_Bool_String_String» OP ">"
    let _Val8 <- _orBool_ _Val6 _Val7
    let _Val9 <- «_==String__STRING-COMMON_Bool_String_String» OP ">="
    let _Val10 <- _orBool_ _Val8 _Val9
    return _Val10

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

def _4ec3bb5 : SortInt → SortInt → SortInt → Option SortInt
  | LO, HI, ST => do
    let _Val0 <- «_>Int_» ST 0
    let _Val1 <- «_<=Int_» HI LO
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» ST 0
    let _Val4 <- «_>=Int_» HI LO
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    guard _Val6
    return 0

noncomputable def _8291415 : SortString → SortString → Option SortBool
  | "add", O => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» O "+"
    let _Val1 <- «_==String__STRING-COMMON_Bool_String_String» O "-"
    let _Val2 <- _orBool_ _Val0 _Val1
    return _Val2
  | _, _ => none

noncomputable def _8ca426b : SortString → Option SortBool
  | OP => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» OP "<"
    let _Val1 <- «_==String__STRING-COMMON_Bool_String_String» OP "<="
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_==String__STRING-COMMON_Bool_String_String» OP ">"
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «_==String__STRING-COMMON_Bool_String_String» OP ">="
    let _Val6 <- _orBool_ _Val4 _Val5
    return _Val6

mutual
  def «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortBool := (_80a1ae7 x0 x1) <|> (_c27c6a9 x0 x1)

  def _c27c6a9 : SortInt → SortIntSeq → Option SortBool
    | C, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H T => do
      let _Val0 <- «_==Int_» C H
      let _Val1 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C T
      let _Val2 <- _orBool_ _Val0 _Val1
      return _Val2
    | _, _ => none
end

noncomputable def _bb63bc4 : SortString → SortString → Option SortBool
  | "mul", O => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» O "*"
    let _Val1 <- «_==String__STRING-COMMON_Bool_String_String» O "//"
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_==String__STRING-COMMON_Bool_String_String» O "/"
    let _Val4 <- _orBool_ _Val2 _Val3
    return _Val4
  | _, _ => none

noncomputable def _d40cfb4 : SortString → Option SortBool
  | OP => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» OP "+"
    let _Val1 <- «_==String__STRING-COMMON_Bool_String_String» OP "-"
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_==String__STRING-COMMON_Bool_String_String» OP "*"
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «_==String__STRING-COMMON_Bool_String_String» OP "/"
    let _Val6 <- _orBool_ _Val4 _Val5
    let _Val7 <- «_==String__STRING-COMMON_Bool_String_String» OP "//"
    let _Val8 <- _orBool_ _Val6 _Val7
    let _Val9 <- «_==String__STRING-COMMON_Bool_String_String» OP "%"
    let _Val10 <- _orBool_ _Val8 _Val9
    let _Val11 <- «_==String__STRING-COMMON_Bool_String_String» OP "**"
    let _Val12 <- _orBool_ _Val10 _Val11
    return _Val12

noncomputable def gtF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _fee1f6e x0 x1

noncomputable def floatLt (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _5667141 x0 x1

noncomputable def intToF (x0 : SortInt) : Option SortFloat := _e5f1d08 x0

noncomputable def floorFI (x0 : SortVal) : Option SortInt := (_85cabd6 x0) <|> (_f73c85c x0)

def _c02b510 : SortIntSeq → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 R => do
    let _Val0 <- «fscAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» R 1
    return _Val0
  | _ => none

def _213f0c2 : SortString → SortVals → Option SortVal
  | "int", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» CS
    let _Val1 <- «_>=Int_» _Val0 2
    let _Val2 <- «intDigAcc(_,_)_MPY-BUILTINS_Int_IntSeq_Int» CS 0
    guard _Val1
    return ((@inj SortInt SortVal) _Val2)
  | _, _ => none

def _4b33ea6 : SortVal → Option SortInt
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» IS) => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    return _Val0
  | _ => none

def _d4293df : SortVal → Option SortInt
  | SortVal.«setV(_)_MPY-SET_Val_IntSeq» DS => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» DS
    return _Val0
  | _ => none

def _a6e6ac4 : SortString → SortInt → SortOpSeq → SortIntSeq → SortOpSeq → SortIntSeq → Option SortEvPair
  | _Gen0, CUR, SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq», _Gen1, OO, ON => do
    let _Val0 <- «appendIE(_,_)_MPY-BUILTINS_IntSeq_IntSeq_Int» ON CUR
    return (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OO _Val0)
  | _, _, _, _, _, _ => none

def _ce2bdd1 : SortString → SortInt → SortOpSeq → SortIntSeq → SortOpSeq → SortIntSeq → Option SortEvPair
  | _Gen0, CUR, SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» _Gen1 _Gen2, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», OO, ON => do
    let _Val0 <- «appendIE(_,_)_MPY-BUILTINS_IntSeq_IntSeq_Int» ON CUR
    return (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OO _Val0)
  | _, _, _, _, _, _ => none

noncomputable def «powCombE(_,_)_MPY-BUILTINS_EvPair_Int_EvPair» (x0 : SortInt) (x1 : SortEvPair) : Option SortEvPair := (_18fc027 x0 x1) <|> (_1e60d22 x0 x1)

noncomputable def powF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _9daeaea x0 x1

noncomputable def eqF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _3994b91 x0 x1

noncomputable def ceilF (x0 : SortVal) : Option SortInt := (_0f9305e x0) <|> (_3836331 x0)

def _8501a34 : SortVal → Option SortInt
  | _Pat0 => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      return _Val0
    | _ => none

def _90ec921 : SortVal → Option SortInt
  | _Pat0 => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      return _Val0
    | _ => none

noncomputable def subF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _fabe8f9 x0 x1

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

noncomputable def addF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _dc1bc34 x0 x1

noncomputable def «rExK(_)_MPY-FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt := _291b93a x0

noncomputable def intFloatDiv (x0 : SortInt) (x1 : SortFloat) : Option SortFloat := _2b8c3d8 x0 x1

noncomputable def divFloatIntV (x0 : SortFloat) (x1 : SortInt) : Option SortFloat := _ca2a05d x0 x1

noncomputable def divF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _d8a2a0c x0 x1

noncomputable def floatMod (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _ea38624 x0 x1

noncomputable def divII (x0 : SortInt) (x1 : SortInt) : Option SortFloat := _edb22f9 x0 x1

def _c2eab84 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» A B
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _, _, _ => none

noncomputable def «sqrtFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat := _fc1f1e4 x0

def _73630e2 : SortString → SortVals → Option SortVal
  | "isinstance", SortVals.«_,__MPY-CORE_Vals_Val_Vals» V (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.«typeV(_)_MPY-CORE_Val_String» "str") SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => do
    let _Val0 <- «isStrV(_)_MPY-BUILTINS_Bool_Val» V
    return ((@inj SortBool SortVal) _Val0)
  | _, _ => none

def _eb8c1ed : SortString → SortVals → Option SortVal
  | "isinstance", SortVals.«_,__MPY-CORE_Vals_Val_Vals» V (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.«typeV(_)_MPY-CORE_Val_String» "int") SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => do
    let _Val0 <- «isIntV(_)_MPY-BUILTINS_Bool_Val» V
    return ((@inj SortBool SortVal) _Val0)
  | _, _ => none

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def «_=/=Bool_» (x0 : SortBool) (x1 : SortBool) : Option SortBool := _31fe72e x0 x1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

noncomputable def _606434e : SortString → SortVals → Option SortVal
  | "abs", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortFloat F) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- absF F
    return ((@inj SortFloat SortVal) _Val0)
  | _, _ => none

def _38142ad : SortIntSeq → SortIntSeq → Option SortBool
  | P, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => do
    let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return false
  | _, _ => none

def _56a27c9 : SortIntSeq → SortIntSeq → Option SortBool
  | P, X => do
    let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P X
    guard _Val0
    return true

def «evDigit(_)_MPY-BUILTINS_Bool_Int» (x0 : SortInt) : Option SortBool := _c0365fe x0

def _758418c : SortString → SortVal → SortVal → Option SortBool
  | ">=", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» A B
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

def _8a4564e : SortString → SortVal → SortVal → Option SortBool
  | "<=", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» B A
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

def _9b4e435 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» B A
    return _Val0
  | _, _, _ => none

def _f10cf1b : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» A B
    return _Val0
  | _, _, _ => none

mutual
  noncomputable def «dSubset(_,_,_,_)_MPY-DICT_Bool_ValSeq_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortValSeq) (x3 : SortValSeq) : Option SortBool := (_4613fdc x0 x1 x2 x3) <|> (_e2b14d5 x0 x1 x2 x3)

  noncomputable def _e2b14d5 : SortValSeq → SortValSeq → SortValSeq → SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» K KR, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VR, KS2, VS2 => do
      let _Val0 <- «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» KS2 K
      let _Val1 <- «dGet(_,_,_)_MPY-DICT_Val_ValSeq_ValSeq_Val» KS2 VS2 K
      let _Val2 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) _Val1) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «dSubset(_,_,_,_)_MPY-DICT_Bool_ValSeq_ValSeq_ValSeq_ValSeq» KR VR KS2 VS2
      let _Val5 <- _andBool_ _Val3 _Val4
      return _Val5
    | _, _, _, _ => none
end

noncomputable def _30456db : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- mulF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def «isEqOrdOp(_)_MPY-CORE_Bool_String» (x0 : SortString) : Option SortBool := _1ab1a90 x0

noncomputable def «isInfinite(_)_FLOAT_Bool_Float» (x0 : SortFloat) : Option SortBool := _3cdc559 x0

def «rangeLen(_,_,_)_MPY-RANGE_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_18746b8 x0 x1 x2) <|> (_4ec3bb5 x0 x1 x2) <|> (_d31716c x0 x1 x2)

noncomputable def «isOrdOp(_)_MPY-CORE_Bool_String» (x0 : SortString) : Option SortBool := _8ca426b x0

mutual
  def _37448bb : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S, ACC => do
      let _Val0 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C ACC
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «snocCode(_,_)_MPY-SET_IntSeq_IntSeq_Int» ACC C
      let _Val3 <- «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» S _Val2
      guard _Val1
      return _Val3
    | _, _ => none

  def _5d1e314 : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S, ACC => do
      let _Val0 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C ACC
      let _Val1 <- «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» S ACC
      guard _Val0
      return _Val1
    | _, _ => none

  def «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_28cc140 x0 x1) <|> (_37448bb x0 x1) <|> (_5d1e314 x0 x1)
end

mutual
  def _9bcb96b : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S, B => do
      let _Val0 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C B
      let _Val1 <- «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» S B
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  def «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_076da9f x0 x1) <|> (_9bcb96b x0 x1)
end

noncomputable def «inLevelE(_,_)_MPY-BUILTINS_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := (_8291415 x0 x1) <|> (_bb63bc4 x0 x1) <|> (_0105150 x0 x1)

noncomputable def «isArithOp(_)_MPY-CORE_Bool_String» (x0 : SortString) : Option SortBool := _d40cfb4 x0

noncomputable def _3762d3f : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- gtF F1 F2
    return _Val0
  | _, _, _ => none

noncomputable def _641b30a : SortString → SortVal → SortVal → Option SortBool
  | "<=", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- gtF F1 F2
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _b69f73f : SortString → SortVal → SortVal → Option SortBool
  | ">=", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- floatLt F1 F2
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _f53e67b : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- floatLt F1 F2
    return _Val0
  | _, _, _ => none

noncomputable def _50f1b5a : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- mulF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _ca41a23 : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- mulF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _e64428a : SortString → SortVals → Option SortVal
  | "float", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- intToF I
    return ((@inj SortFloat SortVal) _Val0)
  | _, _ => none

noncomputable def _2d8e778 : SortString → SortVals → Option SortVal
  | "floor", SortVals.«_,__MPY-CORE_Vals_Val_Vals» V SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- floorFI V
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _1909c2e : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- powF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _a4f5818 : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- powF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _e0a3283 : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- powF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _4807966 : SortString → SortVals → Option SortVal
  | "ceil", SortVals.«_,__MPY-CORE_Vals_Val_Vals» V SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- ceilF V
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _a6670cb : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- subF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _d8961f0 : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- subF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _ebcc6ed : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- subF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

axiom _62d7600 : SortInt → SortIntSeq → Option SortIntSeq
axiom «binAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortIntSeq

noncomputable def _7f23ecf : SortString → SortVal → SortVal → Option SortVal
  | "%", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

noncomputable def _dece19f : SortString → SortVal → SortVal → Option SortVal
  | "//", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I1 I2
    let _Val1 <- «_-Int_» I1 _Val0
    let _Val2 <- «_/Int_» _Val1 I2
    return ((@inj SortInt SortVal) _Val2)
  | _, _, _ => none

noncomputable def _a4f63fd : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- addF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _b009d60 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- addF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _f394023 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- addF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _2cf2597 : SortFloat → Option SortInt
  | F => do
    let _Val0 <- «rExK(_)_MPY-FLOAT_Int_Float» F
    let _Val1 <- «_^Int_» 2 _Val0
    let _Val2 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» _Val1 53 11
    let _Val3 <- «_*Float__FLOAT_Float_Float_Float» F _Val2
    let _Val4 <- «Float2Int(_)_FLOAT_Int_Float» _Val3
    return _Val4

noncomputable def _cd2bd94 : SortFloat → Option SortInt
  | F => do
    let _Val0 <- «rExK(_)_MPY-FLOAT_Int_Float» F
    let _Val1 <- «_^Int_» 2 _Val0
    return _Val1

noncomputable def _4f373ea : SortString → SortVal → SortVal → Option SortVal
  | "/", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intFloatDiv I F
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _3598da3 : SortString → SortVal → SortVal → Option SortVal
  | "/", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- divFloatIntV F I
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _42bfa12 : SortString → SortVal → SortVal → Option SortVal
  | "/", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- divF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _2acce51 : SortString → SortVal → SortVal → Option SortVal
  | "%", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- floatMod F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _798d463 : SortString → SortVal → SortVal → Option SortVal
  | "/", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- divII I1 I2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _e8f314f : SortFloat → Option SortFloat
  | F => do
    let _Val0 <- «sqrtFloat(_)_FLOAT_Float_Float» F
    return _Val0

def _7ff1b9f : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortBool B, SortVal.inj_SortInt I => do
    let _Val0 <- kite B 1 0
    let _Val1 <- «_+Int_» _Val0 I
    return ((@inj SortInt SortVal) _Val1)
  | _, _, _ => none

noncomputable def _a1c85e7 : SortInt → SortInt → SortFloat → Option SortFloat
  | 0, _Gen0, F => do
    let _Val0 <- «signFloat(_)_FLOAT_Bool_Float» F
    let _Val1 <- kite _Val0 (-0e+00 : Float) (0.0 : Float)
    return _Val1
  | _, _, _ => none

noncomputable def _addf2bf : SortFloat → Option SortInt
  | F => do
    let _Val0 <- «_>=Float__FLOAT_Bool_Float_Float» F (0.0 : Float)
    let _Val1 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val2 <- «Float2Int(_)_FLOAT_Int_Float» _Val1
    let _Val3 <- «ceilFloat(_)_FLOAT_Float_Float» F
    let _Val4 <- «Float2Int(_)_FLOAT_Int_Float» _Val3
    let _Val5 <- kite _Val0 _Val2 _Val4
    return _Val5

noncomputable def _b220c77 : SortFloat → Option SortInt
  | F => do
    let _Val0 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val1 <- «_-Float__FLOAT_Float_Float_Float» F _Val0
    let _Val2 <- «_==Float_» _Val1 (0.5 : Float)
    let _Val3 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val4 <- «Float2Int(_)_FLOAT_Int_Float» _Val3
    let _Val5 <- «_%Int_» _Val4 2
    let _Val6 <- «_==Int_» _Val5 0
    let _Val7 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val8 <- «Float2Int(_)_FLOAT_Int_Float» _Val7
    let _Val9 <- «ceilFloat(_)_FLOAT_Float_Float» F
    let _Val10 <- «Float2Int(_)_FLOAT_Int_Float» _Val9
    let _Val11 <- kite _Val6 _Val8 _Val10
    let _Val12 <- «_+Float__FLOAT_Float_Float_Float» F (0.5 : Float)
    let _Val13 <- «floorFloat(_)_FLOAT_Float_Float» _Val12
    let _Val14 <- «Float2Int(_)_FLOAT_Int_Float» _Val13
    let _Val15 <- kite _Val2 _Val11 _Val14
    return _Val15

def _bb59890 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortInt I, SortVal.inj_SortBool B => do
    let _Val0 <- kite B 1 0
    let _Val1 <- «_+Int_» I _Val0
    return ((@inj SortInt SortVal) _Val1)
  | _, _, _ => none

noncomputable def _7031c92 : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortBool B1, SortVal.inj_SortBool B2 => do
    let _Val0 <- «_=/=Bool_» B1 B2
    return _Val0
  | _, _, _ => none

mutual
  def _002e323 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «_=/=Int_» C 46
      let _Val1 <- «fracPart(_)_MPY-FLOAT_Int_IntSeq» R
      guard _Val0
      return _Val1
    | _ => none

  def «fracPart(_)_MPY-FLOAT_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_002e323 x0) <|> (_6ef1389 x0) <|> (_dcbe275 x0)
end

mutual
  def _10441cc : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «_=/=Int_» C 46
      let _Val1 <- «fracScale(_)_MPY-FLOAT_Int_IntSeq» R
      guard _Val0
      return _Val1
    | _ => none

  def «fracScale(_)_MPY-FLOAT_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_10441cc x0) <|> (_c02b510 x0) <|> (_e688eef x0)
end

def _83dcf9b : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_=/=Int_» I2 0
    let _Val1 <- _modInt_ I1 I2
    let _Val2 <- «_-Int_» I1 _Val1
    let _Val3 <- «_/Int_» _Val2 I2
    guard _Val0
    return _Val3

def _8f26baa : SortInt → SortInt → SortInt → Option SortInt
  | Q, R, B => do
    let _Val0 <- «_*Int_» 2 R
    let _Val1 <- «_==Int_» _Val0 B
    let _Val2 <- _modInt_ Q 2
    let _Val3 <- «_=/=Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    let _Val5 <- «_+Int_» Q 1
    guard _Val4
    return _Val5

noncomputable def _96e80de : SortInt → SortInt → SortFloat → Option SortFloat
  | Q, SCALE, _Gen0 => do
    let _Val0 <- «_=/=Int_» Q 0
    let _Val1 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» Q 53 11
    let _Val2 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» SCALE 53 11
    let _Val3 <- «_/Float__FLOAT_Float_Float_Float» _Val1 _Val2
    guard _Val0
    return _Val3

mutual
  def «intPartAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_a28602a x0 x1) <|> (_c3be6f0 x0 x1) <|> (_c5937bc x0 x1)

  def _a28602a : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, A => do
      let _Val0 <- «_=/=Int_» C 46
      let _Val1 <- «_*Int_» A 10
      let _Val2 <- «_-Int_» C 48
      let _Val3 <- «_+Int_» _Val1 _Val2
      let _Val4 <- «intPartAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» R _Val3
      guard _Val0
      return _Val4
    | _, _ => none
end

def _c986c4d : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_=/=Int_» I1 I2
    return _Val0
  | _, _, _ => none

def _dc46a10 : SortString → SortVals → Option SortVal
  | "range", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt A) (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt B) (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt S) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»)) => do
    let _Val0 <- «_=/=Int_» S 0
    guard _Val0
    return ((@inj SortIterable SortVal) (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» A B S))
  | _, _ => none

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

mutual
  noncomputable def _65f01c5 : SortOpSeq → SortIntSeq → Option SortEvPair
    | SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "**" OPS, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N NDS => do
      let _Val0 <- «passPowE(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS NDS
      let _Val1 <- «powCombE(_,_)_MPY-BUILTINS_EvPair_Int_EvPair» N _Val0
      return _Val1
    | _, _ => none

  noncomputable def «passPowE(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» (x0 : SortOpSeq) (x1 : SortIntSeq) : Option SortEvPair := (_2553414 x0 x1) <|> (_65f01c5 x0 x1) <|> (_c7dba0d x0 x1) <|> (_eeba85e x0 x1)

  noncomputable def _c7dba0d : SortOpSeq → SortIntSeq → Option SortEvPair
    | SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» O OPS, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N NDS => do
      let _Val0 <- «_=/=String__STRING-COMMON_Bool_String_String» O "**"
      let _Val1 <- «passPowE(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS NDS
      let _Val2 <- «powCarryE(_,_,_)_MPY-BUILTINS_EvPair_String_Int_EvPair» O N _Val1
      guard _Val0
      return _Val2
    | _, _ => none
end

mutual
  def «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_38142ad x0 x1) <|> (_56a27c9 x0 x1) <|> (_e133ba2 x0 x1)

  def _e133ba2 : SortIntSeq → SortIntSeq → Option SortBool
    | P, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C Xs => do
      let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C Xs)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P Xs
      guard _Val1
      return _Val2
    | _, _ => none
end

mutual
  def _14cc9b7 : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 43 R => do
      let _Val0 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "+" _Val0)
    | _ => none

  def _3cea09f : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42 R => do
      let _Val0 <- «evHead42(_)_MPY-BUILTINS_Bool_IntSeq» R
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      guard _Val1
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "*" _Val2)
    | _ => none

  def _6191372 : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42 R) => do
      let _Val0 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "**" _Val0)
    | _ => none

  def _6493ac0 : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 R) => do
      let _Val0 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "//" _Val0)
    | _ => none

  def «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» (x0 : SortIntSeq) : Option SortOpSeq := (_14cc9b7 x0) <|> (_3cea09f x0) <|> (_6191372 x0) <|> (_6493ac0 x0) <|> (_afebecb x0) <|> (_cbc323c x0) <|> (_d2e1914 x0) <|> (_eceab8b x0) <|> (_f976bf9 x0)

  def _afebecb : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 R => do
      let _Val0 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "-" _Val0)
    | _ => none

  def _cbc323c : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 R => do
      let _Val0 <- «evHead47(_)_MPY-BUILTINS_Bool_IntSeq» R
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      guard _Val1
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "/" _Val2)
    | _ => none

  def _d2e1914 : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «evDigit(_)_MPY-BUILTINS_Bool_Int» C
      let _Val1 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      guard _Val0
      return _Val1
    | _ => none

  def _f976bf9 : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 R => do
      let _Val0 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      return _Val0
    | _ => none
end

mutual
  def «tokNdAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortIntSeq := (_b965464 x0 x1) <|> (_f2650fa x0 x1)

  def «tokNds(_)_MPY-BUILTINS_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := (_1f82817 x0) <|> (_a9081b9 x0) <|> (_cd3c56b x0) <|> (_d31de50 x0)

  def _a9081b9 : SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «evDigit(_)_MPY-BUILTINS_Bool_Int» C
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «_=/=Int_» C 32
      let _Val3 <- _andBool_ _Val1 _Val2
      let _Val4 <- «tokNds(_)_MPY-BUILTINS_IntSeq_IntSeq» R
      guard _Val3
      return _Val4
    | _ => none

  def _b965464 : SortInt → SortIntSeq → Option SortIntSeq
    | A, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «evDigit(_)_MPY-BUILTINS_Bool_Int» C
      let _Val1 <- «_*Int_» A 10
      let _Val2 <- «_-Int_» C 48
      let _Val3 <- «_+Int_» _Val1 _Val2
      let _Val4 <- «tokNdAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» _Val3 R
      guard _Val0
      return _Val4
    | _, _ => none

  def _cd3c56b : SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «evDigit(_)_MPY-BUILTINS_Bool_Int» C
      let _Val1 <- «_-Int_» C 48
      let _Val2 <- «tokNdAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» _Val1 R
      guard _Val0
      return _Val2
    | _ => none

  def _d31de50 : SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 R => do
      let _Val0 <- «tokNds(_)_MPY-BUILTINS_IntSeq_IntSeq» R
      return _Val0
    | _ => none

  def _f2650fa : SortInt → SortIntSeq → Option SortIntSeq
    | A, S => do
      let _Val0 <- «tokNds(_)_MPY-BUILTINS_IntSeq_IntSeq» S
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A _Val0)
end

noncomputable def _9a8a33a : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» KS1 VS1, SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» KS2 VS2 => do
    let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» KS1
    let _Val1 <- «vsLen(_)_MPY-CORE_Int_ValSeq» KS2
    let _Val2 <- «_==Int_» _Val0 _Val1
    let _Val3 <- «dSubset(_,_,_,_)_MPY-DICT_Bool_ValSeq_ValSeq_ValSeq_ValSeq» KS1 VS1 KS2 VS2
    let _Val4 <- _andBool_ _Val2 _Val3
    return _Val4
  | _, _, _ => none

noncomputable def _6a82bc3 : SortFloat → Option SortBool
  | F => do
    let _Val0 <- «isNaN(_)_FLOAT_Bool_Float» F
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «isInfinite(_)_FLOAT_Bool_Float» F
    let _Val3 <- notBool_ _Val2
    let _Val4 <- _andBool_ _Val1 _Val3
    return _Val4

def _1719aa8 : SortVal → Option SortInt
  | _Pat0 => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» LO HI ST) => do
      let _Val0 <- «rangeLen(_,_,_)_MPY-RANGE_Int_Int_Int_Int» LO HI ST
      return _Val0
    | _ => none

def _a8c9961 : SortIntSeq → Option SortIntSeq
  | CS => do
    let _Val0 <- «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» CS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return _Val0

def _d3d248d : SortIntSeq → SortIntSeq → Option SortBool
  | A, B => do
    let _Val0 <- «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» A B
    let _Val1 <- «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» B A
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

noncomputable def _323c995 : SortInt → Option SortIntSeq
  | N => do
    let _Val0 <- «_>Int_» N 0
    let _Val1 <- «binAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» N SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    guard _Val0
    return _Val1

noncomputable def «rExNumer(_)_MPY-FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt := _2cf2597 x0

noncomputable def «rExDenom(_)_MPY-FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt := _cd2bd94 x0

noncomputable def sqrtF (x0 : SortFloat) : Option SortFloat := _e8f314f x0

noncomputable def truncF (x0 : SortFloat) : Option SortInt := _addf2bf x0

noncomputable def roundF (x0 : SortFloat) : Option SortInt := _b220c77 x0

axiom _60e6213 : SortString → SortVal → SortVal → Option SortVal
axiom _6b2bff4 : SortString → SortVal → SortVal → Option SortVal
axiom _7346d9f : SortString → SortVal → SortVal → Option SortVal
axiom «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» (x0 : SortString) (x1 : SortVal) (x2 : SortVal) : Option SortVal
axiom _fc81955 : SortString → SortVal → SortVal → Option SortVal
axiom _ff208f3 : SortString → SortVal → SortVal → Option SortVal

def _divInt_ (x0 : SortInt) (x1 : SortInt) : Option SortInt := _83dcf9b x0 x1

def «rndHE(_,_,_)_MPY-FLOAT_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_162db39 x0 x1 x2) <|> (_8f26baa x0 x1 x2) <|> (_9f6192d x0 x1 x2) <|> (_b6ff738 x0 x1 x2)

noncomputable def «rheToFloat(_,_,_)_MPY-FLOAT_Float_Int_Int_Float» (x0 : SortInt) (x1 : SortInt) (x2 : SortFloat) : Option SortFloat := (_96e80de x0 x1 x2) <|> (_a1c85e7 x0 x1 x2)

def _0bf42d3 : SortIntSeq → Option SortInt
  | CS => do
    let _Val0 <- «intPartAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» CS 0
    return _Val0

noncomputable def _108b118 : SortString → SortVals → Option SortVal
  | "str", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «Int2String(_)_STRING-COMMON_String_Int» I
    let _Val1 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val0
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val1))
  | _, _ => none

def _0d7d6b1 : SortString → SortVal → SortVal → Option SortBool
  | "not in", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» P), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» X) => do
    let _Val0 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P X
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

def _9d30e79 : SortString → SortVal → SortVal → Option SortBool
  | "in", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» P), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» X) => do
    let _Val0 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P X
    return _Val0
  | _, _, _ => none

noncomputable def floatFinite (x0 : SortFloat) : Option SortBool := _6a82bc3 x0

def «seqLen(_)_MPY-BUILTINS_Int_Val» (x0 : SortVal) : Option SortInt := (_1719aa8 x0) <|> (_4b33ea6 x0) <|> (_8501a34 x0) <|> (_90ec921 x0) <|> (_d4293df x0)

def «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _a8c9961 x0

def «sameSet(_,_)_MPY-SET_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := _d3d248d x0 x1

noncomputable def «binCodes(_)_MPY-BUILTINS_IntSeq_Int» (x0 : SortInt) : Option SortIntSeq := (_323c995 x0) <|> (_49c55eb x0)

noncomputable def _ecd3e5c : SortString → SortVals → Option SortVal
  | "int", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortFloat F) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- truncF F
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _1b20c41 : SortString → SortVals → Option SortVal
  | "round", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortFloat F) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- roundF F
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _4dc295c : SortFloat → SortInt → Option SortFloat
  | F, N => do
    let _Val0 <- «_^Int_» 10 N
    let _Val1 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» _Val0 53 11
    let _Val2 <- «_*Float__FLOAT_Float_Float_Float» F _Val1
    let _Val3 <- roundF _Val2
    let _Val4 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» _Val3 53 11
    let _Val5 <- «_^Int_» 10 N
    let _Val6 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» _Val5 53 11
    let _Val7 <- «_/Float__FLOAT_Float_Float_Float» _Val4 _Val6
    return _Val7

noncomputable def _922ae60 : SortVal → SortVal → SortVal → Option SortVal
  | A, B, C => do
    let _Val0 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" A B
    let _Val1 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" _Val0 C
    let _Val2 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "/" _Val1 ((@inj SortInt SortVal) 2)
    return _Val2

def _e865ca1 : SortString → SortInt → SortInt → Option SortInt
  | "//", A, B => do
    let _Val0 <- _divInt_ A B
    return _Val0
  | _, _, _ => none

def _03e112f : SortInt → SortInt → Option SortInt
  | A, B => do
    let _Val0 <- _divInt_ A B
    let _Val1 <- _modInt_ A B
    let _Val2 <- «rndHE(_,_,_)_MPY-FLOAT_Int_Int_Int_Int» _Val0 _Val1 B
    return _Val2

def «intPart(_)_MPY-FLOAT_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := _0bf42d3 x0

noncomputable def _4c721dd : SortInt → SortFloat → Option SortBool
  | I, F => do
    let _Val0 <- floatFinite F
    let _Val1 <- «ceilFloat(_)_FLOAT_Float_Float» F
    let _Val2 <- «Float2Int(_)_FLOAT_Int_Float» _Val1
    let _Val3 <- «_>Int_» _Val2 I
    guard _Val0
    return _Val3

noncomputable def _5784e42 : SortFloat → SortInt → Option SortBool
  | F, I => do
    let _Val0 <- floatFinite F
    let _Val1 <- notBool_ _Val0
    let _Val2 <- intToF I
    let _Val3 <- floatLt F _Val2
    guard _Val1
    return _Val3

noncomputable def _69e2bae : SortInt → SortFloat → Option SortBool
  | I, F => do
    let _Val0 <- floatFinite F
    let _Val1 <- notBool_ _Val0
    let _Val2 <- intToF I
    let _Val3 <- floatLt _Val2 F
    guard _Val1
    return _Val3

noncomputable def _e0c5cc2 : SortInt → SortFloat → Option SortBool
  | I, F => do
    let _Val0 <- floatFinite F
    let _Val1 <- notBool_ _Val0
    let _Val2 <- intToF I
    let _Val3 <- eqF _Val2 F
    guard _Val1
    return _Val3

noncomputable def _e4aab2f : SortFloat → SortInt → Option SortBool
  | F, I => do
    let _Val0 <- floatFinite F
    let _Val1 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val2 <- «Float2Int(_)_FLOAT_Int_Float» _Val1
    let _Val3 <- «_<Int_» _Val2 I
    guard _Val0
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

def _f1c888d : SortString → SortVals → Option SortVal
  | "len", SortVals.«_,__MPY-CORE_Vals_Val_Vals» OBJ SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «seqLen(_)_MPY-BUILTINS_Int_Val» OBJ
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

def _20b19cf : SortString → SortVals → Option SortVal
  | "set", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» CS
    return (SortVal.«setV(_)_MPY-SET_Val_IntSeq» _Val0)
  | _, _ => none

def _87bf7c6 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.«setV(_)_MPY-SET_Val_IntSeq» A, SortVal.«setV(_)_MPY-SET_Val_IntSeq» B => do
    let _Val0 <- «sameSet(_,_)_MPY-SET_Bool_IntSeq_IntSeq» A B
    return _Val0
  | _, _, _ => none

noncomputable def _a4fd04a : SortString → SortVals → Option SortVal
  | "bin", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt N) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «_>=Int_» N 0
    let _Val1 <- «binCodes(_)_MPY-BUILTINS_IntSeq_Int» N
    guard _Val0
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 _Val1))))
  | _, _ => none

noncomputable def _e22316b : SortString → SortVals → Option SortVal
  | "bin", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt N) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «_<Int_» N 0
    let _Val1 <- «_-Int_» 0 N
    let _Val2 <- «binCodes(_)_MPY-BUILTINS_IntSeq_Int» _Val1
    guard _Val0
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 _Val2)))))
  | _, _ => none

noncomputable def «semiPerimeter(_,_,_)_VERIFICATION_Val_Val_Val_Val» (x0 : SortVal) (x1 : SortVal) (x2 : SortVal) : Option SortVal := _922ae60 x0 x1 x2

noncomputable def «applyOpE(_,_,_)_MPY-BUILTINS_Int_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_151fb31 x0 x1 x2) <|> (_19c50ab x0 x1 x2) <|> (_778079e x0 x1 x2) <|> (_d72724a x0 x1 x2) <|> (_e865ca1 x0 x1 x2) <|> (_073f426 x0 x1 x2)

def «rndHalfEven(_,_)_MPY-FLOAT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _03e112f x0 x1

noncomputable def _f17777e : SortIntSeq → Option SortFloat
  | CS => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» CS
    let _Val1 <- «_>Int_» _Val0 0
    let _Val2 <- «headIS(_)_MPY-FLOAT_Int_IntSeq» CS
    let _Val3 <- «_=/=Int_» _Val2 45
    let _Val4 <- _andBool_ _Val1 _Val3
    let _Val5 <- «intPart(_)_MPY-FLOAT_Int_IntSeq» CS
    let _Val6 <- intToF _Val5
    let _Val7 <- «fracPart(_)_MPY-FLOAT_Int_IntSeq» CS
    let _Val8 <- intToF _Val7
    let _Val9 <- «fracScale(_)_MPY-FLOAT_Int_IntSeq» CS
    let _Val10 <- intToF _Val9
    let _Val11 <- «_/Float__FLOAT_Float_Float_Float» _Val8 _Val10
    let _Val12 <- «_+Float__FLOAT_Float_Float_Float» _Val6 _Val11
    guard _Val4
    return _Val12

noncomputable def ltIF (x0 : SortInt) (x1 : SortFloat) : Option SortBool := (_4c721dd x0 x1) <|> (_69e2bae x0 x1)

noncomputable def ltFI (x0 : SortFloat) (x1 : SortInt) : Option SortBool := (_5784e42 x0 x1) <|> (_e4aab2f x0 x1)

noncomputable def eqIF (x0 : SortInt) (x1 : SortFloat) : Option SortBool := (_e0c5cc2 x0 x1) <|> (_f18706c x0 x1)

noncomputable def _cd5f09e : SortVal → SortVal → SortVal → Option SortVal
  | A, B, C => do
    let _Val0 <- «semiPerimeter(_,_,_)_VERIFICATION_Val_Val_Val_Val» A B C
    let _Val1 <- «semiPerimeter(_,_,_)_VERIFICATION_Val_Val_Val_Val» A B C
    let _Val2 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "-" _Val1 A
    let _Val3 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "*" _Val0 _Val2
    let _Val4 <- «semiPerimeter(_,_,_)_VERIFICATION_Val_Val_Val_Val» A B C
    let _Val5 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "-" _Val4 B
    let _Val6 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "*" _Val3 _Val5
    let _Val7 <- «semiPerimeter(_,_,_)_VERIFICATION_Val_Val_Val_Val» A B C
    let _Val8 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "-" _Val7 C
    let _Val9 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "*" _Val6 _Val8
    return _Val9

mutual
  noncomputable def _7032cf2 : SortString → SortInt → SortOpSeq → SortIntSeq → SortOpSeq → SortIntSeq → Option SortEvPair
    | L, CUR, SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» O OPS, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N NDS, OO, ON => do
      let _Val0 <- «inLevelE(_,_)_MPY-BUILTINS_Bool_String_String» L O
      let _Val1 <- «applyOpE(_,_,_)_MPY-BUILTINS_Int_String_Int_Int» O CUR N
      let _Val2 <- «passLGoE(_,_,_,_,_,_)_MPY-BUILTINS_EvPair_String_Int_OpSeq_IntSeq_OpSeq_IntSeq» L _Val1 OPS NDS OO ON
      guard _Val0
      return _Val2
    | _, _, _, _, _, _ => none

  noncomputable def «passLGoE(_,_,_,_,_,_)_MPY-BUILTINS_EvPair_String_Int_OpSeq_IntSeq_OpSeq_IntSeq» (x0 : SortString) (x1 : SortInt) (x2 : SortOpSeq) (x3 : SortIntSeq) (x4 : SortOpSeq) (x5 : SortIntSeq) : Option SortEvPair := (_7032cf2 x0 x1 x2 x3 x4 x5) <|> (_a6e6ac4 x0 x1 x2 x3 x4 x5) <|> (_a7ad23b x0 x1 x2 x3 x4 x5) <|> (_ce2bdd1 x0 x1 x2 x3 x4 x5)

  noncomputable def _a7ad23b : SortString → SortInt → SortOpSeq → SortIntSeq → SortOpSeq → SortIntSeq → Option SortEvPair
    | L, CUR, SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» O OPS, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N NDS, OO, ON => do
      let _Val0 <- «inLevelE(_,_)_MPY-BUILTINS_Bool_String_String» L O
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «appendOpE(_,_)_MPY-BUILTINS_OpSeq_OpSeq_String» OO O
      let _Val3 <- «appendIE(_,_)_MPY-BUILTINS_IntSeq_IntSeq_Int» ON CUR
      let _Val4 <- «passLGoE(_,_,_,_,_,_)_MPY-BUILTINS_EvPair_String_Int_OpSeq_IntSeq_OpSeq_IntSeq» L N OPS NDS _Val2 _Val3
      guard _Val1
      return _Val4
    | _, _, _, _, _, _ => none
end

noncomputable def _c2f5de0 : SortFloat → SortInt → Option SortFloat
  | F, N => do
    let _Val0 <- «rExNumer(_)_MPY-FLOAT_Int_Float» F
    let _Val1 <- «_^Int_» 10 N
    let _Val2 <- «_*Int_» _Val0 _Val1
    let _Val3 <- «rExDenom(_)_MPY-FLOAT_Int_Float» F
    let _Val4 <- «rndHalfEven(_,_)_MPY-FLOAT_Int_Int_Int» _Val2 _Val3
    let _Val5 <- «_^Int_» 10 N
    let _Val6 <- «rheToFloat(_,_,_)_MPY-FLOAT_Float_Int_Int_Float» _Val4 _Val5 F
    return _Val6

mutual
  noncomputable def decStrToF (x0 : SortIntSeq) : Option SortFloat := (_ed58d1a x0) <|> (_f17777e x0)

  noncomputable def _ed58d1a : SortIntSeq → Option SortFloat
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 CS => do
      let _Val0 <- decStrToF CS
      let _Val1 <- «_-Float__FLOAT_Float_Float_Float» (0.0 : Float) _Val0
      return _Val1
    | _ => none
end

noncomputable def _30f7376 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- ltIF I F
    return _Val0
  | _, _, _ => none

noncomputable def _56d50b0 : SortString → SortVal → SortVal → Option SortBool
  | ">=", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- ltIF I F
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _ba3c3fb : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- ltIF I F
    return _Val0
  | _, _, _ => none

noncomputable def _d2878f8 : SortString → SortVal → SortVal → Option SortBool
  | "<=", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- ltIF I F
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _0aebdfa : SortString → SortVal → SortVal → Option SortBool
  | "<=", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- ltFI F I
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _71b87a8 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- ltFI F I
    return _Val0
  | _, _, _ => none

noncomputable def _ea5bc25 : SortString → SortVal → SortVal → Option SortBool
  | ">=", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- ltFI F I
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _f0242b6 : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- ltFI F I
    return _Val0
  | _, _, _ => none

noncomputable def _3162a0b : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- eqIF I F
    return _Val0
  | _, _, _ => none

noncomputable def _62f4b8a : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- eqIF I F
    return _Val0
  | _, _, _ => none

noncomputable def _64d7c13 : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- eqIF I F
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _ce56bf1 : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- eqIF I F
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def «heronProduct(_,_,_)_VERIFICATION_Val_Val_Val_Val» (x0 : SortVal) (x1 : SortVal) (x2 : SortVal) : Option SortVal := _cd5f09e x0 x1 x2

noncomputable def _16b47fd : SortEvPair → Option SortEvPair
  | SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N0 NDS) => do
    let _Val0 <- «passLGoE(_,_,_,_,_,_)_MPY-BUILTINS_EvPair_String_Int_OpSeq_IntSeq_OpSeq_IntSeq» "add" N0 OPS NDS SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return _Val0
  | _ => none

noncomputable def _c6b686a : SortEvPair → Option SortEvPair
  | SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N0 NDS) => do
    let _Val0 <- «passLGoE(_,_,_,_,_,_)_MPY-BUILTINS_EvPair_String_Int_OpSeq_IntSeq_OpSeq_IntSeq» "mul" N0 OPS NDS SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return _Val0
  | _ => none

noncomputable def «roundExactFN(_,_)_MPY-FLOAT_Float_Float_Int» (x0 : SortFloat) (x1 : SortInt) : Option SortFloat := _c2f5de0 x0 x1

noncomputable def _8f573a0 : SortString → SortVals → Option SortVal
  | "float", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- decStrToF CS
    return ((@inj SortFloat SortVal) _Val0)
  | _, _ => none

axiom _7602aea : SortString → SortVal → SortVal → Option SortBool
axiom _9669df5 : SortString → SortVal → SortVal → Option SortBool
axiom _9a4e525 : SortString → SortVal → SortVal → Option SortBool
axiom _9fe303a : SortString → SortVal → SortVal → Option SortBool
axiom «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» (x0 : SortString) (x1 : SortVal) (x2 : SortVal) : Option SortBool
axiom _cb210bb : SortString → SortVal → SortVal → Option SortBool

noncomputable def «passAddE(_)_MPY-BUILTINS_EvPair_EvPair» (x0 : SortEvPair) : Option SortEvPair := (_16b47fd x0) <|> (_75246f8 x0)

noncomputable def «passMulE(_)_MPY-BUILTINS_EvPair_EvPair» (x0 : SortEvPair) : Option SortEvPair := (_c6b686a x0) <|> (_eda2bc1 x0)

noncomputable def _42be4f7 : SortFloat → SortInt → Option SortFloat
  | F, N => do
    let _Val0 <- «isNaN(_)_FLOAT_Bool_Float» F
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «isInfinite(_)_FLOAT_Bool_Float» F
    let _Val3 <- notBool_ _Val2
    let _Val4 <- _andBool_ _Val1 _Val3
    let _Val5 <- «_>=Int_» N 0
    let _Val6 <- _andBool_ _Val4 _Val5
    let _Val7 <- «absFloat(_)_FLOAT_Float_Float» F
    let _Val8 <- «_<Float__FLOAT_Bool_Float_Float» _Val7 (1000000000000.0 : Float)
    let _Val9 <- _andBool_ _Val6 _Val8
    let _Val10 <- «absFloat(_)_FLOAT_Float_Float» F
    let _Val11 <- «_^Int_» 10 N
    let _Val12 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» _Val11 53 11
    let _Val13 <- «_*Float__FLOAT_Float_Float_Float» _Val10 _Val12
    let _Val14 <- «_<Float__FLOAT_Bool_Float_Float» _Val13 (4500000000000000.0 : Float)
    let _Val15 <- _andBool_ _Val9 _Val14
    let _Val16 <- «exponentFloat(_)_FLOAT_Int_Float» F
    let _Val17 <- «_>Int_» _Val16 (-900)
    let _Val18 <- _andBool_ _Val15 _Val17
    let _Val19 <- «roundExactFN(_,_)_MPY-FLOAT_Float_Float_Int» F N
    guard _Val18
    return _Val19

mutual
  noncomputable def _1b13536 : SortVal → SortVals → Option SortVal
    | M, SortVals.«_,__MPY-CORE_Vals_Val_Vals» V R => do
      let _Val0 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "<" V M
      let _Val1 <- «minVals(_,_)_MPY-BUILTINS_Val_Val_Vals» V R
      guard _Val0
      return _Val1
    | _, _ => none

  noncomputable def _4dd24fe : SortVal → SortVals → Option SortVal
    | M, SortVals.«_,__MPY-CORE_Vals_Val_Vals» V R => do
      let _Val0 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "<" V M
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «minVals(_,_)_MPY-BUILTINS_Val_Val_Vals» M R
      guard _Val1
      return _Val2
    | _, _ => none

  noncomputable def «minVals(_,_)_MPY-BUILTINS_Val_Val_Vals» (x0 : SortVal) (x1 : SortVals) : Option SortVal := (_1b13536 x0 x1) <|> (_48f0ffc x0 x1) <|> (_4dd24fe x0 x1)
end

mutual
  noncomputable def _46b68e8 : SortVal → SortVals → Option SortVal
    | M, SortVals.«_,__MPY-CORE_Vals_Val_Vals» V R => do
      let _Val0 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" V M
      let _Val1 <- «maxVals(_,_)_MPY-BUILTINS_Val_Val_Vals» V R
      guard _Val0
      return _Val1
    | _, _ => none

  noncomputable def «maxVals(_,_)_MPY-BUILTINS_Val_Val_Vals» (x0 : SortVal) (x1 : SortVals) : Option SortVal := (_46b68e8 x0 x1) <|> (_a13a52f x0 x1) <|> (_d94269b x0 x1)

  noncomputable def _d94269b : SortVal → SortVals → Option SortVal
    | M, SortVals.«_,__MPY-CORE_Vals_Val_Vals» V R => do
      let _Val0 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" V M
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «maxVals(_,_)_MPY-BUILTINS_Val_Val_Vals» M R
      guard _Val1
      return _Val2
    | _, _ => none
end

noncomputable def _c91b701 : SortVal → SortVal → SortVal → Option SortBool
  | A, B, C => do
    let _Val0 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" A B
    let _Val1 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "<=" _Val0 C
    let _Val2 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" A C
    let _Val3 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "<=" _Val2 B
    let _Val4 <- _orBool_ _Val1 _Val3
    let _Val5 <- «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» "+" B C
    let _Val6 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "<=" _Val5 A
    let _Val7 <- _orBool_ _Val4 _Val6
    return _Val7

noncomputable def _3f2311f : SortIntSeq → Option SortInt
  | CS => do
    let _Val0 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» CS
    let _Val1 <- «tokNds(_)_MPY-BUILTINS_IntSeq_IntSeq» CS
    let _Val2 <- «passPowE(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» _Val0 _Val1
    let _Val3 <- «passMulE(_)_MPY-BUILTINS_EvPair_EvPair» _Val2
    let _Val4 <- «passAddE(_)_MPY-BUILTINS_EvPair_EvPair» _Val3
    let _Val5 <- «firstNdE(_)_MPY-BUILTINS_Int_EvPair» _Val4
    return _Val5

noncomputable def roundFN (x0 : SortFloat) (x1 : SortInt) : Option SortFloat := (_42be4f7 x0 x1) <|> (_4dc295c x0 x1)

noncomputable def _4c60553 : SortString → SortVals → Option SortVal
  | "min", SortVals.«_,__MPY-CORE_Vals_Val_Vals» V (SortVals.«_,__MPY-CORE_Vals_Val_Vals» V2 REST) => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- isStr (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «minVals(_,_)_MPY-BUILTINS_Val_Val_Vals» V (SortVals.«_,__MPY-CORE_Vals_Val_Vals» V2 REST)
    guard _Val4
    return _Val5
  | _, _ => none

noncomputable def _9cb2b17 : SortString → SortVals → Option SortVal
  | "min", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) REST => do
    let _Val0 <- «minVals(_,_)_MPY-BUILTINS_Val_Val_Vals» ((@inj SortInt SortVal) I) REST
    return _Val0
  | _, _ => none

noncomputable def _32f1ecf : SortString → SortVals → Option SortVal
  | "max", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) REST => do
    let _Val0 <- «maxVals(_,_)_MPY-BUILTINS_Val_Val_Vals» ((@inj SortInt SortVal) I) REST
    return _Val0
  | _, _ => none

noncomputable def _c7b7019 : SortString → SortVals → Option SortVal
  | "max", SortVals.«_,__MPY-CORE_Vals_Val_Vals» V (SortVals.«_,__MPY-CORE_Vals_Val_Vals» V2 REST) => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- isStr (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «maxVals(_,_)_MPY-BUILTINS_Val_Val_Vals» V (SortVals.«_,__MPY-CORE_Vals_Val_Vals» V2 REST)
    guard _Val4
    return _Val5
  | _, _ => none

noncomputable def «invalidTriangle(_,_,_)_VERIFICATION_Bool_Val_Val_Val» (x0 : SortVal) (x1 : SortVal) (x2 : SortVal) : Option SortBool := _c91b701 x0 x1 x2

noncomputable def «evalArith(_)_MPY-BUILTINS_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := _3f2311f x0

noncomputable def _727142b : SortString → SortVals → Option SortVal
  | "round", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortFloat F) (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt N) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => do
    let _Val0 <- roundFN F N
    return ((@inj SortFloat SortVal) _Val0)
  | _, _ => none

noncomputable def _1de45ff : SortString → SortVals → Option SortVal
  | "eval", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «evalArith(_)_MPY-BUILTINS_Int_IntSeq» CS
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» (x0 : SortString) (x1 : SortVals) : Option SortVal := (_108b118 x0 x1) <|> (_1b20c41 x0 x1) <|> (_1de45ff x0 x1) <|> (_20b19cf x0 x1) <|> (_213f0c2 x0 x1) <|> (_28eddda x0 x1) <|> (_2d8e778 x0 x1) <|> (_32f1ecf x0 x1) <|> (_437b04b x0 x1) <|> (_4807966 x0 x1) <|> (_4b80f98 x0 x1) <|> (_4c60553 x0 x1) <|> (_583f938 x0 x1) <|> (_606434e x0 x1) <|> (_6d20a96 x0 x1) <|> (_6d20a96 x0 x1) <|> (_727142b x0 x1) <|> (_72eff8b x0 x1) <|> (_73630e2 x0 x1) <|> (_853fa53 x0 x1) <|> (_8f573a0 x0 x1) <|> (_9cb2b17 x0 x1) <|> (_a4fd04a x0 x1) <|> (_a971c50 x0 x1) <|> (_bb50555 x0 x1) <|> (_c7b7019 x0 x1) <|> (_d16bd47 x0 x1) <|> (_dc46a10 x0 x1) <|> (_e22316b x0 x1) <|> (_e4f0a30 x0 x1) <|> (_e64428a x0 x1) <|> (_e64428a x0 x1) <|> (_eb8c1ed x0 x1) <|> (_ecd3e5c x0 x1) <|> (_f1c888d x0 x1)

noncomputable def _39016c3 : SortVal → SortVal → SortVal → Option SortVal
  | A, B, C => do
    let _Val0 <- «invalidTriangle(_,_,_)_VERIFICATION_Bool_Val_Val_Val» A B C
    let _Val1 <- «heronProduct(_,_,_)_VERIFICATION_Val_Val_Val_Val» A B C
    let _Val2 <- «project:Float» (SortK.kseq ((@inj SortVal SortKItem) _Val1) SortK.dotk)
    let _Val3 <- sqrtF _Val2
    let _Val4 <- «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» "round" (SortVals.«_,__MPY-CORE_Vals_Val_Vals» ((@inj SortFloat SortVal) _Val3) (SortVals.«_,__MPY-CORE_Vals_Val_Vals» ((@inj SortInt SortVal) 2) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»))
    let _Val5 <- kite _Val0 ((@inj SortInt SortVal) (-1)) _Val4
    return _Val5

noncomputable def «triangleAreaSpec(_,_,_)_VERIFICATION_Val_Val_Val_Val» (x0 : SortVal) (x1 : SortVal) (x2 : SortVal) : Option SortVal := _39016c3 x0 x1 x2