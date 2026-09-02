requires "verification.k"

module AUDIT-VACUITY
  imports VERIFICATION

  // Fresh false mutation: prepend an extra zero to the required result list.
  // For the satisfying input INPUT = .ValSeq, the real result is empty while
  // this postcondition requires [0].
  claim [extra-result-element]:
    <k>
      Call(
        closureVal(("lst", .ParamNames), strangeBody(), 0),
        list(INPUT:ValSeq))
      =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortVS(INPUT))
      1 |-> list(vCons(0, strangeResult(sortVS(INPUT))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
