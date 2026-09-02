requires "verification-wrong-extrema.k"

module SPEC-WRONG-EXTREMA-ORIGINAL-SHAPE
  imports VERIFICATION-WRONG-EXTREMA

  claim
    <k>
      #runRescale(
        vCons(FIRST:Float,
          vCons(SECOND:Float, REST:ValSeq)))
      => list(
           scaleAcc(
             .ValSeq,
             vCons(FIRST,
               vCons(SECOND, REST)),
             minVF(
               vCons(FIRST,
                 vCons(SECOND, REST))),
             maxVF(
               vCons(FIRST,
                 vCons(SECOND, REST)))))
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
    requires allFloats(REST)
endmodule
