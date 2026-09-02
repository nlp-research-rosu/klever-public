requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false result obligation. This is the exact submitted closure, and
  // input 8 satisfies the entry domain. The real result is 21, not 22.
  claim [fib-eight-is-twenty-two]:
    <k> Call(Name("fib"), Int(8)) => 22 </k>
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
