requires "verification.k"

module CONTEXT-SPEC
  imports VERIFICATION

  // Ground, bridge-free fixed-semantics witness with an observable continuation.
  claim [ground-continuation]:
    <k> invoke("fib", 5) ~> applyBin("+", 100) => 105 </k>
    <arg> 99 </arg>
    <env> "sentinel" |-> 42 </env>
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
endmodule
