requires "verification-wrong-extrema.k"

module SPEC-WRONG-EXTREMA-SYMBOLIC
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
             wrongLo(),
             wrongHi()))
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
