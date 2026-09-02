requires "verification.k"

module AUDIT-GROUND-SPEC
  imports VERIFICATION

  // Satisfying witness for the entry precondition: N = 5 > 0.
  // The result is the concrete canonical/example result, not tripleCount(5).
  claim [ground-n5]:
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
