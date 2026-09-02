requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the correct result for [1, 2] is 2, not None.
  claim [false-result]:
    <k> Call(Name("next_smallest"),
             (list(vCons(1, vCons(2, .ValSeq))), .Exprs))
        => noneV </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "next_smallest" |->
          closureVal(("lst", .ParamNames), nextSmallestBody, 0),
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
