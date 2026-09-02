requires "verification.k"

module SEARCH-FALSE-POSTCONDITION
  imports SEARCH-VERIFICATION

  // Deliberately false: for every satisfying input, the returned value is
  // claimed to be one greater than the contract fold. Witness ALL=[1]:
  // the real result is 1, while this destination is 2.
  claim
    <k> Call(Name("search"), list(ALL:IntValSeq), .Exprs)
      => greatestFreq(ALL) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "search" |-> closureVal(
               "lst", .ParamNames,
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
