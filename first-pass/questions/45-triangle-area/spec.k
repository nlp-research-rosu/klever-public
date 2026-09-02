// spec.k — triangle_area on the UNIFIED semantics. Straight-line float entry claim. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module TRIANGLE-AREA-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module TRIANGLE-AREA-SPEC

requires "verification.k"

module TRIANGLE-AREA-SPEC
  imports TRIANGLE-AREA-VERIFICATION

  // ---- Entry claim -----------------------------------------------------------
  // After `result = triangle_area(A, H)`, result == triangleRes(A, H) = intFloatDiv(A*Int H, 2.0)
  // — EXACTLY the term the body `a * h / 2.0` builds (a*h is A*Int H; /2.0 => intFloatDiv over the
  // float literal). intFloatDiv is uninterpreted, so this is a purely STRUCTURAL float result.
  claim
    <k>
      FuncDef("triangle_area", Params("a", "h"),
        Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Float(2.0))))
      Assign(Name("result"), Call(Name("triangle_area"), A:Int, H:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "triangle_area" <- ?_:Val ] [ "result" <- triangleRes(A, H) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A >Int 0 andBool H >Int 0
    [all-path]
endmodule
