requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfiable input [2]: the real result is 2.
  claim [false-result]:
    <k>
      #loadAll(
        Module(
          FuncDef("skjkasdkd", Params("lst"), targetBody)))
      ~> Call(
           Name("skjkasdkd"),
           list(vCons(2, .ValSeq)))
      => digitSum(largestPrime(vCons(2, .ValSeq), 0)) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "skjkasdkd" |->
             closureVal(("lst", .ParamNames), targetBody, 0),
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
