requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Fresh false mutation: every correct result is required to be one larger.
  // Witness: IS = .IntList. The real result is 0; this destination requires 1.
  claim [main-result-plus-one]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("skjkasdkd"), (list(asVals(IS:IntList)), .Exprs))
      => digitSum(largestPrime(IS, 0)) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "skjkasdkd" |-> closureVal(
          ("lst", .ParamNames),
          #functionBody,
          0),
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
