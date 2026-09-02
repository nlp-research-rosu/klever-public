requires "../../tmp/audit-work/rebuild/verification.k"

module FIBFIB-SPEC-VACUITY
  imports FIBFIB-VERIFICATION

  claim [fibfib-loop]:
    <k>
      #while(Compare(Name("i"), CmpOp("<", Name("n"))),
        Assign(Name("d"),
          BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")))
        Assign(Name("a"), Name("b"))
        Assign(Name("b"), Name("c"))
        Assign(Name("c"), Name("d"))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "a" |-> (A:Int => fibFrom(A, B, C, N -Int I))
        "b" |-> (B:Int => ?_B:Int)
        "c" |-> (C:Int => ?_C:Int)
        "d" |-> (_D:Int => ?_D:Int)
        "i" |-> (I:Int => N:Int)
        "n" |-> N,
        _P:Parent) ...
    </scopes>
    requires 0 <=Int I andBool I <=Int N

  // Deliberately false at the satisfying witness N = 0: the real call returns
  // 0, while this destination requires 1.
  claim [fibfib-correct-plus-one]:
    <k>
      Call(Name("fibfib"), Int(N:Int))
      => fibFrom(0, 0, 1, N) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "fibfib" |-> closureVal(
          "n", .ParamNames,
          Assign(Name("a"), Int(0))
          Assign(Name("b"), Int(0))
          Assign(Name("c"), Int(1))
          Assign(Name("i"), Int(0))
          Assign(Name("d"), Int(0))
          While(Compare(Name("i"), CmpOp("<", Name("n"))),
            Assign(Name("d"),
              BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")))
            Assign(Name("a"), Name("b"))
            Assign(Name("b"), Name("c"))
            Assign(Name("c"), Name("d"))
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
    requires N >=Int 0
endmodule
