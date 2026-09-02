requires "verification-body-mutated.k"

module TRIANGLE-AREA-BODY-MUTATION-SPEC
  imports TRIANGLE-AREA-BODY-MUTATION-VERIFICATION

  // The executed body and the expected final binding both use a+h, while the
  // result obligation deliberately remains the original a*h/2 theorem.
  claim
    <k>
      #loadAll(triangleAreaProgramMutation)
      ~> Call(Name("triangle_area"), Int(A), Int(H))
      => divII(A *Int H, 2)
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
                           BinOp("+", Name("a"), Name("h")),
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
