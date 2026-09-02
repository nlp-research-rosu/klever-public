requires "verification.k"

module GROUND-ENTRY-SPEC
  imports MONOTONIC-VERIFICATION

  claim [ascending-ground]:
    <k>
      #loadAll(monotonicProgram)
      ~> Call(
           Name("monotonic"),
           list(vCons(1, vCons(2, vCons(2, .ValSeq))))
         )
      => true
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [zigzag-ground]:
    <k>
      #loadAll(monotonicProgram)
      ~> Call(
           Name("monotonic"),
           list(vCons(1, vCons(0, vCons(1, .ValSeq))))
         )
      => false
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
