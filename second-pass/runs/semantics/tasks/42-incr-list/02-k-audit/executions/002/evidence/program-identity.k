requires "verification.k"

module PROGRAM-IDENTITY
  imports VERIFICATION

  // The right-hand term is the trusted translator's regenerated constructor
  // tree for /candidate/solution.py.
  claim [program-identity]:
    <k>
      #loadAll(solutionProgram)
      =>
      #loadAll(
        Module(
          FuncDef("incr_list", Params("l"),
            Expr(Str("Return list with elements incremented by 1."))
            Assign(Name("result"), ListExpr(.Exprs))
            For(Name("x"), Name("l"),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  BinOp("+", Name("x"), Int(1)))))
            Return(Name("result"))
            .Stmts)))
    </k>
endmodule
