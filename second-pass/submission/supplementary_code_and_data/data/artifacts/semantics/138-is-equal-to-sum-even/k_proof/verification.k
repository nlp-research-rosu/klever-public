requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Invoke the closure denoted by the sole FuncDef in solution.mpy.  Constructing
  // the closure directly avoids leaving its module-level name binding behind in
  // the final state; Call, argument binding, Return, and frame cleanup still run
  // through the supplied Python semantics.
  syntax KItem ::= "#isEqualToSumEven" "(" Int ")"

  rule <k> #isEqualToSumEven(N:Int)
        => Call(
             closureVal(
               ("n", .ParamNames),
               (Return(
                  BoolOp(
                    "and",
                    ( Compare(Name("n"), CmpOp(">=", Int(8)))
                    , Compare(
                        BinOp("%", Name("n"), Int(2)),
                        CmpOp("==", Int(0)))
                    , .Exprs)))
                .Stmts),
               0),
             (N, .Exprs))
           ... </k>
endmodule
