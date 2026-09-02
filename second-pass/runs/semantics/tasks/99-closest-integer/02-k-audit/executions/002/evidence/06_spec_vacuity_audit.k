requires "verification.k"

module CLOSEST-INTEGER-SPEC-VACUITY-AUDIT
  imports CLOSEST-INTEGER-VERIFICATION

  // Fresh false mutation: for the satisfiable input CS = codes("10"), the
  // original program/result expression is 10, not 11.
  claim
    <k> runClosest(str(CS:IntSeq))
      => nearestAway(decStrToF(CS)) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
