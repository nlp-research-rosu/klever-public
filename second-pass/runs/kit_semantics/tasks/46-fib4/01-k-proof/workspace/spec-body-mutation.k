requires "spec.k"

module SPEC-BODY-MUTATION
  imports SPEC

  // Material mutation: c starts at 3 instead of 2.  At n = 2 this body returns
  // 3, so the original contract result 2 must no longer be provable.
  claim [mutated-body-rejected]:
    <k>
      Call(Name("fib4"), Int(2))
      =>
      2
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "fib4" |-> closureVal(
          "n",
          Assign(Name("a"), Int(0))
          Assign(Name("b"), Int(0))
          Assign(Name("c"), Int(3))
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
