requires "verification.k"

module GROUND-WITNESSES
  imports VERIFICATION

  // Satisfies the invocation claim with a nonempty saved environment and a
  // continuation that consumes the returned integer.
  claim [invoke-n2-context]:
    <k> invoke("fib", 2) ~> evalRight("+", Int(10)) => 11 </k>
    <arg> 99 </arg>
    <env> "saved" |-> 7 </env>
    <functions>
      "fib" |-> function("n",
        If(Compare(Name("n"), CmpOp("<=", Int(1))),
          Return(Name("n")),
          .Stmts)
        Return(BinOp("+",
          Call(Name("fib"), BinOp("-", Name("n"), Int(1))),
          Call(Name("fib"), BinOp("-", Name("n"), Int(2))))))
    </functions>
    [all-path]

  // Satisfies the exact-module claim at a documented input.
  claim [module-n8]:
    <k>
      Module(
        FuncDef("fib", Params("n"),
          If(Compare(Name("n"), CmpOp("<=", Int(1))),
            Return(Name("n")),
            .Stmts)
          Return(BinOp("+",
            Call(Name("fib"), BinOp("-", Name("n"), Int(1))),
            Call(Name("fib"), BinOp("-", Name("n"), Int(2)))))))
      => 21
    </k>
    <arg> 8 </arg>
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
    [all-path]
endmodule
