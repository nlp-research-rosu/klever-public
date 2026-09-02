import Klean72WillItFly.Inj

noncomputable def _105572a : SortK → Option SortBool
  | K => some false

noncomputable def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

noncomputable def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

noncomputable def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

noncomputable def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

noncomputable def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

noncomputable def _3712fd9 : Option SortVal := some (SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int» (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "q" (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "w" SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames»)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«BoolOp(_,_)_MPY-SYNTAX_Expr_String_Exprs» "and" (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "q") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "q") (SortIndex.«Slice(_,_,_)_MPY-SYNTAX_Index_Bound_Bound_Bound» SortBound.«NoBound_MPY-SYNTAX_Bound» SortBound.«NoBound_MPY-SYNTAX_Bound» ((@inj SortExpr SortBound) (SortExpr.«UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» "-" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))))))) (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "sum") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "q") SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»)) (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<=" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "w"))) SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»)))) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») 0)

noncomputable def _495da55 : SortK → Option SortBool
  | K => some false

noncomputable def _b662ad7 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

noncomputable def _613283e : SortK → Option SortBool
  | K => some false

noncomputable def _a66427b : SortValSeq → SortInt → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0, 0 => some V
  | _, _ => none

noncomputable def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

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

axiom allIntegral (x0 : SortValSeq) : Option SortBool

axiom allNumeric (x0 : SortValSeq) : Option SortBool

noncomputable def _d74a36c : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortFloat Float) SortK.dotk => some true
  | _ => none

noncomputable def _dadad71 : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortBool Bool) SortK.dotk => some true
  | _ => none

axiom hasFloat (x0 : SortValSeq) : Option SortBool

axiom intLikeTotal (x0 : SortVal) : Option SortInt

axiom noFloatSum (x0 : SortInt) : Option SortFloat

axiom projectBoolTotal (x0 : SortVal) : Option SortBool

axiom projectFloatTotal (x0 : SortVal) : Option SortFloat

axiom projectIntTotal (x0 : SortVal) : Option SortInt

axiom sumFloatRest (x0 : SortFloat) (x1 : SortValSeq) : Option SortFloat

axiom sumInts (x0 : SortInt) (x1 : SortValSeq) : Option SortInt

axiom sumToFloat (x0 : SortInt) (x1 : SortValSeq) : Option SortFloat

noncomputable def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def «willItFlyClosure()_VERIFICATION-SYNTAX_Val» : Option SortVal := _3712fd9

mutual
  noncomputable def _5d69a53 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  noncomputable def «vsLen(_)_MPY-CORE_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_5d69a53 x0) <|> (_b662ad7 x0)
end

mutual
  noncomputable def _86fc1c7 : SortValSeq → SortInt → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S, I => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» S _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  noncomputable def «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortVal := (_86fc1c7 x0 x1) <|> (_a66427b x0 x1)
end

noncomputable def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

noncomputable def isFloat (x0 : SortK) : Option SortBool := (_d74a36c x0) <|> (_613283e x0)

noncomputable def isBool (x0 : SortK) : Option SortBool := (_dadad71 x0) <|> (_495da55 x0)

noncomputable def _1c1496e : SortValSeq → SortInt → SortInt → SortInt → Option SortValSeq
  | _Gen0, I, STOP, STEP => do
    let _Val0 <- «_>Int_» STEP 0
    let _Val1 <- «_<Int_» I STOP
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» STEP 0
    let _Val4 <- «_>Int_» I STOP
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    let _Val7 <- notBool_ _Val6
    guard _Val7
    return SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

noncomputable def _d9429a0 : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val2 <- notBool_ _Val1
    let _Val3 <- _andBool_ _Val0 _Val2
    let _Val4 <- isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val5 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val6 <- notBool_ _Val5
    let _Val7 <- _andBool_ _Val4 _Val6
    let _Val8 <- _orBool_ _Val3 _Val7
    let _Val9 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val10 <- notBool_ _Val9
    let _Val11 <- _andBool_ _Val8 _Val10
    return _Val11

noncomputable def _e3e11eb : SortVal → Option SortBool
  | V => do
    let _Val0 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val2 <- notBool_ _Val1
    let _Val3 <- _andBool_ _Val0 _Val2
    let _Val4 <- isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val5 <- notBool_ _Val4
    let _Val6 <- _andBool_ _Val3 _Val5
    return _Val6

axiom «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortValSeq
axiom _fefa459 : SortValSeq → SortInt → SortInt → SortInt → Option SortValSeq

noncomputable def «integralV(_)_VERIFICATION-SYNTAX_Bool_Val» (x0 : SortVal) : Option SortBool := _d9429a0 x0

noncomputable def «floatV(_)_VERIFICATION-SYNTAX_Bool_Val» (x0 : SortVal) : Option SortBool := _e3e11eb x0

noncomputable def _afd569b : SortValSeq → Option SortValSeq
  | VS => do
    let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
    let _Val1 <- «_+Int_» _Val0 (-1)
    let _Val2 <- «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» VS _Val1 (-1) (-1)
    return _Val2

noncomputable def reverseSlice (x0 : SortValSeq) : Option SortValSeq := _afd569b x0