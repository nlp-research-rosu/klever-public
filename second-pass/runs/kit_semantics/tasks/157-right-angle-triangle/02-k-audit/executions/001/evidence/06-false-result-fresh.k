requires "verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Fresh false result obligation: the real submitted body returns true for
  // the satisfiable entry state with inputs (3,4,5).
  claim [audit-false-result]:
    <k> Call(Name("right_angle_triangle"), 3, 4, 5)
         => ?RESULT:Bool </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "right_angle_triangle" |-> rightAngleTriangleClosure(),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RESULT ==Bool false
endmodule
