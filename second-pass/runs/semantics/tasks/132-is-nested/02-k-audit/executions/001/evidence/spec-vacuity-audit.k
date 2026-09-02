requires "verification.k"

module IS-NESTED-VACUITY-AUDIT
  imports IS-NESTED-VERIFICATION-WITH-LOOP-LEMMA

  // Deliberately false result mutation.  For BS = bNil, the actual result and
  // nested(BS) are false, while this postcondition demands true.
  claim [false-negated-result]:
    <k>
      Call(Name("is_nested"), str(bCodes(BS:BSeq)))
      => notBool nested(BS)
    </k>
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
