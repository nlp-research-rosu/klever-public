requires "fixed-harness.k"

module SPEC-FIXED-HEAP
  imports FIXED-HARNESS

  claim
    <k>
      #runFixed(vCons(1.0, vCons(2.0, .ValSeq)))
      => ?RESULT:Val
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 => ?FINALSCOPELOC:Int </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => 7 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
