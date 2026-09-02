requires "verification-body-mutant.k"

module BODY-MUTATION-SPEC
  imports VERIFICATION-BODY-MUTANT

  claim
    <k>
      Call(
        Name("derivative"),
        list(
          asValSeq(
            ivCons(3, ivCons(1, ivCons(2, ivCons(4, ivCons(5, .IntVals)))))
          )
        )
      )
      => ref(?RESULT:Int)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("derivative" |-> derivativeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      ?RESULT |->
        list(vCons(1, vCons(4, vCons(12, vCons(20, .ValSeq)))))
      ?REST:Map
    </heap>
    <heapLoc> 0 => ?NEXT:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    [label(body-mutation-must-fail)]
endmodule
