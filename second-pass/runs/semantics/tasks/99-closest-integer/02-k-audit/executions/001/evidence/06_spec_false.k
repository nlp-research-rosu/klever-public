requires "verification.k"

module CLOSEST-INTEGER-SPEC-FALSE
  imports CLOSEST-INTEGER-VERIFICATION

  // Fresh false mutation: require every actual result to be one greater than
  // the result-constraining target. CS = codes("10") satisfies the source
  // configuration and makes the original result 10, while this demands 11.
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
