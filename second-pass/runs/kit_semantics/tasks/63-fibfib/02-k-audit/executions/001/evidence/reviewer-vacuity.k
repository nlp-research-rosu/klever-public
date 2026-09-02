requires "verification.k"

module REVIEWER-VACUITY
  imports VERIFICATION

  // Fresh false result obligation: the original program returns 24 at N=8.
  claim [false-off-by-one-at-eight]:
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
          Return(Name("a"))
          .Stmts)))
      ~> Call(Name("fibfib"), Int(8))
      => 25
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
          Return(Name("a"))
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
