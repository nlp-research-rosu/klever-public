requires "verification.k"

module SEARCH-GROUND-WITNESS-SPEC
  imports SEARCH-VERIFICATION

  // Satisfying precondition witness [1]; both Python implementations return 1.
  claim [one]:
    <k> Call(Name("search"), list((vCons(1, .ValSeq)):IntValSeq), .Exprs) => 1 </k>
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

  // Satisfying precondition witness [2]; both Python implementations return -1.
  claim [two]:
    <k> Call(Name("search"), list((vCons(2, .ValSeq)):IntValSeq), .Exprs) => -1 </k>
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

  // First documented example.
  claim [example]:
    <k> Call(Name("search"),
             list((vCons(4, vCons(1, vCons(2, vCons(2, vCons(3, vCons(1, .ValSeq))))))):IntValSeq),
             .Exprs)
      => 2
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
endmodule
