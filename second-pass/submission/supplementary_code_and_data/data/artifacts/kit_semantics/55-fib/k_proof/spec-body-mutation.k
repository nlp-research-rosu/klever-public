requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately changed initialization: a = 1.  The original result 0 for
  // input 0 must no longer be provable.
  claim [mutated-fib-zero-is-zero]:
    <k> Call(Name("fib"), Int(0)) => 0 </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "fib" |-> closureVal(
          "n", .ParamNames,
          Assign(Name("a"), Int(1))
          Assign(Name("b"), Int(1))
          While(
            Compare(Name("n"), CmpOp(">", Int(0))),
            Assign(Name("b"), BinOp("+", Name("a"), Name("b")))
            Assign(Name("a"), BinOp("-", Name("b"), Name("a")))
            Assign(Name("n"), BinOp("-", Name("n"), Int(1)))
          )
          Return(Name("a"))
          .Stmts,
          0
        ),
        parent(-1)
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
