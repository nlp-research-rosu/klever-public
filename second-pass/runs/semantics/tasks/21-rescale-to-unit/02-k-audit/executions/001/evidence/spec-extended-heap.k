requires "verification.k"

module SPEC-EXTENDED-HEAP
  imports VERIFICATION

  claim
    <k>
      #runRescale(vCons(1.0, vCons(2.0, .ValSeq)))
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
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
