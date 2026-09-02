requires "verification.k"

module BODY-MUTATION-SPEC
  imports VERIFICATION

  // The executed module itself has a changed base case and is false at ARG=0.
  claim [changed-body-must-fail]:
    <k>
      Module(
        FuncDef("fib", Params("n"),
          If(Compare(Name("n"), CmpOp("<=", Int(1))),
            Return(BinOp("+", Name("n"), Int(1))),
            .Stmts)
          Return(BinOp("+",
            Call(Name("fib"), BinOp("-", Name("n"), Int(1))),
            Call(Name("fib"), BinOp("-", Name("n"), Int(2)))))))
      => fibMath(0)
    </k>
    <arg> 0 </arg>
    <env> .Map </env>
    <functions>
      .Map
      => "fib" |-> function("n",
           If(Compare(Name("n"), CmpOp("<=", Int(1))),
             Return(BinOp("+", Name("n"), Int(1))),
             .Stmts)
           Return(BinOp("+",
             Call(Name("fib"), BinOp("-", Name("n"), Int(1))),
             Call(Name("fib"), BinOp("-", Name("n"), Int(2))))))
    </functions>
    [all-path]
endmodule
