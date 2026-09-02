requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Unchanged supporting lemma, included so the mutated module target follows
  // the same real recursive control flow as the positive proof.
  claim [fib-invoke]:
    <k> invoke("fib", N) ~> REST => fibMath(N) ~> REST </k>
    <arg> _A </arg>
    <env> _RHO </env>
    <functions>
      "fib" |-> function("n",
        If(Compare(Name("n"), CmpOp("<=", Int(1))),
          Return(Name("n")),
          .Stmts)
        Return(BinOp("+",
          Call(Name("fib"), BinOp("-", Name("n"), Int(1))),
          Call(Name("fib"), BinOp("-", Name("n"), Int(2))))))
    </functions>
    requires N >=Int 0
    [all-path]

  // Fresh false mutation: at N=0 the real program and fibMath both return 0,
  // but this target requires the result to be 1.
  claim [fib-module-off-by-one]:
    <k>
      Module(
        FuncDef("fib", Params("n"),
          If(Compare(Name("n"), CmpOp("<=", Int(1))),
            Return(Name("n")),
            .Stmts)
          Return(BinOp("+",
            Call(Name("fib"), BinOp("-", Name("n"), Int(1))),
            Call(Name("fib"), BinOp("-", Name("n"), Int(2)))))))
      => fibMath(N) +Int 1
    </k>
    <arg> N </arg>
    <env> .Map </env>
    <functions>
      .Map
      => "fib" |-> function("n",
           If(Compare(Name("n"), CmpOp("<=", Int(1))),
             Return(Name("n")),
             .Stmts)
           Return(BinOp("+",
             Call(Name("fib"), BinOp("-", Name("n"), Int(1))),
             Call(Name("fib"), BinOp("-", Name("n"), Int(2))))))
    </functions>
    requires N >=Int 0
    [all-path]
endmodule
