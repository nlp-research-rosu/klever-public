requires "verification.k"

module MUTATION-SPEC
  imports VERIFICATION

  // This deliberately false target is used only to show that the proof is
  // sensitive to an off-by-one error in the claimed result.
  claim [off-by-one-must-fail]:
    <k> invoke("fib", N) => fibMath(N) +Int 1 </k>
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
endmodule
