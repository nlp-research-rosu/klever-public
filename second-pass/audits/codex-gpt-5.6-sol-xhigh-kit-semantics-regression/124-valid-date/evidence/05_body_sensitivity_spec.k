requires "verification-body-audit.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // Original program accepts January 31. The audit mutation changes only the
  // final 31-day branch to 30, so an execution-sensitive proof must reject this.
  claim [january-31]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(Name("valid_date"), Str("01-31-2000"))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
