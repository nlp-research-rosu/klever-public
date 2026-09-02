requires "bridge-witness-extended.k"

module LOOP-WITNESS-FALSE-SPEC
  imports LOOP-WITNESS-EXTENDED

  // Both claims are false under the fixed semantics: a Python for-loop leaves
  // its target bound to the last iterated value, namely 2. The proof-local
  // bridge erases the whole loop in an arbitrary continuation and leaves 99.
  claim [filter-loop-false]:
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

  claim [map-loop-false]:
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
