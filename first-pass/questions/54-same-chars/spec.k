// spec.k — the reachability claim kprove discharges.
//
//   kompile verification.k --backend haskell \
//     --main-module SAME-CHARS-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module SAME-CHARS-SPEC

requires "verification.k"

module SAME-CHARS-SPEC
  imports SAME-CHARS-VERIFICATION

  // ---- Entry claim — see ../3-below-zero/PROOF.md ----------------------------
  // same_chars is a PURE nested expression (no loop): the two set() builtins fire once each
  // on the symbolic str(CS0)/str(CS1), and the == on the resulting sets reduces to sameSet,
  // composing to sameSet(dedupCodes(CS0), dedupCodes(CS1)) = sameChars(CS0, CS1).
  // After `result = same_chars(str(CS0), str(CS1))` the root scope's result is
  // sameChars(CS0, CS1): whether CS0 and CS1 consist of the same set of characters.
  // Holds for ANY symbolic code-sequences CS0, CS1 (no domain restriction — the function is
  // total).  Char codes are raw (case-sensitive); the equality is order/duplicate-agnostic.
  claim
    <k>
      FuncDef("same_chars", Params("s0", "s1"),
        Return(
          Compare(
            Call(Name("set"), Name("s0"), .Exprs),
            CmpOp("==", Call(Name("set"), Name("s1"), .Exprs)))))
      Assign(Name("result"),
        Call(Name("same_chars"), str(CS0:IntSeq), str(CS1:IntSeq), .Exprs))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "same_chars" <- ?_:Val ]
                       [ "result" <- sameChars(CS0, CS1) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
