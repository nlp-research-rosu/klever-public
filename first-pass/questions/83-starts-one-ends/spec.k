// spec.k — starts_one_ends on the UNIFIED semantics (src/). Straight-line single guard (no loop):
// result = soe(N) = (N==1 ? 1 : 18*10^(N-2)). The program's `if n==1` case-splits; each branch
// matches soe's corresponding [simplification] arm. Domain N >= 1. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module STARTS-ONE-ENDS-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module STARTS-ONE-ENDS-SPEC

requires "verification.k"

module STARTS-ONE-ENDS-SPEC
  imports STARTS-ONE-ENDS-VERIFICATION

  // ---- Entry claim — result = starts_one_ends(N) == soe(N). The `if n==1: return 1` returns early;
  // otherwise the body falls through to `return 18 * 10 ** (n-2)`. kprove splits on N==1 and matches
  // the corresponding soe arm. Domain N >= 1 (so the N=/=1 arm has N>=2, exponent N-2 >= 0).
  claim
    <k>
      FuncDef("starts_one_ends", Params("n"),
        If(Compare(Name("n"), CmpOp("==", Int(1))),
           Return(Int(1)),
           .Stmts)
        Return(BinOp("*", Int(18), BinOp("**", Int(10), BinOp("-", Name("n"), Int(2))))))
      Assign(Name("result"), Call(Name("starts_one_ends"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "starts_one_ends" <- ?_:Val ] [ "result" <- soe(N) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1
    [all-path]
endmodule
