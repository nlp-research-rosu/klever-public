requires "verification-mutation.k"

module SPEC-BODY-MUTATION
  imports MUTATION

  // Deliberately false for the mutated body: it always returns None.
  claim [body-sensitive]:
    <k> Call(Name("next_smallest"),
             (list(vCons(1, vCons(2, .ValSeq))), .Exprs))
        => 2 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "next_smallest" |->
          closureVal(("lst", .ParamNames), mutantBody, 0),
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
