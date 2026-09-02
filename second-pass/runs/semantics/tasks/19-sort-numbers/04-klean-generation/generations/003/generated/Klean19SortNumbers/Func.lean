import Klean19SortNumbers.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _218dc3a : SortString → Option SortIntSeq
  | "" => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

def _a90d83e : SortNumWords → Option SortValSeq
  | SortNumWords.«.NumWords_SORT-NUMBERS-VERIFICATION_NumWords» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

def _2e9dd52 : SortIntSeq → SortValSeq → Option SortIntSeq
  | _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some CS
  | _, _ => none

def _553ef43 : SortIntSeq → SortValSeq → Option SortIntSeq
  | _Gen0, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _, _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

axiom sortKeyVS (x0 : SortValSeq) (x1 : SortVal) : Option SortValSeq

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

noncomputable def _f390a9b : SortString → SortString → Option SortBool
  | S1, S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    let _Val1 <- notBool_ _Val0
    return _Val1

mutual
  def _6dbca3c : SortIntSeq → SortValSeq → Option SortIntSeq
    | SEP, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R) => do
      let _Val0 <- «joinCodes(_,_)_MPY-METHODS_IntSeq_IntSeq_ValSeq» SEP (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R)
      let _Val1 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» SEP _Val0
      let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» CS _Val1
      return _Val2
    | _, _ => none

  def «joinCodes(_,_)_MPY-METHODS_IntSeq_IntSeq_ValSeq» (x0 : SortIntSeq) (x1 : SortValSeq) : Option SortIntSeq := (_2e9dd52 x0 x1) <|> (_553ef43 x0 x1) <|> (_6dbca3c x0 x1)
end

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

noncomputable def _1a533b9 : SortNumWord → Option SortVal
  | SortNumWord.«eightW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "eight"
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _ => none

noncomputable def _1cd5e1b : SortNumWord → Option SortVal
  | SortNumWord.«zeroW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "zero"
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _ => none

noncomputable def _24e16b3 : SortNumWord → Option SortVal
  | SortNumWord.«fourW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "four"
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _ => none

noncomputable def _27bd5b3 : SortNumWord → Option SortVal
  | SortNumWord.«threeW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "three"
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _ => none

noncomputable def _36c95ba : SortNumWord → Option SortVal
  | SortNumWord.«oneW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "one"
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _ => none

noncomputable def _74776e9 : SortNumWord → Option SortVal
  | SortNumWord.«nineW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "nine"
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _ => none

noncomputable def _90958b2 : SortNumWord → Option SortIntSeq
  | SortNumWord.«sevenW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "seven"
    return _Val0
  | _ => none

noncomputable def _a6a895e : SortNumWord → Option SortIntSeq
  | SortNumWord.«fiveW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "five"
    return _Val0
  | _ => none

noncomputable def _a75d6e5 : SortNumWord → Option SortIntSeq
  | SortNumWord.«fourW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "four"
    return _Val0
  | _ => none

noncomputable def _b388e2b : SortNumWord → Option SortIntSeq
  | SortNumWord.«twoW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "two"
    return _Val0
  | _ => none

noncomputable def _b7c2b0d : SortNumWord → Option SortIntSeq
  | SortNumWord.«eightW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "eight"
    return _Val0
  | _ => none

noncomputable def _ba11eb5 : SortNumWord → Option SortVal
  | SortNumWord.«sixW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "six"
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _ => none

noncomputable def _bd5a99b : SortNumWord → Option SortIntSeq
  | SortNumWord.«nineW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "nine"
    return _Val0
  | _ => none

noncomputable def _cdaf2ba : SortNumWord → Option SortIntSeq
  | SortNumWord.«zeroW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "zero"
    return _Val0
  | _ => none

noncomputable def _d1e8222 : SortNumWord → Option SortIntSeq
  | SortNumWord.«threeW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "three"
    return _Val0
  | _ => none

noncomputable def _dcf8276 : SortNumWord → Option SortVal
  | SortNumWord.«fiveW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "five"
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _ => none

noncomputable def _f001551 : SortNumWord → Option SortIntSeq
  | SortNumWord.«oneW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "one"
    return _Val0
  | _ => none

noncomputable def _f3e65bb : SortNumWord → Option SortVal
  | SortNumWord.«sevenW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "seven"
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _ => none

noncomputable def _fef0520 : SortNumWord → Option SortVal
  | SortNumWord.«twoW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "two"
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _ => none

noncomputable def _ff53890 : SortNumWord → Option SortIntSeq
  | SortNumWord.«sixW_SORT-NUMBERS-VERIFICATION_NumWord» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "six"
    return _Val0
  | _ => none

noncomputable def «wordVal(_)_SORT-NUMBERS-VERIFICATION_Val_NumWord» (x0 : SortNumWord) : Option SortVal := (_1a533b9 x0) <|> (_1cd5e1b x0) <|> (_24e16b3 x0) <|> (_27bd5b3 x0) <|> (_36c95ba x0) <|> (_74776e9 x0) <|> (_ba11eb5 x0) <|> (_dcf8276 x0) <|> (_f3e65bb x0) <|> (_fef0520 x0)

noncomputable def «wordCodes(_)_SORT-NUMBERS-VERIFICATION_IntSeq_NumWord» (x0 : SortNumWord) : Option SortIntSeq := (_90958b2 x0) <|> (_a6a895e x0) <|> (_a75d6e5 x0) <|> (_b388e2b x0) <|> (_b7c2b0d x0) <|> (_bd5a99b x0) <|> (_cdaf2ba x0) <|> (_d1e8222 x0) <|> (_f001551 x0) <|> (_ff53890 x0)

mutual
  noncomputable def _00327d7 : SortNumWords → Option SortValSeq
    | SortNumWords.«nw(_,_)_SORT-NUMBERS-VERIFICATION_NumWords_NumWord_NumWords» W WORDS => do
      let _Val0 <- «wordVal(_)_SORT-NUMBERS-VERIFICATION_Val_NumWord» W
      let _Val1 <- «wordsVS(_)_SORT-NUMBERS-VERIFICATION_ValSeq_NumWords» WORDS
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Val0 _Val1)
    | _ => none

  noncomputable def «wordsVS(_)_SORT-NUMBERS-VERIFICATION_ValSeq_NumWords» (x0 : SortNumWords) : Option SortValSeq := (_00327d7 x0) <|> (_a90d83e x0)
end

noncomputable def _bc1f072 : SortNumWords → Option SortVal
  | WORDS => do
    let _Val0 <- «wordsVS(_)_SORT-NUMBERS-VERIFICATION_ValSeq_NumWords» WORDS
    let _Val1 <- sortKeyVS _Val0 (SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int» (SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» "word" SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "zero"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 0)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "one"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "two"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 2)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "three"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 3)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "four"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 4)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "five"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 5)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "six"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 6)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "seven"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 7)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«If(_,_,_)_MPY-SYNTAX_Stmt_Expr_Stmts_Stmts» (SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp» (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "word") (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "==" (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "eight"))) (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 8)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts») (SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«Return(_)_MPY-SYNTAX_Stmt_Expr» (SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 9)) SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)))))))))) 0)
    let _Val2 <- «joinCodes(_,_)_MPY-METHODS_IntSeq_IntSeq_ValSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») _Val1
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val2))

noncomputable def «numericOutput(_)_SORT-NUMBERS-VERIFICATION_Val_NumWords» (x0 : SortNumWords) : Option SortVal := _bc1f072 x0