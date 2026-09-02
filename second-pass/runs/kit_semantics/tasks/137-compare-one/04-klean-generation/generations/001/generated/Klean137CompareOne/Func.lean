import Klean137CompareOne.Inj

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

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

def _076da9f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

def _fd49342 : SortValSeq → SortVal → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some false
  | _, _ => none

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

def _5dd92ea : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», A => some A
  | _, _ => none

def _e688eef : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 1
  | _ => none

def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _15eace1 : SortVal → Option SortVal
  | SortVal.inj_SortFloat F => some ((@inj SortFloat SortVal) F)
  | _ => none

def _18b010b : SortIntSeq → SortInt → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0, _Gen1 => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _, _, _ => none

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

def _282601c : SortVal → Option SortVal
  | SortVal.inj_SortInt I => some ((@inj SortInt SortVal) I)
  | _ => none

axiom «ceilFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

axiom «_==Float_» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «_==Bool_» (x0 : SortBool) (x1 : SortBool) : Option SortBool

def _364aa68 : Option SortModule := some (SortModule.«Module(_)_MPY-SYNTAX_Module_Stmts» (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» "compare_one" (SortParams.«Params(_)_MPY-SYNTAX_Params_ParamNames» (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "a" (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "b" SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames»))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "isinstance") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "str") SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a_value") (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "float") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a") "replace") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» ",") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» ".") SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))) SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a_value") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "isinstance") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "str") SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b_value") (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "float") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Attribute(_,_)_MPY-SYNTAX_Expr_Expr_String» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b") "replace") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» ",") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» ".") SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))) SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b_value") (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a_value") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» ">" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b_value"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b_value") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» ">" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "a_value"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "b")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» SortExpr.«NoneVal_MPY-SYNTAX_Expr») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)))))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))

def _4613fdc : SortValSeq → SortValSeq → SortValSeq → SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, _Gen1 => some true
  | _, _, _, _ => none

def _4b7fd38 : SortBool → Option SortInt
  | false => some 0
  | _ => none

def _73f627a : SortBool → Option SortInt
  | true => some 1
  | _ => none

def _80a1ae7 : SortInt → SortIntSeq → Option SortBool
  | _Gen0, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

axiom «_-Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «_+Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «_/Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

def _b48ab39 : SortIntSeq → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _Gen0 => some C
  | _ => none

def _b662ad7 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

def _c71764f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _f3f7875 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1 => some true
  | _, _ => none

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

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _b37e75d : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_==Int_» I1 I2
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

def _0ae23e4 : SortString → SortVal → SortVal → Option SortBool
  | ">=", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_>=Int_» I1 I2
    return _Val0
  | _, _, _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def _fee1f6e : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_>Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

noncomputable def _5667141 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_<Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

def _41490e6 : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_<Int_» I1 I2
    return _Val0
  | _, _, _ => none

def _c875e09 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_<Int_» A B
    guard _Val0
    return true
  | _, _ => none

noncomputable def _e5f1d08 : SortInt → Option SortFloat
  | I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    return _Val0

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

def _6b454b2 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_>Int_» I1 I2
    return _Val0
  | _, _, _ => none

def _cc09b1d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_>Int_» A B
    guard _Val0
    return false
  | _, _ => none

noncomputable def _3994b91 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0

noncomputable def _b558675 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0
  | _, _, _ => none

noncomputable def _9e5ad0c : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortBool B1, SortVal.inj_SortBool B2 => do
    let _Val0 <- «_==Bool_» B1 B2
    return _Val0
  | _, _, _ => none

def «solutionModule()_VERIFICATION_Module» : Option SortModule := _364aa68

def «boolAsInt(_)_MPY-CORE_Int_Bool» (x0 : SortBool) : Option SortInt := (_4b7fd38 x0) <|> (_73f627a x0)

def «headIS(_)_MPY-FLOAT_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := _b48ab39 x0

mutual
  def _5d69a53 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «vsLen(_)_MPY-CORE_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_5d69a53 x0) <|> (_b662ad7 x0)
end

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

mutual
  def «replaceC(_,_,_)_MPY-METHODS_IntSeq_IntSeq_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) : Option SortIntSeq := (_18b010b x0 x1 x2) <|> (_b5057da x0 x1 x2) <|> (_f58851d x0 x1 x2)

  def _b5057da : SortIntSeq → SortInt → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, A, B => do
      let _Val0 <- «_==Int_» C A
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «replaceC(_,_,_)_MPY-METHODS_IntSeq_IntSeq_Int_Int» R A B
      guard _Val1
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _Val2)
    | _, _, _ => none

  def _f58851d : SortIntSeq → SortInt → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, A, B => do
      let _Val0 <- «_==Int_» C A
      let _Val1 <- «replaceC(_,_,_)_MPY-METHODS_IntSeq_IntSeq_Int_Int» R A B
      guard _Val0
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B _Val1)
    | _, _, _ => none
end

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

def _6ef1389 : SortIntSeq → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 R => do
    let _Val0 <- «fracAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» R 0
    return _Val0
  | _ => none

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

noncomputable def gtF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _fee1f6e x0 x1

