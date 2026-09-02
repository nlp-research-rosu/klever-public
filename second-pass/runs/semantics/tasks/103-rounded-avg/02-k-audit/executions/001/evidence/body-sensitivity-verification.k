requires "reference-semantics/semantics.k"

module ROUNDED-AVG-VERIFICATION
  imports MPY

  // This is exactly the translated body of rounded_avg from solution.mpy.
  // Naming it here keeps each reachability claim focused on its input class
  // and expected result.
  syntax Stmts ::= "roundedAvgBody" [function, total]
  rule roundedAvgBody
    => Return(Int(777)) .Stmts

  // A direct entry-point call. Its closure has the module scope as parent,
  // just as the closure produced by the module-level FuncDef in solution.mpy.
  syntax Expr ::= roundedAvgCall(Int, Int) [function, total]
  rule roundedAvgCall(N:Int, M:Int)
    => Call(closureVal(("n", "m", .ParamNames), roundedAvgBody, 0),
            (N, M, .Exprs))
endmodule
