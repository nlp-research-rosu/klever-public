requires "reference-semantics/semantics.k"

module SUM-TO-N-VERIFICATION
  imports MPY

  // The generated solution.mpy term, followed by a call of its entry point.
  syntax KItem ::= "#runSumToN" "(" Int ")"
  rule #runSumToN(N:Int)
    => #loadAll(
         Module(
           FuncDef(
             "sum_to_n",
             Params("n"),
             Return(
               BinOp(
                 "//",
                 BinOp("*", Name("n"), BinOp("+", Name("n"), Int(1))),
                 Int(2))))))
       ~> Call(Name("sum_to_n"), Int(N), .Exprs)

  // Mathematical triangular number.  This spells floor division exactly as
  // the supplied Python semantics does.  For N >= 0, N * (N + 1) is even, so
  // this is the standard N * (N + 1) / 2 closed form.
  syntax Int ::= triangular(Int) [function, total]
  rule triangular(N:Int)
    => (N *Int (N +Int 1) -Int pyMod(N *Int (N +Int 1), 2)) /Int 2
endmodule
