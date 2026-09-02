requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False result mutation of function-correct at the satisfying input VS =
  // .ValSeq. The real and summarized result is -1, not 0.
  claim
    <k> #loadAll(solutionProgram)
        ~> Call(Name("can_arrange"), list(.ValSeq))
      => 0
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
    [label(false-empty-result)]
endmodule
