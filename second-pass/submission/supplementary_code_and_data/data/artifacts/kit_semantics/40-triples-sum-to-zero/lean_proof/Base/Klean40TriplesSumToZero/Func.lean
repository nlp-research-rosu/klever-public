import Klean40TriplesSumToZero.Inj

def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _1ff7081 : Option SortExpr := some (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "j") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<" (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "len") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "l") SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))))

def _47f2e6a : Option SortStmts := some (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "l") ((@inj SortExpr SortIndex) (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "i"))) (SortExpr.«Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "l") ((@inj SortExpr SortIndex) (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "j")))) (SortExpr.«Subscript(_,_)_MPY-SYNTAX_Expr_Expr_Index» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "l") ((@inj SortExpr SortIndex) (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "k")))) (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 0))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "found") (SortExpr.«Bool(_)_MPY-SYNTAX_Expr_Bool» true)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "k") "+" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))

def _5f762f5 : Option SortExpr := some (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "k") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<" (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "len") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "l") SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))))

def _441e453 : SortIntSeq → Option SortValSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
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

def _72b6a10 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Gen0, 0 => some I
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _b1952bc : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some 0
  | _, _ => none

def _58ef342 : Option SortExpr := some (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "i") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<" (SortExpr.«Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "len") (SortExprs.«_,__MPY-SYNTAX_Exprs_Expr_Exprs» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "l") SortExprs.«.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs»))))

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

def «middleCond()_VERIFICATION_Expr» : Option SortExpr := _1ff7081

def «innerBody()_VERIFICATION_Stmts» : Option SortStmts := _47f2e6a

def «innerCond()_VERIFICATION_Expr» : Option SortExpr := _5f762f5

mutual
  def _2c6e0e1 : SortIntSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I R => do
      let _Val0 <- «intVals(_)_VERIFICATION_ValSeq_IntSeq» R
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) I) _Val0)
    | _ => none

  def «intVals(_)_VERIFICATION_ValSeq_IntSeq» (x0 : SortIntSeq) : Option SortValSeq := (_2c6e0e1 x0) <|> (_441e453 x0)
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _ebc12e0 : SortIntSeq → SortInt → Option SortBool
  | _Gen0, I => do
    let _Val0 <- «_<Int_» I 0
    guard _Val0
    return false

def _f534f41 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, N => do
    let _Val0 <- «_<Int_» N 0
    guard _Val0
    return 0
  | _, _ => none

mutual
  def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

def «outerCond()_VERIFICATION_Expr» : Option SortExpr := _58ef342

def _2c5cb1a : Option SortStmts := do
  let _Val0 <- «innerCond()_VERIFICATION_Expr»
  let _Val1 <- «innerBody()_VERIFICATION_Stmts»
  return (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "k") (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "j") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» _Val0 _Val1) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "k") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 0)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "j") "+" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))))

mutual
  def _80a0eb3 : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 R, N => do
      let _Val0 <- «_>Int_» N 0
      let _Val1 <- «_-Int_» N 1
      let _Val2 <- «intAt(_,_)_VERIFICATION_Int_IntSeq_Int» R _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  def «intAt(_,_)_VERIFICATION_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_72b6a10 x0 x1) <|> (_80a0eb3 x0 x1) <|> (_b1952bc x0 x1) <|> (_f534f41 x0 x1)
end

def _608a888 : SortIntSeq → SortInt → SortInt → SortInt → Option SortBool
  | IS, I, J, K => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_<=Int_» J I
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_<=Int_» K J
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    let _Val6 <- «_>=Int_» I _Val5
    let _Val7 <- _orBool_ _Val4 _Val6
    let _Val8 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    let _Val9 <- «_>=Int_» J _Val8
    let _Val10 <- _orBool_ _Val7 _Val9
    guard _Val10
    return false

def _935a148 : SortIntSeq → SortInt → Option SortBool
  | IS, I => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    let _Val1 <- «_>=Int_» I _Val0
    guard _Val1
    return false

