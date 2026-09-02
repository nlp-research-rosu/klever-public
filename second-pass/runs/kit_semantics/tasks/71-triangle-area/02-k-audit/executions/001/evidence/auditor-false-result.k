requires "verification.k"

module AUDITOR-FALSE-RESULT
  imports VERIFICATION

  // Ground witness: Python triangle_area(3, 4, 5) is 6.0, never -1.
  claim [false-ground-result]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (3, 4, 5, .Exprs))
      => -1
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
endmodule
