requires "verification.k"

module BODY-MUTANT-AUDIT
  imports VERIFICATION

  syntax Stmts ::= "auditMutantBody" [macro]
  rule auditMutantBody => Return(TupleExpr(.Exprs))

  syntax Module ::= "auditMutantModule" [macro]
  rule auditMutantModule =>
    Module(FuncDef("bf", Params("planet1", "planet2"), auditMutantBody))
endmodule
