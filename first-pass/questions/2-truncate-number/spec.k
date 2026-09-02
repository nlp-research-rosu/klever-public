// spec.k — truncate_number on the UNIFIED semantics. Straight-line float entry claim. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module TRUNCATE-NUMBER-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module TRUNCATE-NUMBER-SPEC

requires "verification.k"

module TRUNCATE-NUMBER-SPEC
  imports TRUNCATE-NUMBER-VERIFICATION

  // ---- Entry claim -----------------------------------------------------------
  // After `result = truncate_number(F)` for a symbolic Float F, result == truncRes(F) =
  // floatMod(F, 1.0) — EXACTLY the term the body `number % 1.0` builds. floatMod is
  // uninterpreted, so this is a purely STRUCTURAL float result.
  claim
    <k>
      FuncDef("truncate_number", Params("number"),
        Return(BinOp("%", Name("number"), Float(1.0))))
      Assign(Name("result"), Call(Name("truncate_number"), F:Float))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "truncate_number" <- ?_:Val ] [ "result" <- truncRes(F) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
