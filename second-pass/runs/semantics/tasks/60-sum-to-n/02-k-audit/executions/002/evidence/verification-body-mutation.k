requires "reference-semantics/semantics.k"

module SUM-TO-N-BODY-MUTATION
  imports MPY

  // Materially changed executed body: n * (n + 2) // 2.
  syntax KItem ::= "#runSumToNBodyMut" "(" Int ")"
  rule #runSumToNBodyMut(N:Int)
    => #loadAll(
         Module(
           FuncDef(
             "sum_to_n",
             Params("n"),
             Return(
               BinOp(
                 "//",
                 BinOp("*", Name("n"), BinOp("+", Name("n"), Int(2))),
                 Int(2))))))
       ~> Call(Name("sum_to_n"), Int(N), .Exprs)

  syntax Int ::= triangularBodyMut(Int) [function, total]
  rule triangularBodyMut(N:Int)
    => (N *Int (N +Int 1) -Int pyMod(N *Int (N +Int 1), 2)) /Int 2
endmodule
