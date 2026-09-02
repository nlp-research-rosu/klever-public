requires "verification.k"

module AUDIT-SPEC-FALSE-RESULT
  imports VERIFICATION

  // Deliberately false: for N=5 the real/program result is 1, but this asks for 2.
  claim [false-plus-one]:
    <k>
      Call(Name("get_max_triples"), (Int(N:Int), .Exprs))
      => tripleCount(N) +Int 1
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
    requires N >Int 0
endmodule
