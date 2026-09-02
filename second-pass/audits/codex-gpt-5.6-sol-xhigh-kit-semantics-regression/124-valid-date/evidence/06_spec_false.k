requires "verification.k"

module AUDIT-SPEC-FALSE
  imports VERIFICATION

  // Fresh audit mutation: 03-11-2000 satisfies the length-10 entry domain and
  // the real program returns true. The deliberately false destination below
  // tests that the proof constrains the returned Boolean.
  claim [false-march-result]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(Name("valid_date"), Str("03-11-2000"))
      => false
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
