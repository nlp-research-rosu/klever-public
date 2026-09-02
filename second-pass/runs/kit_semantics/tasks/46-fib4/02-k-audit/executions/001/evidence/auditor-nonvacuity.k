requires "spec.k"

module AUDITOR-NONVACUITY
  imports SPEC

  // Reviewer-authored false obligation.  The exact submitted body returns 2
  // for the satisfiable input n = 4, but this mutation demands 3.
  claim [auditor-wrong-n4]:
    <k>
      Call(Name("fib4"), Int(4))
      =>
      3
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "fib4" |-> closureVal(
          "n",
          Assign(Name("a"), Int(0))
          Assign(Name("b"), Int(0))
          Assign(Name("c"), Int(2))
          Assign(Name("d"), Int(0))
          Assign(Name("e"), Int(0))
          Assign(Name("i"), Int(0))
          While(
            Compare(Name("i"), CmpOp("<", Name("n"))),
            Assign(
              Name("e"),
              BinOp(
                "+",
                BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")),
                Name("d")))
            Assign(Name("a"), Name("b"))
            Assign(Name("b"), Name("c"))
            Assign(Name("c"), Name("d"))
            Assign(Name("d"), Name("e"))
            Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
          Return(Name("a")),
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
