requires "verification.k"

module SPEC-DIAGNOSTIC
  imports VERIFICATION

  claim [execution-only]:
    <k>
      #loadAll(solutionModule) ~> Call(Name("solve"), N:Int)
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
    requires 0 <=Int N andBool N <=Int 10000
    ensures canonicalBin(?CODES)
endmodule
