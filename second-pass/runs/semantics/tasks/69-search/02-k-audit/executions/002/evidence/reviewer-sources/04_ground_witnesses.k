requires "04_witness_extension.k"

module SEARCH-GROUND-WITNESSES
  imports SEARCH-WITNESS-EXTENSION

  claim
    <k> Call(Name("search"), list(oneSeq), .Exprs) => 1 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "search" |-> closureVal("lst", .ParamNames, #searchBody, 0),
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

  claim
    <k> Call(Name("search"), list(twoSeq), .Exprs) => -1 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "search" |-> closureVal("lst", .ParamNames, #searchBody, 0),
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

  claim
    <k> Call(Name("search"), list(twoTwoSeq), .Exprs) => 2 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "search" |-> closureVal("lst", .ParamNames, #searchBody, 0),
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

  claim
    <k>
      Call(
        Name("search"),
        list(exampleSeq),
        .Exprs)
      => 2
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "search" |-> closureVal("lst", .ParamNames, #searchBody, 0),
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
