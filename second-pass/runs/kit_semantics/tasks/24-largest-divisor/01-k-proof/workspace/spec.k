requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #while(
        Compare(
          BinOp("%", Name("n"), Name("divisor")),
          CmpOp("!=", Int(0))),
        Assign(
          Name("divisor"),
          BinOp("-", Name("divisor"), Int(1))) .Stmts)
      ~> Return(Name("divisor")) .Stmts
      ~> #endcall
      =>
      largestDivisorAtOrBelow(N, D) ~> CONT
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(
          "largest_divisor" |->
            closureVal(
              "n",
              Assign(
                Name("divisor"),
                BinOp("-", Name("n"), Int(1)))
              While(
                Compare(
                  BinOp("%", Name("n"), Name("divisor")),
                  CmpOp("!=", Int(0))),
                Assign(
                  Name("divisor"),
                  BinOp("-", Name("divisor"), Int(1))) .Stmts)
              Return(Name("divisor")) .Stmts,
              0),
          parent(-1))
        1 |-> scope(
          "n" |-> N
          "divisor" |-> D,
          parent(0))
      )
      =>
      ( -1 |-> builtinsScope
        0 |-> scope(
          "largest_divisor" |->
            closureVal(
              "n",
              Assign(
                Name("divisor"),
                BinOp("-", Name("n"), Int(1)))
              While(
                Compare(
                  BinOp("%", Name("n"), Name("divisor")),
                  CmpOp("!=", Int(0))),
                Assign(
                  Name("divisor"),
                  BinOp("-", Name("divisor"), Int(1))) .Stmts)
              Return(Name("divisor")) .Stmts,
              0),
          parent(-1))
      )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(CONT, 0, 1)) => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 2
     andBool D >=Int 1

  claim [largest-divisor]:
    <k>
      Call(Name("largest_divisor"), Int(N))
      =>
      largestDivisorAtOrBelow(N, N -Int 1)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "largest_divisor" |->
          closureVal(
            "n",
            Assign(
              Name("divisor"),
              BinOp("-", Name("n"), Int(1)))
            While(
              Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("!=", Int(0))),
              Assign(
                Name("divisor"),
                BinOp("-", Name("divisor"), Int(1))) .Stmts)
            Return(Name("divisor")) .Stmts,
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
    requires N >=Int 2
endmodule
