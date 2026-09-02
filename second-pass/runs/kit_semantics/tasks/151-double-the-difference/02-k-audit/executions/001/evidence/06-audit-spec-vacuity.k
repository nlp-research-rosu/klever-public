requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #loop(list(VS:ValSeq), Name("number"), dtdLoopBody)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "double_the_difference" |->
          closureVal(("lst", .ParamNames), dtdBody, 0),
        parent(-1))
      1 |-> scope(
        "lst" |-> list(INPUT:ValSeq)
        "number" |-> (OLD:Val => lastNumber(VS, OLD))
        "result" |-> (S:Int => S +Int dtd(VS)),
        parent(0))
    </scopes>
    requires numericVals(VS)

  // Fresh audit mutation: false for the satisfying empty-list witness because
  // the real result and dtd(.ValSeq) are 0, not 1.
  claim [false-result-plus-one]:
    <k>
      Call(Name("double_the_difference"), (list(VS:ValSeq), .Exprs))
      => dtd(VS) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "double_the_difference" |->
          closureVal(("lst", .ParamNames), dtdBody, 0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires numericVals(VS)
endmodule
