requires "verification.k"

module REVIEWER-BODY-MUTATION
  imports VERIFICATION

  // Fresh program-body mutation: return c rather than a.  At N=1 this
  // executed program returns 1, while the original theorem requires F(1)=0.
  claim [return-c-is-not-original-fibfib]:
    <k>
      #loadAll(Module(
        FuncDef(
          "fibfib",
          Params("n"),
          Assign(Name("a"), Int(0))
          Assign(Name("b"), Int(0))
          Assign(Name("c"), Int(1))
          Assign(Name("i"), Int(0))
          Assign(Name("next_value"), Int(1))
          While(
            Compare(Name("i"), CmpOp("<", Name("n"))),
            Assign(
              Name("next_value"),
              BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")))
            Assign(Name("a"), Name("b"))
            Assign(Name("b"), Name("c"))
            Assign(Name("c"), Name("next_value"))
            Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
            .Stmts)
          Return(Name("c"))
          .Stmts)))
      ~> Call(Name("fibfib"), Int(1))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
      =>
      -1 |-> builtinsScope
      0 |-> scope(
        "fibfib" |-> closureVal(
          ("n", .ParamNames),
          Assign(Name("a"), Int(0))
          Assign(Name("b"), Int(0))
          Assign(Name("c"), Int(1))
          Assign(Name("i"), Int(0))
          Assign(Name("next_value"), Int(1))
          While(
            Compare(Name("i"), CmpOp("<", Name("n"))),
            Assign(
              Name("next_value"),
              BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")))
            Assign(Name("a"), Name("b"))
            Assign(Name("b"), Name("c"))
            Assign(Name("c"), Name("next_value"))
            Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
            .Stmts)
          Return(Name("c"))
          .Stmts,
          0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
