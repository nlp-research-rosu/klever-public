requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // The executed program term is materially changed to `return False`, while
  // retaining the true result obligation for the satisfiable input (3,4,5).
  claim [audit-mutated-body]:
    <k> Call(Name("right_angle_triangle"), 3, 4, 5)
         => ?RESULT:Bool </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "right_angle_triangle" |->
          closureVal(
            ("a", "b", "c"),
            Return(Bool(false)),
            0
          ),
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
    ensures ?RESULT ==Bool true
endmodule
