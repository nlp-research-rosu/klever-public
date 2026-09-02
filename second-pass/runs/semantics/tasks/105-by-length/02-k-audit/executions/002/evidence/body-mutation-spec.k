requires "body-mutated-verification.k"

module BODY-MUTATION-SPEC
  imports BY-LENGTH-VERIFICATION

  // The original result for input [2] is ["Two"]. The mutated actual body
  // appends 3, so a body-sensitive proof must reject this stale obligation.
  claim [stale-original-result]:
    <k>
      #applyK(
        toCall(byLengthClosure),
        (list(vCons(2, .ValSeq)), .Vals))
      ~> #observeList
    =>
      list(vCons(str(strToCodes("Two")), .ValSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
