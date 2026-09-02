requires "verification.k"

module FALSE-RESULT-SPEC
  imports VERIFICATION

  // Fresh result mutation: the real submitted module returns 1 at ARG=2,
  // while this destination requires fibMath(2)+1 = 2.
  claim [actual-module-off-by-one-must-fail]:
    <k>
      Module(
        FuncDef("fib", Params("n"),
          If(Compare(Name("n"), CmpOp("<=", Int(1))),
            Return(Name("n")),
            .Stmts)
          Return(BinOp("+",
            Call(Name("fib"), BinOp("-", Name("n"), Int(1))),
            Call(Name("fib"), BinOp("-", Name("n"), Int(2)))))))
      => fibMath(2) +Int 1
    </k>
    <arg> 2 </arg>
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
