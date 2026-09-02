requires "verification.k"

module MONOTONIC-SPEC-CLAIM2
  imports MONOTONIC-VERIFICATION

  claim
    <k>
      #loadAll(monotonicProgram)
      ~> Call(Name("monotonic"), list(VS:ValSeq))
      => nonincreasing(VS)
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
    requires notBool nondecreasing(VS)
endmodule
