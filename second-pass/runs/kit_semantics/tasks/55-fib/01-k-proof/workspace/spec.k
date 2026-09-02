requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-inv]:
    <k>
      #while(
        Compare(Name("n"), CmpOp(">", Int(0))),
        Assign(Name("b"), BinOp("+", Name("a"), Name("b")))
        Assign(Name("a"), BinOp("-", Name("b"), Name("a")))
        Assign(Name("n"), BinOp("-", Name("n"), Int(1)))
      )
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      SC:Map
      1 |-> scope(
        "n" |-> (N:Int => 0)
        "a" |-> (A:Int => fibFrom(A, B, N))
        "b" |-> (B:Int => ?BFinal:Int),
        parent(0)
      )
    </scopes>
    requires N >=Int 0

  claim [fib-call]:
    <k>
      Call(Name("fib"), Int(N:Int))
      => fibFrom(0, 1, N)
    </k>
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
    requires N >=Int 0
endmodule
