requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false on the satisfiable invalid-triangle domain
  // A + B <= C (for example A=1, B=2, C=10): the result is -1, not -2.
  claim [false-result]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Int, B:Int, C:Int, .Exprs))
      => -2
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
