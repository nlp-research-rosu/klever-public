requires "verification.k"

module SPEC-GROUND-EQUAL-CLAIMED
  imports VERIFICATION

  claim
    <k>
      #runRescale(vCons(2.0, vCons(2.0, .ValSeq)))
      => list(
           scaleAcc(
             .ValSeq,
             vCons(2.0, vCons(2.0, .ValSeq)),
             minVF(vCons(2.0, vCons(2.0, .ValSeq))),
             maxVF(vCons(2.0, vCons(2.0, .ValSeq)))))
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
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
