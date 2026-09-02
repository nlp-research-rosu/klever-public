requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false-postcondition mutation: N=5 satisfies N>0, but the real
  // submitted body returns 1, not 2.
  claim [false-entry-n5]:
    <k>
      Call(Name("get_max_triples"), (Int(5), .Exprs))
      => 2
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
