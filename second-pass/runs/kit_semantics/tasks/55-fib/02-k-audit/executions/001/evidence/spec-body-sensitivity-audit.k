requires "verification.k"

module SPEC-BODY-SENSITIVITY-AUDIT
  imports VERIFICATION

  // Material body mutation: the loop computes b = a + b + 1.
  // For the satisfying input 1 this mutated program returns 2, so the
  // original-program obligation returning 1 must be rejected.
  claim [mutated-body-n1]:
    <k> Call(Name("fib"), Int(1)) => 1 </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "fib" |-> closureVal(
          "n", .ParamNames,
          Assign(Name("a"), Int(0))
          Assign(Name("b"), Int(1))
          While(
            Compare(Name("n"), CmpOp(">", Int(0))),
            Assign(
              Name("b"),
              BinOp("+", BinOp("+", Name("a"), Name("b")), Int(1))
            )
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
