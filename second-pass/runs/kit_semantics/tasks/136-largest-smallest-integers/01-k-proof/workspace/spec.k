requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k> #loop(list(intVals(IS:IntSeq)), Name("value"), lsiLoopBody)
      => .K ... </k>
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
      -1 |-> builtinsScope
    </scopes>
    requires N <=Int 0
      andBool P >=Int 0

  claim [entry]:
    <k>
      #loadAll(Module(
        FuncDef("largest_smallest_integers", Params("lst"), lsiBody)))
      ~> Call(Name("largest_smallest_integers"), (list(intVals(IS:IntSeq)), .Exprs))
      => tuple(vCons(negativeResult(scanNeg(IS, 0)),
               vCons(positiveResult(scanPos(IS, 0)), .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "largest_smallest_integers"
           |-> closureVal(("lst", .ParamNames), lsiBody, 0),
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
