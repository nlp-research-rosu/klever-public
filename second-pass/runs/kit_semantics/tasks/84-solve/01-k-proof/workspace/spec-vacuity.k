requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Satisfiable witness N=150. The real result decodes to 6, not 7.
  claim [false-result]:
    <k>
      #loadAll(solutionModule) ~> Call(Name("solve"), 150)
      =>
      str(?CODES:IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?SCOPES:Map
    </scopes>
    <scopeLoc> 1 => ?SCOPELOC:Int </scopeLoc>
    <heap> .Map => ?HEAP:Map </heap>
    <heapLoc> 0 => ?HEAPLOC:Int </heapLoc>
    <stack> .List => ?STACK:List </stack>
    <ret> noRet => ?RET:RetState </ret>
    <exc> NoExc => ?EXC:Exc </exc>
    <exit-code> 0 => ?EXIT:Int </exit-code>
    ensures canonicalBin(?CODES) andBool decodeBin(?CODES) ==Int 7
endmodule
