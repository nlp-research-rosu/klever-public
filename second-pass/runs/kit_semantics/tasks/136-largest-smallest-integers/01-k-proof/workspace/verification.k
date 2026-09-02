requires "verification-core.k"

module VERIFICATION
  imports VERIFICATION-CORE

  // This rule is admitted only after loop-spec.k proves the identical
  // reachability transition against VERIFICATION-CORE, which has no such
  // bridge.  Its arbitrary continuation and omitted cells have exactly the
  // same framing as that connection theorem.
  rule <k>
    #loop(list(intVals(IS:IntSeq)), Name("value"), lsiLoopBody)
    => .K
    ...
  </k>
  <env> 1 </env>
  <scopes>
    1 |-> scope(
      "largest_negative" |-> (N:Int => scanNeg(IS, N))
      "lst" |-> INPUT:Val
      "smallest_positive" |-> (P:Int => scanPos(IS, P))
      "value" |-> (CURRENT:Int => lastValue(IS, CURRENT)),
      parent(0))
    0 |-> scope(
      "largest_smallest_integers"
        |-> closureVal(("lst", .ParamNames), lsiBody, 0),
      parent(-1))
    -1 |-> BUILTINS:Scope
  </scopes>
  requires N <=Int 0
    andBool P >=Int 0
  [priority(40)]
endmodule
