import Klean94Skjkasdkd.Inj

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _47f3cfa : SortVals → Option SortInt
  | SortVals.«.List{"_,__SEMANTIC_Vals_Val_Vals"}_Vals» => some 0
  | _ => none

def _e1c1f1a : SortVals → Option SortInt
  | SortVals.«_,__SEMANTIC_Vals_Val_Vals» (SortVal.«intVal(_)_SEMANTIC_Val_Int» N) _VS => some N
  | _ => none

def _01a68b1 : SortVals → Option SortVals
  | SortVals.«_,__SEMANTIC_Vals_Val_Vals» (SortVal.«intVal(_)_SEMANTIC_Val_Int» _N) VS => some VS
  | _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _c07afb4 : SortStmts → Option SortMap
  | SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» => do
    let _Val0 <- «.Map»
    return _Val0
  | _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _94b50c5 : SortInt → SortInt → Option SortBool
  | N, D => do
    let _Val0 <- «_*Int_» D D
    let _Val1 <- «_>Int_» _Val0 N
    guard _Val1
    return true

def _8b27b9d : SortInt → Option SortBool
  | N => do
    let _Val0 <- «_<Int_» N 2
    guard _Val0
    return false

def _5b4545e : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<Int_» N 10
    guard _Val0
    return N

mutual
  def _5f804ac : SortVals → Option SortInt
    | SortVals.«_,__SEMANTIC_Vals_Val_Vals» _V VS => do
      let _Val0 <- «valLength(_)_SEMANTIC_Int_Vals» VS
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «valLength(_)_SEMANTIC_Int_Vals» (x0 : SortVals) : Option SortInt := (_47f3cfa x0) <|> (_5f804ac x0)
end

def «intHead(_)_SEMANTIC_Int_Vals» (x0 : SortVals) : Option SortInt := _e1c1f1a x0

def «intTail(_)_SEMANTIC_Vals_Vals» (x0 : SortVals) : Option SortVals := _01a68b1 x0

noncomputable def _0535fbc : SortInt → SortInt → Option SortBool
  | N, D => do
    let _Val0 <- «_*Int_» D D
    let _Val1 <- «_<=Int_» _Val0 N
    let _Val2 <- «_%Int_» N D
    let _Val3 <- «_==Int_» _Val2 0
    let _Val4 <- _andBool_ _Val1 _Val3
    guard _Val4
    return false

mutual
  noncomputable def _87c6dcf : SortStmts → Option SortMap
    | SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» F P B) REST => do
      let _Val0 <- «_|->_» ((@inj SortString SortKItem) F) ((@inj SortDef SortKItem) (SortDef.«def(_,_)_SEMANTIC_Def_Params_Stmts» P B))
      let _Val1 <- «collectDefs(_)_SEMANTIC_Map_Stmts» REST
      let _Val2 <- _Map_ _Val0 _Val1
      return _Val2
    | _ => none

  noncomputable def «collectDefs(_)_SEMANTIC_Map_Stmts» (x0 : SortStmts) : Option SortMap := (_87c6dcf x0) <|> (_c07afb4 x0)
end

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

axiom «refDigitSum(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt
axiom _c58705e : SortInt → Option SortInt

def _a91d3c4 : SortVals → Option SortInt
  | VS => do
    let _Val0 <- «valLength(_)_SEMANTIC_Int_Vals» VS
    let _Val1 <- «_==Int_» _Val0 0
    guard _Val1
    return 0

noncomputable def _e7a12df : SortPgm → Option SortMap
  | SortPgm.«Module(_)_MPY-SYNTAX_Pgm_Stmts» SS => do
    let _Val0 <- «collectDefs(_)_SEMANTIC_Map_Stmts» SS
    return _Val0

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def «programDefs(_)_VERIFICATION_Map_Pgm» (x0 : SortPgm) : Option SortMap := _e7a12df x0

axiom _1c63a14 : SortInt → SortInt → Option SortBool
axiom «refPrimeFrom(_,_)_VERIFICATION_Bool_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortBool

noncomputable def _aa65234 : SortInt → Option SortBool
  | N => do
    let _Val0 <- «_>=Int_» N 2
    let _Val1 <- «refPrimeFrom(_,_)_VERIFICATION_Bool_Int_Int» N 2
    guard _Val0
    return _Val1

noncomputable def «refPrime(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := (_8b27b9d x0) <|> (_aa65234 x0)

noncomputable def _7dfabd2 : SortInt → SortInt → Option SortInt
  | N, BEST => do
    let _Val0 <- «refPrime(_)_VERIFICATION_Bool_Int» N
    let _Val1 <- «_>Int_» N BEST
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return N

noncomputable def _4bf9165 : SortInt → SortInt → Option SortInt
  | N, BEST => do
    let _Val0 <- «refPrime(_)_VERIFICATION_Bool_Int» N
    let _Val1 <- «_>Int_» N BEST
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- notBool_ _Val2
    guard _Val3
    return BEST

noncomputable def «refChoose(_,_)_VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_4bf9165 x0 x1) <|> (_7dfabd2 x0 x1)

axiom _409fb10 : SortVals → Option SortInt
axiom «refLargest(_)_VERIFICATION_Int_Vals» (x0 : SortVals) : Option SortInt

noncomputable def _2d33076 : SortVals → Option SortInt
  | VS => do
    let _Val0 <- «refLargest(_)_VERIFICATION_Int_Vals» VS
    let _Val1 <- «refDigitSum(_)_VERIFICATION_Int_Int» _Val0
    return _Val1

noncomputable def «refAnswer(_)_VERIFICATION_Int_Vals» (x0 : SortVals) : Option SortInt := _2d33076 x0