requires "verification.k"

module SEARCH-FRESH-VACUITY-SPEC
  imports SEARCH-VERIFICATION

  // Fresh false result mutation: for every satisfying input, the real result
  // is greatestFreq(ALL), not greatestFreq(ALL) + 1.  Witness ALL=[1] gives
  // 1 versus 2.
  claim
    <k> Call(Name("search"), list(ALL:IntValSeq), .Exprs)
      => greatestFreq(ALL) +Int 1
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
