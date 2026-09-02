import Klean115MaxFill.Inj

axiom «.Map» : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

noncomputable def _7a614a7 : SortStmts → Option SortMap
  | SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts» => do
    let _Val0 <- «.Map»
    return _Val0
  | _ => none

mutual
  noncomputable def _610a34a : SortStmts → Option SortMap
    | SortStmts.«___MPY-SYNTAX_Stmts_Stmt_Stmts» (SortStmt.«FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts» F P BODY) REST => do
      let _Val0 <- «_|->_» ((@inj SortString SortKItem) F) ((@inj SortFunction SortKItem) (SortFunction.«function(_,_)_MPY_Function_Params_Stmts» P BODY))
      let _Val1 <- «collectFunctions(_)_MPY_Map_Stmts» REST
      let _Val2 <- _Map_ _Val0 _Val1
      return _Val2
    | _ => none

  noncomputable def «collectFunctions(_)_MPY_Map_Stmts» (x0 : SortStmts) : Option SortMap := (_610a34a x0) <|> (_7a614a7 x0)
end

noncomputable def _faebd63 : SortModule → Option SortMap
  | SortModule.«Module(_)_MPY-SYNTAX_Module_Stmts» SS => do
    let _Val0 <- «collectFunctions(_)_MPY_Map_Stmts» SS
    return _Val0

noncomputable def «functionsOf(_)_VERIFICATION_Map_Module» (x0 : SortModule) : Option SortMap := _faebd63 x0