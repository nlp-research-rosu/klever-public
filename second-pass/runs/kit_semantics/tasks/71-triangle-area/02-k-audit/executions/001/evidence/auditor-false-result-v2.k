requires "verification.k"

module AUDITOR-FALSE-RESULT-V2
  imports VERIFICATION

  // Satisfiable witness: A=1, B=2, C=3. The real invalid result is -1.
  claim [false-invalid-result]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Int, B:Int, C:Int, .Exprs))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A +Int B <=Int C
endmodule
