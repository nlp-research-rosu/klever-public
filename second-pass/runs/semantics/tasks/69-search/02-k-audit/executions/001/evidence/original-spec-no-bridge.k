requires "verification-no-bridge.k"

module SEARCH-SPEC-NO-BRIDGE
  imports SEARCH-VERIFICATION

  // Original target claim, with only the candidate operational bridge removed.
  claim
    <k> Call(Name("search"), list(ALL:IntValSeq), .Exprs)
      => greatestFreq(ALL)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "search" |-> closureVal(
               "lst" , .ParamNames,
               #searchBody,
               0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires nonEmpty(ALL)
     andBool allPositive(ALL)
endmodule
