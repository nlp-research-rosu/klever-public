requires "verification.k"

module SPEC
  imports VERIFICATION

  // Circularity at the stable loop head (the source initializes the local
  // target before entering the loop).
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

  // Whole-function theorem: ordinary lookup, call-frame allocation, parameter
  // binding, body execution, return, and frame cleanup all use fixed MPY rules.
  claim [double-the-difference]:
    <k>
      Call(Name("double_the_difference"), (list(VS:ValSeq), .Exprs))
      => dtd(VS)
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
