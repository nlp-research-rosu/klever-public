requires "verification.k"

module TRIANGLE-AREA-SPEC-VACUITY-AUDIT
  imports TRIANGLE-AREA-VERIFICATION

  // Deliberately false: for A=5 and H=3, real execution returns divII(15, 2),
  // while this mutation demands divII(16, 2).
  claim
    <k>
      #loadAll(triangleAreaProgram)
      ~> Call(Name("triangle_area"), Int(A), Int(H))
      => divII((A *Int H) +Int 1, 2)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      =>
        0 |-> scope(
               "triangle_area"
                 |-> closureVal(
                       ("a", "h"),
                       Return(
                         BinOp(
                           "/",
                           BinOp("*", Name("a"), Name("h")),
                           Int(2))),
                       0),
               parent(-1))
        -1 |-> builtinsScope
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