noncomputable def floatLt (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _5667141 x0 x1

noncomputable def intToF (x0 : SortInt) : Option SortFloat := _e5f1d08 x0

def _c02b510 : SortIntSeq → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 R => do
    let _Val0 <- «fscAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» R 1
    return _Val0
  | _ => none

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

noncomputable def eqF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _3994b91 x0 x1

noncomputable def «_=/=Bool_» (x0 : SortBool) (x1 : SortBool) : Option SortBool := _31fe72e x0 x1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

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

noncomputable def «isEqOrdOp(_)_MPY-CORE_Bool_String» (x0 : SortString) : Option SortBool := _1ab1a90 x0

noncomputable def «isInfinite(_)_FLOAT_Bool_Float» (x0 : SortFloat) : Option SortBool := _3cdc559 x0

noncomputable def «isOrdOp(_)_MPY-CORE_Bool_String» (x0 : SortString) : Option SortBool := _8ca426b x0

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

noncomputable def _9a8a33a : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» KS1 VS1, SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» KS2 VS2 => do
    let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» KS1
    let _Val1 <- «vsLen(_)_MPY-CORE_Int_ValSeq» KS2
    let _Val2 <- «_==Int_» _Val0 _Val1
    let _Val3 <- «dSubset(_,_,_,_)_MPY-DICT_Bool_ValSeq_ValSeq_ValSeq_ValSeq» KS1 VS1 KS2 VS2
    let _Val4 <- _andBool_ _Val2 _Val3
    return _Val4
  | _, _, _ => none

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

noncomputable def _6a82bc3 : SortFloat → Option SortBool
  | F => do
    let _Val0 <- «isNaN(_)_FLOAT_Bool_Float» F
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «isInfinite(_)_FLOAT_Bool_Float» F
    let _Val3 <- notBool_ _Val2
    let _Val4 <- _andBool_ _Val1 _Val3
    return _Val4

def _d3d248d : SortIntSeq → SortIntSeq → Option SortBool
  | A, B => do
    let _Val0 <- «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» A B
    let _Val1 <- «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» B A
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

def _0bf42d3 : SortIntSeq → Option SortInt
  | CS => do
    let _Val0 <- «intPartAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» CS 0
    return _Val0

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

def «sameSet(_,_)_MPY-SET_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := _d3d248d x0 x1

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

def _87bf7c6 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.«setV(_)_MPY-SET_Val_IntSeq» A, SortVal.«setV(_)_MPY-SET_Val_IntSeq» B => do
    let _Val0 <- «sameSet(_,_)_MPY-SET_Bool_IntSeq_IntSeq» A B
    return _Val0
  | _, _, _ => none

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

noncomputable def _5750ede : SortVal → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» C) => do
    let _Val0 <- «replaceC(_,_,_)_MPY-METHODS_IntSeq_IntSeq_Int_Int» C 44 46
    let _Val1 <- decStrToF _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _ => none

axiom _7602aea : SortString → SortVal → SortVal → Option SortBool
axiom _9669df5 : SortString → SortVal → SortVal → Option SortBool
axiom _9a4e525 : SortString → SortVal → SortVal → Option SortBool
axiom _9fe303a : SortString → SortVal → SortVal → Option SortBool
axiom «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» (x0 : SortString) (x1 : SortVal) (x2 : SortVal) : Option SortBool
axiom _cb210bb : SortString → SortVal → SortVal → Option SortBool

noncomputable def «numericValue(_)_VERIFICATION_Val_Val» (x0 : SortVal) : Option SortVal := (_15eace1 x0) <|> (_282601c x0) <|> (_5750ede x0)

noncomputable def _39d2932 : SortVal → SortVal → Option SortVal
  | A, B => do
    let _Val0 <- «numericValue(_)_VERIFICATION_Val_Val» A
    let _Val1 <- «numericValue(_)_VERIFICATION_Val_Val» B
    let _Val2 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" _Val0 _Val1
    let _Val3 <- notBool_ _Val2
    let _Val4 <- «numericValue(_)_VERIFICATION_Val_Val» B
    let _Val5 <- «numericValue(_)_VERIFICATION_Val_Val» A
    let _Val6 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" _Val4 _Val5
    let _Val7 <- _andBool_ _Val3 _Val6
    guard _Val7
    return B

noncomputable def _94b3baa : SortVal → SortVal → Option SortVal
  | A, B => do
    let _Val0 <- «numericValue(_)_VERIFICATION_Val_Val» A
    let _Val1 <- «numericValue(_)_VERIFICATION_Val_Val» B
    let _Val2 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" _Val0 _Val1
    let _Val3 <- notBool_ _Val2
    let _Val4 <- «numericValue(_)_VERIFICATION_Val_Val» B
    let _Val5 <- «numericValue(_)_VERIFICATION_Val_Val» A
    let _Val6 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" _Val4 _Val5
    let _Val7 <- notBool_ _Val6
    let _Val8 <- _andBool_ _Val3 _Val7
    guard _Val8
    return SortVal.«noneV_MPY-CORE_Val»

noncomputable def _b456268 : SortVal → SortVal → Option SortVal
  | A, B => do
    let _Val0 <- «numericValue(_)_VERIFICATION_Val_Val» A
    let _Val1 <- «numericValue(_)_VERIFICATION_Val_Val» B
    let _Val2 <- «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» ">" _Val0 _Val1
    guard _Val2
    return A

noncomputable def «expectedCompare(_,_)_VERIFICATION_Val_Val_Val» (x0 : SortVal) (x1 : SortVal) : Option SortVal := (_39d2932 x0 x1) <|> (_94b3baa x0 x1) <|> (_b456268 x0 x1)