def _d1a46e8 : SortIntSeq → SortInt → SortInt → SortInt → Option SortBool
  | IS, I, J, K => do
    let _Val0 <- «_<=Int_» 0 I
    let _Val1 <- «_<Int_» I J
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» J K
    let _Val4 <- _andBool_ _Val2 _Val3
    let _Val5 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    let _Val6 <- «_<Int_» J _Val5
    let _Val7 <- _andBool_ _Val4 _Val6
    let _Val8 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    let _Val9 <- «_>=Int_» K _Val8
    let _Val10 <- _andBool_ _Val7 _Val9
    guard _Val10
    return false

def _e45c47f : SortIntSeq → SortInt → SortInt → Option SortBool
  | IS, I, J => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_<=Int_» J I
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    let _Val4 <- «_>=Int_» I _Val3
    let _Val5 <- _orBool_ _Val2 _Val4
    guard _Val5
    return false

def _f28c1c2 : SortIntSeq → SortInt → SortInt → Option SortBool
  | IS, I, J => do
    let _Val0 <- «_<=Int_» 0 I
    let _Val1 <- «_<Int_» I J
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    let _Val4 <- «_>=Int_» J _Val3
    let _Val5 <- _andBool_ _Val2 _Val4
    guard _Val5
    return false

def «middleBody()_VERIFICATION_Stmts» : Option SortStmts := _2c5cb1a

axiom _385884b : SortIntSeq → SortInt → SortInt → SortInt → Option SortBool
axiom «thirdFrom(_,_,_,_)_VERIFICATION_Bool_IntSeq_Int_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortBool

def _87a52ac : Option SortStmts := do
  let _Val0 <- «middleCond()_VERIFICATION_Expr»
  let _Val1 <- «middleBody()_VERIFICATION_Stmts»
  return (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "j") (SortExpr.«BinOp(_,_,_)_MPY-SYNTAX_Expr_String_Expr_Expr» "+" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "i") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» _Val0 _Val1) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "j") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 0)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«AugAssign(_,_,_)_MPY-SYNTAX_Stmt_Expr_String_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "i") "+" (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))))

axiom «pairFrom(_,_,_)_VERIFICATION_Bool_IntSeq_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) : Option SortBool
axiom _ec0565f : SortIntSeq → SortInt → SortInt → Option SortBool

def «outerBody()_VERIFICATION_Stmts» : Option SortStmts := _87a52ac

axiom _4f302a6 : SortIntSeq → SortInt → Option SortBool
axiom «tripleFrom(_,_)_VERIFICATION_Bool_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortBool

def _3dbfbc7 : Option SortStmts := do
  let _Val0 <- «outerCond()_VERIFICATION_Expr»
  let _Val1 <- «outerBody()_VERIFICATION_Stmts»
  return (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "found") (SortExpr.«Bool(_)_MPY-SYNTAX_Expr_Bool» false)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "i") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 0)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "j") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 0)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "k") (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 0)) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«While(_,_)_MPY-SYNTAX_Stmt_Expr_Stmts» _Val0 _Val1) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "found")) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»))))))

def «programBody()_VERIFICATION_Stmts» : Option SortStmts := _3dbfbc7

def _e0f0b49 : Option SortVal := do
  let _Val0 <- «programBody()_VERIFICATION_Stmts»
  return (SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int» (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "l" SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames») _Val0 0)

def «triplesClosure()_VERIFICATION_Val» : Option SortVal := _e0f0b49

noncomputable def _c586863 : Option SortMap := do
  let _Val0 <- «triplesClosure()_VERIFICATION_Val»
  let _Val1 <- «_|->_» ((@inj SortString SortKItem) "triples_sum_to_zero") ((@inj SortVal SortKItem) _Val0)
  return _Val1

noncomputable def «solutionBindings()_VERIFICATION_Map» : Option SortMap := _c586863