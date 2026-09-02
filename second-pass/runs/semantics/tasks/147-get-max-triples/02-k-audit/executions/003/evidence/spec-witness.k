requires "verification.k"

module SPEC-WITNESS
  imports VERIFICATION

  // N = 5 satisfies the entry precondition and its intended answer is 1.
  claim [entry-n5]:
    <k>
      Call(Name("get_max_triples"), (Int(5), .Exprs))
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "get_max_triples" |-> closureVal(
          ("n", .ParamNames), getMaxTriplesBody, 0),
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
