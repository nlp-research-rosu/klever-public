requires "verification.k"

module SPEC
  imports VERIFICATION

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

  claim [fib-module]:
    <k>
      Module(
        FuncDef("fib", Params("n"),
          If(Compare(Name("n"), CmpOp("<=", Int(1))),
            Return(Name("n")),
            .Stmts)
          Return(BinOp("+",
            Call(Name("fib"), BinOp("-", Name("n"), Int(1))),
            Call(Name("fib"), BinOp("-", Name("n"), Int(2)))))))
      => fibMath(N)
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
