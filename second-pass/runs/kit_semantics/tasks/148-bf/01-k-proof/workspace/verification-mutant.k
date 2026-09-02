requires "verification.k"

module MUTATION
  imports VERIFICATION

  // Body-sensitivity probe: same binding and signature, but a materially
  // changed body that always returns the empty tuple.
  syntax Stmts ::= "mutantBody" [macro]
  rule mutantBody => Return(TupleExpr(.Exprs))

  syntax Module ::= "mutantModule" [macro]
  rule mutantModule =>
    Module(FuncDef("bf", Params("planet1", "planet2"), mutantBody))
endmodule
