requires "bridge-witness-fixed.k"

module LOOP-WITNESS-FIXED-FALSE-SPEC
  imports LOOP-WITNESS-FIXED

  claim [filter-loop-fixed-rejects-99]:
    <k>
      #applyK(
        toCall(filterLoopWitnessClosure),
        (list(vCons(2, .ValSeq)), .Vals))
    => 99
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

  claim [map-loop-fixed-rejects-99]:
    <k>
      #applyK(
        toCall(mapLoopWitnessClosure),
        (list(vCons(2, .ValSeq)), .Vals))
    => 99
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
