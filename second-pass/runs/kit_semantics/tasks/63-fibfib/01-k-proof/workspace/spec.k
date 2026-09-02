requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [fibfib-loop]:
    <k>
      #while(
        Compare(Name("i"), CmpOp("<", Name("n"))),
        Assign(
          Name("next_value"),
          BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")))
        Assign(Name("a"), Name("b"))
        Assign(Name("b"), Name("c"))
        Assign(Name("c"), Name("next_value"))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
        .Stmts)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
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
      1 |-> scope(
        "n"          |-> N:Int
        "a"          |-> (fibfibSpec(I:Int)        => fibfibSpec(N))
        "b"          |-> (fibfibSpec(I +Int 1)     => fibfibSpec(N +Int 1))
        "c"          |-> (fibfibSpec(I +Int 2)     => fibfibSpec(N +Int 2))
        "i"          |-> (I                        => N)
        "next_value" |-> (fibfibSpec(I +Int 2)     => fibfibSpec(N +Int 2)),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool I <=Int N

  claim [fibfib-entry]:
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
      ~> Call(Name("fibfib"), Int(N:Int))
      => fibfibSpec(N)
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
    requires N >=Int 0
endmodule
