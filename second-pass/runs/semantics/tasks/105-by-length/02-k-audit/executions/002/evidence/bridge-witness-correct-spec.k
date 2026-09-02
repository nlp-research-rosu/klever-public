requires "bridge-witness-fixed.k"

module LOOP-WITNESS-CORRECT-SPEC
  imports LOOP-WITNESS-FIXED

  claim [filter-loop-correct]:
    <k>
      #applyK(
        toCall(filterLoopWitnessClosure),
        (list(vCons(2, .ValSeq)), .Vals))
    => 2
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

  claim [map-loop-correct]:
    <k>
      #applyK(
        toCall(mapLoopWitnessClosure),
        (list(vCons(2, .ValSeq)), .Vals))
    => 2
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
