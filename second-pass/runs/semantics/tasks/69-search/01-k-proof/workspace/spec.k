requires "verification.k"

module SEARCH-SPEC
  imports SEARCH-VERIFICATION

  // Entry-point theorem.  The non-empty/positive assumptions are precisely
  // the HumanEval precondition; the result is the declarative contract fold.
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
