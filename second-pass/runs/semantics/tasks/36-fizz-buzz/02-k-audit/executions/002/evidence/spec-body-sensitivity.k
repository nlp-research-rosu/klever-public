requires "verification.k"

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION

  // The invoked closure itself is mutated: each matching digit adds 2 rather
  // than 1. At n=78, integer 77 contributes 4, so the original result 2 must
  // no longer be provable.
  claim [mutated-body-entry-78]:
    <k>
      Call(
        closureVal(
          "n",
          Assign(Name("count"), Int(0))
          Assign(Name("i"), Int(0))
          Assign(Name("x"), Int(0))
          While(
            Compare(Name("i"), CmpOp("<", Name("n"))),
            If(
              BoolOp(
                "or",
                Compare(BinOp("%", Name("i"), Int(11)), CmpOp("==", Int(0))),
                Compare(BinOp("%", Name("i"), Int(13)), CmpOp("==", Int(0)))),
              Assign(Name("x"), Name("i"))
              While(
                Compare(Name("x"), CmpOp(">", Int(0))),
                If(
                  Compare(BinOp("%", Name("x"), Int(10)), CmpOp("==", Int(7))),
                  AugAssign(Name("count"), "+", Int(2)) .Stmts,
                  .Stmts)
                Assign(Name("x"), BinOp("//", Name("x"), Int(10)))),
              .Stmts)
            AugAssign(Name("i"), "+", Int(1)))
          Return(Name("count")),
          0),
        78)
      => 2
    </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
