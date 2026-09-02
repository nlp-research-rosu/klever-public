requires "verification.k"

module GCD-SPEC
  imports GCD-VERIFICATION

  // ---- Loop invariant (circularity) — Euclid: (a, b) := (gcdF(A, B), 0) when the loop halts.
  claim
    <k>
      #while(Name("b"),
        Assign(TupleExpr(Name("a"), Name("b")),
               TupleExpr(Name("b"), BinOp("%", Name("a"), Name("b")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "a" <- A:Int ] [ "b" <- B:Int ], P:Parent)
               => scope(.Map [ "a" <- ?A2:Int ] [ "b" <- ?B2:Int ], P) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?A2 ==Int gcdF(A, B) andBool ?B2 ==Int 0
    [all-path]

  // ---- Entry claim — result = greatest_common_divisor(A, B) == gcdF(A, B).
  claim
    <k>
      FuncDef("greatest_common_divisor", Params("a", "b"),
        While(Name("b"),
          Assign(TupleExpr(Name("a"), Name("b")),
                 TupleExpr(Name("b"), BinOp("%", Name("a"), Name("b")))))
        Return(Name("a")))
      Assign(Name("result"), Call(Name("greatest_common_divisor"), (A:Int, B:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "greatest_common_divisor" <- ?_:Val ] [ "result" <- ?R:Int ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Int gcdF(A, B)
    [all-path]
endmodule
