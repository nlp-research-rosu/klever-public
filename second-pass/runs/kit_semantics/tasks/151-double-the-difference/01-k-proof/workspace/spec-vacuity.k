requires "verification.k"

module SPEC-VACUITY
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

  // Deliberately false by one for every input, including the realizable empty
  // list witness.
  claim [false-postcondition]:
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
