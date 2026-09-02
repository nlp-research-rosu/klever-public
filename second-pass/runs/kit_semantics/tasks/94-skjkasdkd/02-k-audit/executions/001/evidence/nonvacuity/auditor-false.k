requires "verification.k"

module AUDITOR-FALSE
  imports VERIFICATION

  // Satisfiable input [3, 4] returns 3, so the off-by-one result 4 is false.
  claim [auditor-false-result]:
    <k>
      #loadAll(
        Module(
          FuncDef("skjkasdkd", Params("lst"), targetBody)))
      ~> Call(
           Name("skjkasdkd"),
           list(vCons(3, vCons(4, .ValSeq))))
      => digitSum(
           largestPrime(vCons(3, vCons(4, .ValSeq)), 0)) +Int 1
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
