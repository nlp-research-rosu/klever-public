requires "verification.k"

module SPEC
  imports VERIFICATION

  // Circularity at the recurring internal while-loop head.  The continuation
  // and all configuration cells except the active local scope are framed.
  claim [loop-invariant]:
    <k>
      #while(
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
        Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
      ) => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        ("n" |-> N:Int)
        ("i" |-> (I:Int => N))
        ("a" |-> (fib4Spec(I) => fib4Spec(N)))
        ("b" |-> (fib4Spec(I +Int 1) => ?BFinal:Int))
        ("c" |-> (fib4Spec(I +Int 2) => ?CFinal:Int))
        ("d" |-> (fib4Spec(I +Int 3) => ?DFinal:Int))
        ("e" |-> (E:Int => ?EFinal:Int)),
        P:Parent)
      ...
    </scopes>
    requires I >=Int 0 andBool I <=Int N

  // Exact source-level invocation boundary: lookup is pinned to the translated
  // fib4 closure, and the supplied semantics executes its complete body.
  claim [fib4-correct]:
    <k>
      Call(Name("fib4"), Int(N:Int))
      =>
      fib4Spec(N)
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
    requires N >=Int 0
endmodule
