requires "verification.k"

module REAL-PROGRAM-PIN-SPLIT
  imports X-OR-Y-SUMMARY

  claim
    <k>
      #loadAll(
        Module(
          FuncDef("x_or_y", Params("n", "x", "y"),
            If(Compare(Name("n"), CmpOp("<", Int(2))),
              Return(Name("y")),
              .Stmts)
            For(Name("divisor"), Call(Name("range"), Int(2), Name("n")),
              If(Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("==", Int(0))),
                Return(Name("y")),
                .Stmts))
            Return(Name("x"))))
      )
      ~> Call(Name("x_or_y"), N:Int, X:Val, Y:Val)
      => Y
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> (
        scope(.Map, parent(-1))
        =>
        scope(
          "x_or_y" |-> closureVal(
            ("n", "x", "y"),
            If(Compare(Name("n"), CmpOp("<", Int(2))),
              Return(Name("y")),
              .Stmts)
            For(Name("divisor"), Call(Name("range"), (Int(2), Name("n"))),
              If(Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("==", Int(0))),
                Return(Name("y")),
                .Stmts))
            Return(Name("x")),
            0),
          parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N <Int 2
    [label(real_program_pin_small)]

  claim
    <k>
      #loadAll(
        Module(
          FuncDef("x_or_y", Params("n", "x", "y"),
            If(Compare(Name("n"), CmpOp("<", Int(2))),
              Return(Name("y")),
              .Stmts)
            For(Name("divisor"), Call(Name("range"), Int(2), Name("n")),
              If(Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("==", Int(0))),
                Return(Name("y")),
                .Stmts))
            Return(Name("x"))))
      )
      ~> Call(Name("x_or_y"), N:Int, X:Val, Y:Val)
      => primeSelect(N, 2, X, Y)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> (
        scope(.Map, parent(-1))
        =>
        scope(
          "x_or_y" |-> closureVal(
            ("n", "x", "y"),
            If(Compare(Name("n"), CmpOp("<", Int(2))),
              Return(Name("y")),
              .Stmts)
            For(Name("divisor"), Call(Name("range"), (Int(2), Name("n"))),
              If(Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("==", Int(0))),
                Return(Name("y")),
                .Stmts))
            Return(Name("x")),
            0),
          parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 2
    [label(real_program_pin_scan)]
endmodule
