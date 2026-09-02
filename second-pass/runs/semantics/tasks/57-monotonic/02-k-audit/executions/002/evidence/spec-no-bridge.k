requires "verification-no-bridge.k"

module MONOTONIC-SPEC-NO-BRIDGE
  imports MONOTONIC-VERIFICATION-NO-BRIDGE

  claim
    <k>
      #loadAll(monotonicProgramNoBridge)
      ~> Call(Name("monotonic"), list(VS:ValSeq))
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
    requires nondecreasingNoBridge(VS)

  claim
    <k>
      #loadAll(monotonicProgramNoBridge)
      ~> Call(Name("monotonic"), list(VS:ValSeq))
      => nonincreasingNoBridge(VS)
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
    requires notBool nondecreasingNoBridge(VS)
endmodule
