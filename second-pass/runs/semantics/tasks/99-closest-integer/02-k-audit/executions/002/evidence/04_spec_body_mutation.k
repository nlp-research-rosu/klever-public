requires "verification-body-mutation.k"

module CLOSEST-INTEGER-SPEC-BODY-MUTATION
  imports CLOSEST-INTEGER-VERIFICATION

  // Universal functional correctness for every semantic string input:
  // float(value) is decStrToF(CS), and the result is exactly the
  // half-away-from-zero contract above.
  claim
    <k> runClosest(str(CS:IntSeq))
      => nearestAway(decStrToF(CS))
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
