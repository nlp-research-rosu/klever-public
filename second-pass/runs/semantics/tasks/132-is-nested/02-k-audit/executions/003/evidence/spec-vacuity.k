requires "verification.k"

module SPEC-VACUITY
  imports IS-NESTED-VERIFICATION-WITH-LOOP-LEMMA

  // Fresh false result mutation. The realizable empty-string input returns
  // false in both Python implementations and in the positive K claim.
  claim [empty-input-wrong-result]:
    <k> Call(Name("is_nested"), str(bCodes(bNil))) => true </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("is_nested" |-> isNestedClosure, parent(-1))
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
