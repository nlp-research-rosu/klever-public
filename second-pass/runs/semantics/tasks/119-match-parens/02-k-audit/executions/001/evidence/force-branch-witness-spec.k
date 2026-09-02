requires "force-branch-witness.k"

module FORCE-BRANCH-WITNESS-SPEC
  imports FORCE-BRANCH-WITNESS

  // The proof extension chooses THEN from S, although the actual branch value
  // V is the empty (falsey) string.
  claim
    <k> str(.IntSeq)
         ~> #forceBranch(.IntSeq, ThenMark .Stmts, ElseMark .Stmts)
      => thenReached
    </k>
    <env> 0 </env>
    <scopes> .Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(bridgeChoosesThen)]

  // The supplied semantics' native If correctly chooses ELSE for the exact
  // same empty (falsey) branch value.
  claim
    <k> If(str(.IntSeq), ThenMark .Stmts, ElseMark .Stmts)
      => elseReached
    </k>
    <env> 0 </env>
    <scopes> .Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(nativeChoosesElse)]
endmodule
