requires "verification.k"

module OPPOSITE-VALUE-WITNESS
  imports MATCH-PARENS-VERIFICATION

  // S is an intended-domain empty string, but V is deliberately given the
  // opposite interpretation: the empty (falsey) value.  #forceBranch ignores
  // V and chooses THEN from S/B instead.
  claim
    <k> str(.IntSeq)
         ~> #forceBranch(
              .IntSeq,
              Assign(Name("marker"), Int(1)) .Stmts,
              Assign(Name("marker"), Int(2)) .Stmts)
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(("marker" |-> 0), parent(-1))
      =>
      0 |-> scope(("marker" |-> 1), parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(forceIgnoresOppositeValue)]

  // The candidate's own direct #goodBranch rule makes the correct observable
  // choice for exactly the same falsey value: ELSE writes marker = 2.
  claim
    <k> str(.IntSeq)
         ~> #goodBranch(
              Assign(Name("marker"), Int(1)) .Stmts,
              Assign(Name("marker"), Int(2)) .Stmts)
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(("marker" |-> 0), parent(-1))
      =>
      0 |-> scope(("marker" |-> 2), parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(directBranchUsesActualValue)]
endmodule
