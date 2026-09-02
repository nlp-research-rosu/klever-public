requires "verification.k"

module BODY-MUTATION-GROUND-SPEC
  imports VERIFICATION

  // The mutated body assigns index + 1 on a descent. For [2,1] it returns 2,
  // whereas the submitted source and canonical function return 1.
  claim
    <k> #loadAll(solutionProgram)
        ~> Call(Name("can_arrange"), list(vCons(2, vCons(1, .ValSeq))))
      => 2
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 => ?FINALSCOPELOC:Int </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List => ?FINALSTACK:List </stack>
    <ret> noRet => ?FINALRET:RetState </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(mutated-ground-result)]
endmodule
